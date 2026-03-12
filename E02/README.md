# L02. Image Formation

  ## 01. 체크보드 기반 카메라 캘리브레이션
  이미지에서 체크보드 코너를 검출하고 실제 좌표와 이미지 좌표의 대응 관계를 이용하여 카메라 파라미터 추정
  
  체크보드 패턴이 촬영된 여러 장의 이미지를 이용하여 카메라의 내부 행렬과 왜곡 계수를 계산하여 왜곡 보정
  <details>
    <summary>전체 코드</summary>
    
    # 체크보드 기반 카메라 캘리브레이션
# 이미지에서 체크보드 코너를 검출하고 실제 좌표와 이미지 좌표의 대응 관계를 이용하여 카메라 파라미터 추정
# 체크보드 패턴이 촬영된 여러 장의 이미지를 이용하여 카메라의 내부 행렬과 왜곡 계수를 계산하여 왜곡 보정

import cv2
import numpy as np
import glob

# 체크보드 내부 코너 개수
CHECKERBOARD = (9, 6)

# 체크보드 한 칸 실제 크기 (mm)
# 실제 좌표는 모든 이미지에서 동일한 격자 구조를 가짐 (한 칸의 실제 크기: 25mm)
square_size = 25.0

# 코너 정밀화 조건
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001) # 코너 정밀화 반복 조건 (최대 30회 또는 0.001 픽셀 이하의 이동)

# 실제 좌표 생성
# 요구사항 2: 체크보드의 실제 좌표와 이미지에서 찾은 코너 좌표를 구성
objp = np.zeros((CHECKERBOARD[0]*CHECKERBOARD[1], 3), np.float32) # (9*6, 3) 크기의 배열 생성
objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2) # (0,0), (1,0), ..., (8,5) 형태로 좌표 생성
objp *= square_size # 실제 크기 적용 (mm 단위)

# 저장할 좌표
objpoints = []
imgpoints = []

# 이미지 파일 경로
images = glob.glob("../images/calibration_images/left*.jpg")
img_size = None

# -----------------------------
# 1. 체크보드 코너 검출
# -----------------------------

