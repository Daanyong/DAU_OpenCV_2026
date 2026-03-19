# 소벨 에지 검출 및 결과 시각화
# edgeDetectionImage 이미지를 그레이스케일로 변환
# Sobel 필터를 사용하여 X축과 Y축의 방향의 에지를 검출
# 검출된 에지 강도 이미지를 시각화

import cv2 as cv
import matplotlib.pyplot as plt

# 요구사항1: cv.imread()를 사용하여 이미지를 불러옴
img = cv.imread('edgeDetectionImage.jpg')

# 요구사항2: cv.cvtColor()를 사용하여 그레이스케일로 변환
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# 요구사항3: cv.Sobel()을 사용하여 X축(cv.CV_64F, 1, 0)과 Y축(cv.CV_64F, 0, 1) 방향의 에지를 검출
# 힌트 1: cv.Sobel()의 ksize 3 또는 5로 설정
grad_x = cv.Sobel(gray, cv.CV_64F, 1, 0, ksize=3)
grad_Y = cv.Sobel(gray, cv.CV_64F, 0, 1, ksize=3)

# 요구사항4: cv.magnitude()를 사용하여 에지 강도 계산
edge_strength = cv.magnitude(grad_x, grad_Y)
# 힌트 2: cv.convertScaleAbs()를 사용하여 에지 강도 이미지를 unit8로 변환
edge_display = cv.convertScaleAbs(edge_strength)

# 요구사항5: Matplotlib를 사용하여 원본 이미지와 에지 강도 이미지를 나란히 시각화
# 힌트3: plt.imshow()에서 cmap='gray'를 사용하여 흑백으로 시각화
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
plt.title('Original Image')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(edge_display, cmap='gray')
plt.title('Edge Strength Image')
plt.axis('off')

plt.tight_layout()
plt.show()