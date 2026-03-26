# 호모그래피를 이용한 이미지 정합
# SIFT 특징점을 사용하여 두 이미지 간 대응점을 찾고, 이를 바탕으로 호모그래피를 계산하여 하나의 이미지 위에 정렬

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# cv.imread()를 사용하여 두 개의 이미지를 불러옴
img1 = cv.imread('img1.jpg')
img2 = cv.imread('img2.jpg')

# cv.SIFT_create()를 사용하여 특징점을 검출
sift = cv.SIFT_create()
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)

# cv.BFMatcher()를 사용하여 특징점을 매칭하고, 좋은 매칭점만 선별
bf = cv.BFMatcher()
matches = bf.knnMatch(des1, des2, k=2)

good = []
for m, n in matches:
    if m.distance < 0.75 * n.distance:
        good.append(m)

matched_img = cv.drawMatches(img1, kp1, img2, kp2, good, None, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

# cv.findHomography()를 사용하여 호모그래피 행렬을 계산
src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1,1,2)
dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1,1,2)

M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5.0)

# cv.warpPerspective()를 사용하여 한 이미지를 변환하여 다른 이미지와 정렬
h1, w1 = img1.shape[:2]
h2, w2 = img2.shape[:2]

corners1 = np.float32([[0,0],[w1,0],[w1,h1],[0,h1]]).reshape(-1,1,2)
corners2 = np.float32([[0,0],[w2,0],[w2,h2],[0,h2]]).reshape(-1,1,2)

transformed_corners1 = cv.perspectiveTransform(corners1, M)
all_corners = np.concatenate((transformed_corners1, corners2), axis=0)
x_min, y_min = np.int32(all_corners.min(axis=0).ravel())
x_max, y_max = np.int32(all_corners.max(axis=0).ravel())
translation_dist = [-x_min, -y_min]
H_translation = np.array([[1,0,translation_dist[0]],[0,1,translation_dist[1]],[0,0,1]], dtype=np.float32)
stitched_width = x_max - x_min
stitched_height = y_max - y_min

result = cv.warpPerspective(img1, H_translation.dot(M), (stitched_width, stitched_height))
result[translation_dist[1]:translation_dist[1]+h2, translation_dist[0]:translation_dist[0]+w2] = img2

# 변환된 이미지와 특징점 매칭 결과를 나란히 출력
plt.figure(figsize=(12, 6))
plt.subplot(1, 4, 1)
plt.imshow(cv.cvtColor(img1, cv.COLOR_BGR2RGB))
plt.title("Original Image")
plt.axis('off')

plt.subplot(1, 4, 2)
plt.imshow(cv.cvtColor(img2, cv.COLOR_BGR2RGB))
plt.title("Target Image")
plt.axis('off')

plt.subplot(1, 4, 3)
plt.imshow(cv.cvtColor(result, cv.COLOR_BGR2RGB))
plt.title("Aligned Image")
plt.axis('off')

plt.subplot(1, 4, 4)
plt.imshow(cv.cvtColor(matched_img, cv.COLOR_BGR2RGB))
plt.title('Matched Points')
plt.axis('off')

plt.show()