# 요구사항 1: 모든 이미지에서 체크보드 코너를 검출
for fname in images:
    img = cv2.imread(fname) # 이미지 읽기
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # 그레이스케일로 변환 (코너 검출을 위해)

    img_size = gray.shape[::-1] # 이미지 크기 저장 (너비, 높이) - 캘리브레이션 함수에서 필요

    # 체크보드 코너 검출은 cv2.findChessboardCorners() 사용
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)

    # 검출된 코너가 있으면 정밀화하여 저장
    if ret:
        corners2 = cv2.cornerSubPix(
            gray,
            corners,
            (11,11),
            (-1,-1),
            criteria
        )

        # 3D 실제 좌표와 2D 이미지 좌표를 저장
        objpoints.append(objp)
        imgpoints.append(corners2)
    
    # -----------------------------
    # 2. 카메라 캘리브레이션
    # -----------------------------
    
    # 요구사항 3: cv2.calibrateCamera()를 사용하여 카메라 내부 행렬 k와 왜곡 계수를 구함
    ret, K, dist, rvecs, tvecs = cv2.calibrateCamera(
        objpoints,
        imgpoints,
        img_size,
        None,
        None
    )
    
    # 결과 출력
    print("Camera Matrix K:")
    print(K)
    
    print("\nDistortion Coefficients:")
    print(dist)
    
    # -----------------------------
    # 3. 왜곡 보정 시각화
    # -----------------------------
    img = cv2.imread(images[0]) # 첫 번째 이미지 읽기
    
    h, w = img.shape[:2] # 이미지 크기 (높이, 너비) - 왜곡 보정 함수에서 필요
    
    # 왜곡 보정 시 이미지 손실을 최소화하도록 새로운 카메라 행렬과 ROI 계산
    new_K, roi = cv2.getOptimalNewCameraMatrix(K, dist, (w,h), 1, (w,h))
    
    # 요구사항 4: cv2.undistort()를 사용하여 왜곡 보정한 결과를 시각화
    undistorted = cv2.undistort(img, K, dist, None, new_K)
    
    comparison = np.hstack((img, undistorted))
    
    cv2.imshow("Original vs Undistorted", comparison)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
  </details>
  
  #### 요구사항 1: 모든 이미지에서 체크보드 코너를 검출
  #### 요구사항 2: 체크보드의 실제 좌표와 이미지에서 찾은 코너 좌표를 구성
    for fname in images:
    img = cv2.imread(fname) # 이미지 읽기
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # 그레이스케일로 변환 (코너 검출을 위해)

    img_size = gray.shape[::-1] # 이미지 크기 저장 (너비, 높이) - 캘리브레이션 함수에서 필요

    # 체크보드 코너 검출은 cv2.findChessboardCorners() 사용
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)

    # 검출된 코너가 있으면 정밀화하여 저장
    if ret:
        corners2 = cv2.cornerSubPix(
            gray,
            corners,
            (11,11),
            (-1,-1),
            criteria
        )

        # 3D 실제 좌표와 2D 이미지 좌표를 저장
        objpoints.append(objp)
        imgpoints.append(corners2)
  #### 요구사항 3: cv2.calibrateCamera()를 사용하여 카메라 내부 행렬 k와 왜곡 계수를 구함
    ret, K, dist, rvecs, tvecs = cv2.calibrateCamera(
    objpoints,
    imgpoints,
    img_size,
    None,
    None
    )
  #### 요구사항 4: cv2.undistort()를 사용하여 왜곡 보정한 결과를 시각화
    undistorted = cv2.undistort(img, K, dist, None, new_K)
  #### 결과화면
<img width="953" height="383" alt="image" src="https://github.com/user-attachments/assets/abf6962a-0be1-4bb4-b04e-e83fb4b09a54" />

---
  ## 02. 이미지 Rotation & Transformation
  한 장의 이미지에 회전, 크기 조절, 평행이동을 적용
  <details>
    <summary>전체 코드</summary>
    # 이미지 Rotation & Transformation
    # 한 장의 이미지에 회전, 크기 조절, 평행이동을 적용
    import cv2
    import numpy as np
    import matplotlib.pyplot as plt
    
    # 이미지 불러오기
    image = cv2.imread("../images/rose.png")
    
    if image is None:
        raise FileNotFoundError("파일이 존재하지 않습니다.")
    
    rows, cols = image.shape[:2]
    
    # 변환 조건
    angle = 30          # +30도 회전
    scale = 0.8         # 0.8배 축소
    tx = 40             # x축 +40px 이동
    ty = -20            # y축 -20px 이동
    
    # 요구사항 1: 이미지의 중심 기준으로 +30도 회전
    # 요구사항 2: 회전과 동시에 크기를 0.8로 조절
    # 회전 행렬은 cv2.getRotationMatrix2D()로 생성 가능
    rotation_matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, scale)
    
    # 요구사항 3: 그 결과를 x축 방향으로 +80px, y축 방향으로 -40px만큼 평행이동
    # 평행이동은 회전 행렬의 마지막 열 값을 조정하는 방식으로 반영
    rotation_matrix[0, 2] += tx
    rotation_matrix[1, 2] += ty
    
    # 회전, 크기 조절, 평행이동은 cv2.warpAffine()로 적용
    transformed_image = cv2.warpAffine(
        image,
        rotation_matrix,
        (cols, rows),
        flags=cv2.INTER_LINEAR
    )
    
    plt.figure(figsize=(10, 5))
    
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title("Original Image")
    plt.axis("off")
    
    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(transformed_image, cv2.COLOR_BGR2RGB))
    plt.title("Rotated + Scaled + Translated")
    plt.axis("off")
    
    plt.tight_layout()
    plt.show()
  </details>
  
  #### 요구사항 1: 이미지의 중심 기준으로 +30도 회전
  #### 요구사항 2: 회전과 동시에 크기를 0.8로 조절
    angle = 30
    scale = 0.8
    
    rotation_matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, scale)
  #### 요구사항 3: 그 결과를 x축 방향으로 +80px, y축 방향으로 -40px만큼 평행이동
    tx = 40
    ty = -20
    rotation_matrix[0, 2] += tx
    rotation_matrix[1, 2] += ty
    
    transformed_image = cv2.warpAffine(
        image,
        rotation_matrix,
        (cols, rows),
        flags=cv2.INTER_LINEAR
    )
  #### 결과화면
 <img width="740" height="272" alt="image" src="https://github.com/user-attachments/assets/bcea3954-b67d-4d4e-863e-c7b169bda1b3" />

