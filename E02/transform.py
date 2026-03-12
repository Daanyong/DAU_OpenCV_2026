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