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