---
  ## 03. Stereo Disparity 기반 Depth 추정
  같은 장면을 왼쪽 카메라와 오른쪽 카메라에서 촬영한 두 장의 이미지를 이용해 깊이를 추정

  두 이미지에서 같은 물체가 얼마나 옆으로 이동해 보이는지 계산하여 물체가 카메라에서 얼마나 떨어져 있는지(depth)를 구할 수 있음

  Disparity: Left 이미지와 right 이미지에서 같은 물체의 픽셀 위치 차이, 값이 클 수록 가까운 물체

  Depth: Disparity를 이용하면 물체의 실제 거리 정보를 계산할 수 있음, 값이 작을 수록 가까운 물체
  <details>
    <summary>전체 코드</summary>
    
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
        print(f"  Mean Disparity : {result['mean_disparity']:.4f}")
        print(f"  Mean Depth     : {result['mean_depth']:.4f}")
    
    # 요구사항 4: 세 ROI 중 어떤 영역이 가장 가까운지, 어떤 영역이 가장 먼지 해석
    closest_roi = max(results.items(), key=lambda x: x[1]["mean_disparity"])[0]
    farthest_roi = max(results.items(), key=lambda x: x[1]["mean_depth"])[0]
    
    print("===== 거리 해석 =====")
    print(f"가장 가까운 ROI: {closest_roi}")
    print(f"가장 먼 ROI: {farthest_roi}")
    
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
  </details>
  
  #### 요구사항 1: 입력 이미지를 그레이스케일로 변환하고 cv2.StereoBM_create()를 사용하여 disparity map 계산
    left_gray = cv2.cvtColor(left_color, cv2.COLOR_BGR2GRAY)
    right_gray = cv2.cvtColor(right_color, cv2.COLOR_BGR2GRAY)

    stereo = cv2.StereoBM_create(numDisparities=96, blockSize=15)

    disparity = stereo.compute(left_gray, right_gray).astype(np.float32) / 16.0
  #### 요구사항 2: Disparity > 0인 픽셀만 사용하여 depth map 계산
    depth_map = np.zeros_like(disparity, dtype=np.float32)
    valid_mask = disparity > 0
  #### 요구사항 3: ROI Painting, Frog, Teddy 각각에 대해 평균 disparity와 평균 depth를 계산
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
   #### 요구사항 4: 세 ROI 중 어떤 영역이 가장 가까운지, 어떤 영역이 가장 먼지 해석
    closest_roi = max(results.items(), key=lambda x: x[1]["mean_disparity"])[0]
    farthest_roi = max(results.items(), key=lambda x: x[1]["mean_depth"])[0]
  #### 결과화면
<img width="673" height="608" alt="p3_Result" src="https://github.com/user-attachments/assets/c499cfa3-48d7-4261-9288-0aa3663e7e61" />
<img width="227" height="167" alt="image" src="https://github.com/user-attachments/assets/bb730b11-e562-46c1-8f5f-cc633c00f7b6" />
