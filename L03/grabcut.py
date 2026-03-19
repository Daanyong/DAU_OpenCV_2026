# GrabCut을 이용한 대화식 영역 분할 및 객체 추출
# coffee cup 이미지로 사용자가 지정한 사각형 영역을 바탕으로 GrabCut 알고리즘을 사용하여 객체 추출
# 객체 추출 결과를 마스크 형태로 시각화합니다
# 원본 이미지에서 배경을 제거하고 객체만 남은 이미지를 출력합니다

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

img = cv.imread('coffee cup.jpg')
mask = np.zeros(img.shape[:2], np.uint8)

# 요구사항1: cv.grabCut()를 사용하여 대화식 분할을 수행
# 요구사항2: 초기 사각형 영역은 (x, y, width, height) 형식으로 설정
# 힌트: cv.grabCut()에서 bgdModel과 fgdModel은 np.zeros((1, 65), np.float64)로 초기화
bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)

rect = (90, 80, 1000, 800)

cv.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv.GC_INIT_WITH_RECT)

# 요구사항3: 마스크를 사용하여 원본 이미지에서 배경을 제거
# 힌트: 마스크값은 cv.GC_BGD, cv.GC_FGD, cv.GC_PR_BGD, cv.GC_PR_FGD를 사용
# 힌트: np.where()를 사용하여 마스크 값을 0 또는 1로 변경한 후 원본 이미지에 곱하여 배경을 제거
mask2 = np.where((mask == cv.GC_FGD) | (mask == cv.GC_PR_FGD), 1, 0).astype('uint8')
result = img * mask2[:, :, np.newaxis]

# 요구사항4: matplotlib를 사용하여 원본이미지, 마스크이미지, 배경 제거 이미지 세 개를 나란히 시각화합니다
plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1)
plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
plt.title('Original Image')
plt.axis('off')

plt.subplot(1, 3, 2)
plt.imshow(mask, cmap='gray')
plt.title('Mask Image')
plt.axis('off')

plt.subplot(1, 3, 3)
plt.imshow(cv.cvtColor(result, cv.COLOR_BGR2RGB))
plt.title('Foreground Only')
plt.axis('off')

plt.tight_layout()
plt.show()