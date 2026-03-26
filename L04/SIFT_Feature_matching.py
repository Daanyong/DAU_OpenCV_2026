# SIFT를 이용한 두 영상 간 특징점 매칭
# 두 개의 이미지를 입력받아 SIFT 특징점 기반으로 매칭을 수행하고 결과를 시각화

import cv2 as cv
import matplotlib.pyplot as plt

# cv.imread()를 사용하여 두 개의 이미지를 불러옴
img1 = cv.imread('mot_color70.jpg')
img2 = cv.imread('mot_color83.jpg')

# cv.SIFT_create()를 사용하여 특징점을 추출
sift = cv.SIFT_create()
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)

# cv.BFMatcher() 또는 cv.FlannBasedMatcher()를 사용하여 두 영상 간 특징점을 매칭
bf = cv.BFMatcher(cv.NORM_L2)
matches = bf.knnMatch(des1, des2, k=2)

good_matches = []
for m, n in matches:
    if m.distance < 0.75 * n.distance:
        good_matches.append(m)

# cv.drawMatches()를 사용하여 매칭 결과를 시각화
matched_img = cv.drawMatches(
    img1, kp1,
    img2, kp2,
    good_matches[:20],
    None,
    flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
)
# matplotlib을 이용하여 매칭 결과를 출력
plt.figure(figsize=(12, 6))
plt.imshow(cv.cvtColor(matched_img, cv.COLOR_BGR2RGB))
plt.title('SIFT Feature Matching')
plt.axis('off')
plt.show()