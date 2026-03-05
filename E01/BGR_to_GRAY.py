# 이미지 불러오기 및 그레이스케일 변환
# OpenCV를 사용하여 이미지를 불러오고 화면에 출력
# 원본 이미지와 그레이스케일로 변환된 이미지를 나란히 표시

import cv2 as cv
import sys
import numpy as np
import matplotlib.pyplot as plt

# 요구사항 1: cv.imread()를 사용하여 이미지 로드
img = cv.imread('soccer.jpg')

if img is None:
    sys.exit('파일이 존재하지 않습니다.')

# 요구사항 2: cv.cvtColor() 함수를 사용해 이미지를 그레이스케일로 변환
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)


# 요구사항 3: np.hstack() 함수를 이용해 원본 이미지와 그레이스케일 이미지를 가로로 연결하여 출력
imgs = np.hstack((img, cv.cvtColor(gray, cv.COLOR_GRAY2BGR)))

# 요구사항 4: cv.imshow()와 cv.waitKey()를 사용해 결과를 화면에 표시하고, 아무 키나 누르면 창이 닫히도록 할 것
plt.imshow(cv.cvtColor(imgs, cv.COLOR_BGR2RGB))
plt.axis('off')
plt.show()

cv.waitKey(0)
cv.destroyAllWindows()