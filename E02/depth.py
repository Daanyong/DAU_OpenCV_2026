# Stereo Disparity 기반 Depth 추정
# 같은 장면을 왼쪽 카메라와 오른쪽 카메라에서 촬영한 두 장의 이미지를 이용해 깊이를 추정
# 두 이미지에서 같은 물체가 얼마나 옆으로 이동해 보이는지 계산하여 물체가 카메라에서 얼마나 떨어져 있는지(depth)를 구할 수 있음
# Disparity: Left 이미지와 right 이미지에서 같은 물체의 픽셀 위치 차이, 값이 클 수록 가까운 물체
# Depth: Disparity를 이용하면 물체의 실제 거리 정보를 계산할 수 있음, 값이 작을 수록 가까운 물체

import cv2
import numpy as np
from pathlib import Path

# 출력 폴더 생성
output_dir = Path("./outputs")
output_dir.mkdir(parents=True, exist_ok=True)

# 좌/우 이미지 불러오기
left_color = cv2.imread("../images/left.png")
right_color = cv2.imread("../images/right.png")

if left_color is None or right_color is None:
    raise FileNotFoundError("좌/우 이미지를 찾지 못했습니다.")


# 카메라 파라미터
f = 700.0
B = 0.12

# 각 ROI를(x, y, width, height) 형태로 정의
rois = {
    "Painting": (55, 50, 130, 110),
    "Frog": (90, 265, 230, 95),
    "Teddy": (310, 35, 115, 90)
}

# 요구사항 1: 입력 이미지를 그레이스케일로 변환
left_gray = cv2.cvtColor(left_color, cv2.COLOR_BGR2GRAY)
right_gray = cv2.cvtColor(right_color, cv2.COLOR_BGR2GRAY)

# -----------------------------
# 1. Disparity 계산
# -----------------------------
# 요구사항 1: cv2.StereoBM_create()를 사용하여 disparity map 계산
stereo = cv2.StereoBM_create(numDisparities=96, blockSize=15)

# StereoBM은 정수형 disparity 값을 16배 스케일해서 반환하므로 Depth 계산을 위해서 실수 연산으로 변경 후 16으로 나눠서 사용
disparity = stereo.compute(left_gray, right_gray).astype(np.float32) / 16.0

# -----------------------------
# 2. Depth 계산
# Z = fB / d
# -----------------------------
# 요구사항 2: Disparity > 0인 픽셀만 사용하여 depth map 계산
depth_map = np.zeros_like(disparity, dtype=np.float32)
valid_mask = disparity > 0

# 유효한 disparity 값이 없는 경우를 대비하여 예외 처리
depth_map[valid_mask] = (f * B) / disparity[valid_mask]

# -----------------------------
# 3. ROI별 평균 disparity / depth 계산
# -----------------------------
# 요구사항 3: ROI Painting, Frog, Teddy 각각에 대해 평균 disparity와 평균 depth를 계산
results = {}

# 각 ROI에 대해 유효한 disparity 값이 있는 픽셀만 평균 계산
for name, (x, y, w, h) in rois.items():
    roi_disp = disparity[y:y+h, x:x+w] # 3개의 ROI 영역에서 disparity와 depth 값을 추출
    roi_depth = depth_map[y:y+h, x:x+w] # 3개의 ROI 영역에서 disparity와 depth 값을 추출

    roi_valid = roi_disp > 0 # 유효한 disparity 값이 있는 픽셀만 평균 계산

    # 유효한 픽셀이 있는 경우에만 평균 계산, 그렇지 않으면 NaN으로 처리
    if np.any(roi_valid):
        mean_disp = np.mean(roi_disp[roi_valid])
        mean_depth = np.mean(roi_depth[roi_valid])
        valid_pixels = np.count_nonzero(roi_valid)
    else:
        mean_disp = np.nan
        mean_depth = np.nan
        valid_pixels = 0

    results[name] = {
        "mean_disparity": mean_disp,
        "mean_depth": mean_depth,
    }

# -----------------------------
# 4. 결과 출력
# -----------------------------
print("===== ROI별 평균 Disparity / Depth =====")
for name, result in results.items():
    print(f"[{name}]")
    print(f"Mean Disparity: {result['mean_disparity']:.4f}")
    print(f"Mean Depth: {result['mean_depth']:.4f}")

