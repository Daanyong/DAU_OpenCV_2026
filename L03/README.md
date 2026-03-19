# L03. Edge and Region

  ## 01. 소벨 에지 검출 및 결과 시각화
  edgeDetectionImage 이미지를 그레이스케일로 변환
  
  Sobel 필터를 사용하여 X축과 Y축의 방향의 에지를 검출

  검출된 에지 강도 이미지를 시각화
  <details>
    <summary>전체 코드</summary>
    
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
  </details>
  
  #### 요구사항 1: cv.imread()를 사용하여 이미지를 불러옴
    img = cv.imread('edgeDetectionImage.jpg')
  #### 요구사항 2: cv.cvtColor()를 사용하여 그레이스케일로 변환
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
  #### 요구사항  3: cv.Sobel()을 사용하여 X축(cv.CV_64F, 1, 0)과 Y축(cv.CV_64F, 0, 1) 방향의 에지를 검출
    grad_x = cv.Sobel(gray, cv.CV_64F, 1, 0, ksize=3)
    grad_Y = cv.Sobel(gray, cv.CV_64F, 0, 1, ksize=3)
  #### 요구사항 4: cv.magnitude()를 사용하여 에지 강도 계산
    edge_strength = cv.magnitude(grad_x, grad_Y)
  #### 결과화면
<img width="739" height="227" alt="image" src="https://github.com/user-attachments/assets/78c3b3a7-d6b6-42f1-a00e-517d2f898158" />

---
  ## 02. 캐니 에지 및 허프 변환을 이용한 직선 검출
  dabo 이미지에 캐니 에지 검출을 사용하여 에지 맵 생성
  
  허프 변환을 사용하여 이미지에서 직선을 검출
  
  검출된 직선을 원본 이미지에 빨간색으로 표시
  <details>
    <summary>전체 코드</summary>
    
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
  </details>
  
  #### 요구사항 1: cv.Canny()를 사용하여 에지 맵 생성
    canny = cv.Canny(gray, 100, 200)
  #### 요구사항 2: cv.HoughLinesP()를 사용하여 직선 검출
    lines = cv.HoughLinesP(canny, rho=1, theta=3.14/180, threshold=100, minLineLength=50, maxLineGap=10)
  #### 요구사항 3: cv.line()을 사용하여 검출된 직선을 원본 이미지에 그림
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
  #### 요구사항4: Matplotlib를 사용하여 원본 이미지와 직선이 그려진 이미지를 나란히 시각화
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
  #### 결과화면
<img width="736" height="292" alt="image" src="https://github.com/user-attachments/assets/c1d1171c-c8a6-436b-ba5d-58bf8bd442f7" />

---
  ## 03. GrabCut을 이용한 대화식 영역 분할 및 객체 추출
  coffee cup 이미지로 사용자가 지정한 사각형 영역을 바탕으로 GrabCut 알고리즘을 사용하여 객체 추출

  객체 추출 결과를 마스크 형태로 시각화합니다

  원본 이미지에서 배경을 제거하고 객체만 남은 이미지를 출력합니다
  <details>
    <summary>전체 코드</summary>
    
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
   
  </details>
  
  #### 요구사항 1: cv.grabCut()를 사용하여 대화식 분할을 수행
  #### 요구사항 2: 초기 사각형 영역은 (x, y, width, height) 형식으로 설정
  #### 힌트 1: cv.grabCut()에서 bgdModel과 fgdModel은 np.zeros((1, 65), np.float64)로 초기화
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    
    rect = (90, 80, 1000, 800)

    cv.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv.GC_INIT_WITH_RECT)
  #### 요구사항 2: cv.setMouseCallback()을 사용하여 마우스 이벤트를 처리
    cv.setMouseCallback('Drawing', draw)
  #### 요구사항 3: 마스크를 사용하여 원본 이미지에서 배경을 제거
  #### 힌트 2: 마스크값은 cv.GC_BGD, cv.GC_FGD, cv.GC_PR_BGD, cv.GC_PR_FGD를 사용
  #### 힌트 3: np.where()를 사용하여 마스크 값을 0 또는 1로 변경한 후 원본 이미지에 곱하여 배경을 제거
    mask2 = np.where((mask == cv.GC_FGD) | (mask == cv.GC_PR_FGD), 1, 0).astype('uint8')
    result = img * mask2[:, :, np.newaxis]
  #### 요구사항4: matplotlib를 사용하여 원본이미지, 마스크이미지, 배경 제거 이미지 세 개를 나란히 시각화합니다
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
  #### 결과화면
  <img width="1115" height="294" alt="image" src="https://github.com/user-attachments/assets/7b49e7ba-f998-4146-838e-6a901c76843e" />
