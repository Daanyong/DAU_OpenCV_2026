# 캐니 에지 및 허프 변환을 이용한 직선 검출
# dabo 이미지에 캐니 에지 검출을 사용하여 에지 맵 생성
# 허프 변환을 사용하여 이미지에서 직선을 검출
# 검출된 직선을 원본 이미지에 빨간색으로 표시

import cv2 as cv
import matplotlib.pyplot as plt

img = cv.imread('dabo.jpg')
ori_img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# 요구사항 1: cv.Canny()를 사용하여 에지 맵 생성
canny = cv.Canny(gray, 100, 200)

# 요구사항 2: cv.HoughLinesP()를 사용하여 직선 검출
lines = cv.HoughLinesP(canny, rho=1, theta=3.14/180, threshold=100, minLineLength=50, maxLineGap=10)

# 요구사항3: cv.line()을 사용하여 검출된 직선을 원본 이미지에 그림
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

# 요구사항4: Matplotlib를 사용하여 원본 이미지와 직선이 그려진 이미지를 나란히 시각화
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(ori_img)
plt.title('Original Image')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
plt.title('Detected Lines')
plt.axis('off')

plt.tight_layout()
plt.show()