# 요구사항 4: 세 ROI 중 어떤 영역이 가장 가까운지, 어떤 영역이 가장 먼지 해석
# disparity가 클수록 가까움
closest_by_disp = max(results.items(), key=lambda x: x[1]["mean_disparity"])
farthest_by_disp = min(results.items(), key=lambda x: x[1]["mean_disparity"])

# depth가 작을수록 가까움
closest_by_depth = min(results.items(), key=lambda x: x[1]["mean_depth"])
farthest_by_depth = max(results.items(), key=lambda x: x[1]["mean_depth"])

print()
print("===== 거리 해석 =====")
print(f"Disparity 기준 가장 가까운 ROI : {closest_by_disp[0]}")
print(f"Disparity 기준 가장 먼 ROI    : {farthest_by_disp[0]}")
print(f"Depth 기준 가장 가까운 ROI    : {closest_by_depth[0]}")
print(f"Depth 기준 가장 먼 ROI        : {farthest_by_depth[0]}")

print()
print("===== 결과 해석 =====")
print(f"가장 가까운 ROI : {closest_by_disp[0]}")
print(f"가장 먼 ROI    : {farthest_by_disp[0]}")

# -----------------------------
# 5. disparity 시각화
# 가까울수록 빨강 / 멀수록 파랑
# -----------------------------
disp_tmp = disparity.copy()
disp_tmp[disp_tmp <= 0] = np.nan

if np.all(np.isnan(disp_tmp)):
    raise ValueError("유효한 disparity 값이 없습니다.")

# 5% ~ 95% 범위로 클리핑하여 시각화
d_min = np.nanpercentile(disp_tmp, 5)
d_max = np.nanpercentile(disp_tmp, 95)

# d_max가 d_min보다 작거나 같은 경우를 대비하여 작은 값을 더해줌
if d_max <= d_min:
    d_max = d_min + 1e-6

# disparity 값을 0~1 범위로 정규화
disp_scaled = (disp_tmp - d_min) / (d_max - d_min)
disp_scaled = np.clip(disp_scaled, 0, 1)

# disparity는 클수록 가까운 물체이므로 반전
disp_vis = np.zeros_like(disparity, dtype=np.uint8)
valid_disp = ~np.isnan(disp_tmp)
disp_vis[valid_disp] = (disp_scaled[valid_disp] * 255).astype(np.uint8)

# disparity 시각화
disparity_color = cv2.applyColorMap(disp_vis, cv2.COLORMAP_JET)

# -----------------------------
# 6. depth 시각화
# 가까울수록 빨강 / 멀수록 파랑
# -----------------------------
depth_vis = np.zeros_like(depth_map, dtype=np.uint8)

# depth_map에서 유효한 픽셀만 사용하여 5% ~ 95% 범위로 클리핑하여 시각화
if np.any(valid_mask):
    depth_valid = depth_map[valid_mask]

    z_min = np.percentile(depth_valid, 5)
    z_max = np.percentile(depth_valid, 95)

    if z_max <= z_min:
        z_max = z_min + 1e-6

    depth_scaled = (depth_map - z_min) / (z_max - z_min)
    depth_scaled = np.clip(depth_scaled, 0, 1)

    # depth는 클수록 멀기 때문에 반전
    depth_scaled = 1.0 - depth_scaled
    depth_vis[valid_mask] = (depth_scaled[valid_mask] * 255).astype(np.uint8)

depth_color = cv2.applyColorMap(depth_vis, cv2.COLORMAP_JET)

# -----------------------------
# 7. Left / Right 이미지에 ROI 표시
# -----------------------------
left_vis = left_color.copy()
right_vis = right_color.copy()

# 각 ROI에 대해 사각형과 텍스트로 표시
for name, (x, y, w, h) in rois.items():
    cv2.rectangle(left_vis, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(left_vis, name, (x, y - 8),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.rectangle(right_vis, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(right_vis, name, (x, y - 8),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

# -----------------------------
# 8. 저장
# -----------------------------
cv2.imwrite(str(output_dir / "left_with_roi.png"), left_vis)
cv2.imwrite(str(output_dir / "right_with_roi.png"), right_vis)
cv2.imwrite(str(output_dir / "disparity_map_color.png"), disparity_color)
cv2.imwrite(str(output_dir / "depth_map_color.png"), depth_color)

# -----------------------------
# 9. 출력
# -----------------------------
cv2.imshow("Left with ROI", left_vis)
cv2.imshow("Right with ROI", right_vis)
cv2.imshow("Disparity Map", disparity_color)
cv2.imshow("Depth Map", depth_color)

cv2.waitKey(0)
cv2.destroyAllWindows()
