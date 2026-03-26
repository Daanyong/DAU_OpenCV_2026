# SIFT를 이용한 특징점 검출 및 시각화
# 주어진 이미지를 이용하여 SIFT 알고리즘을 사용하여 특징점을 검출하고 이를 시각화

import cv2 as cv
import matplotlib.pyplot as plt

img = cv.imread('mot_color70.jpg')

# cv.SIFT_create()를 사용하여 SIFT 객체를 생성
sift = cv.SIFT_create()

# detectAndCompute()를 사용하여 특징점을 검출
kp, des = sift.detectAndCompute(img, None)

# cv.drawKeypoints()를 사용하여 특징점을 이미지에 시각화
img_keypoints = cv.drawKeypoints(img, kp, None, flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# matplotlib을 이용하여 원본 이미지와 특징점이 시각화된 이미지를 나란히 출력
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
plt.title('Original Image')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(cv.cvtColor(img_keypoints, cv.COLOR_BGR2RGB))
plt.title('SIFT Keypoints')
plt.axis('off')

plt.show()