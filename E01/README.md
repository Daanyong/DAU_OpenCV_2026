# E01. Open CV 실습

  ## 01. 이미지 불러오기 및 그레이스케일 변환
  OpenCV를 사용하여 이미지를 불러오고 화면에 출력
  
  원본 이미지와 그레이스케일로 변환된 이미지를 나란히 표시
  <details>
    <summary>전체 코드</summary>
    
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
  </details>
  
  #### 요구사항 1: cv.imread()를 사용하여 이미지 로드
    img = cv.imread('soccer.jpg')
  #### 요구사항 2: cv.cvtColor() 함수를 사용해 이미지를 그레이스케일로 변환
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
  #### 요구사항 3: np.hstack() 함수를 이용해 원본 이미지와 그레이스케일 이미지를 가로로 연결하여 출력
    imgs = np.hstack((img, cv.cvtColor(gray, cv.COLOR_GRAY2BGR)))
  #### 요구사항 4: cv.imshow()와 cv.waitKey()를 사용해 결과를 화면에 표시하고, 아무 키나 누르면 창이 닫히도록 할 것
    cv.imshow('imgs', imgs)
    cv.waitKey(0)
    cv.destroyAllWindows()
  #### 결과화면
<img width="2157" alt="image" src="https://github.com/user-attachments/assets/60ab6505-0f75-475b-a903-6fb34f70ad01" />

---
  ## 02. 페인팅 붓 크기 조절 기능 추가
  마우스 입력으로 이미지 위에 붓질
  
  키보드 입력을 이용해 붓의 크기를 조절하는 기능 추가
  <details>
    <summary>전체 코드</summary>
    
    import cv2 as cv
    import sys
    
    # 이미지 불러오기
    img = cv.imread('soccer.jpg')
    
    if img is None:
        sys.exit('파일이 존재하지 않습니다.')
    
    # 요구사항 1: 초기 붓 크기는 5를 사용
    brush_size = 5
    
    # 마우스 상태 초기화
    drawing = False
    
    # 마우스 이벤트 처리 함수
    def draw(event, x, y, flags, param):
        global drawing, color, brush_size

    # 요구사항 4: 좌클릭=파란색, 우클릭=빨간색, 드래그로 연속 그리기
    # 좌클릭
    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        color = (255, 0, 0)

    # 우클릭
    elif event == cv.EVENT_RBUTTONDOWN:
        drawing = True
        color = (0,0,255)

    # 드래그로 연속 그리기
    elif event == cv.EVENT_MOUSEMOVE:
        if drawing:
            cv.circle(img, (x, y), brush_size, color, -1)

    # 마우스 버튼 떼면 종료
    elif event == cv.EVENT_LBUTTONUP or event == cv.EVENT_RBUTTONUP:
        drawing = False

    # 윈도우 생성
    cv.namedWindow('painting')
    
    # 마우스 콜백 등록
    cv.setMouseCallback('painting', draw)
    
    while True:
        # 이미지 출력
        cv.imshow('painting', img)

    # 키 입력 받기
    key = cv.waitKey(1)

    # 요구사항 2: + 입력 시 붓 크기 1 증가
    # 요구사항 3: 붓 크기는 최대 15로 제한
    if key == ord('+'):
        brush_size = min(brush_size + 1, 15)

    # 요구사항 2: - 입력 시 붓 크기 1 감소
    # 요구사항 3: 붓 크기는 최소 1로 제한
    elif key == ord('-'):
        brush_size = max(brush_size - 1, 1)

    
    # 요구사항 5: q키를 누르면 영상 창이 종료
    elif key == ord('q'):
        break

    cv.destroyAllWindows()
  </details>
  
  #### 요구사항 1: 초기 붓 크기는 5를 사용
    brush_size = 5
  #### 요구사항 2: + 입력 시 붓 크기 1 증가, - 입력 시 붓 크기 1 감소
  #### 요구사항 3: 붓 크기는 최소 1, 최대 15로 제한
    if key == ord('+'):
        brush_size = min(brush_size + 1, 15)
    elif key == ord('-'):
        brush_size = max(brush_size - 1, 1)
  #### 요구사항 4: 좌클릭=파란색, 우클릭=빨간색, 드래그로 연속 그리기
    # 좌클릭
    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        color = (255, 0, 0)

    # 우클릭
    elif event == cv.EVENT_RBUTTONDOWN:
        drawing = True
        color = (0,0,255)

    # 드래그로 연속 그리기
    elif event == cv.EVENT_MOUSEMOVE:
        if drawing:
            cv.circle(img, (x, y), brush_size, color, -1)

    # 마우스 버튼 떼면 종료
    elif event == cv.EVENT_LBUTTONUP or event == cv.EVENT_RBUTTONUP:
        drawing = False
  #### 결과화면
  <img width="1068" height="727" alt="brush_control" src="https://github.com/user-attachments/assets/6b4f847b-53ba-46ff-81b5-177178652c01" />


---
  ## 03. 마우스로 영역 선택 및 ROI(관심영역) 추출
  이미지를 불러오고 사용자가 마우스로 클릭하고 드래그하여 관심영역(ROI)을 선택

  선택한 영역만 따로 저장하거나 표시
  <details>
    <summary>전체 코드</summary>
    
    import cv2 as cv
    import sys
    import numpy as np
    
    # 요구사항 1: 이미지를 불러옴
    img = cv.imread('soccer.jpg')
    
    if img is None:
        sys.exit('파일이 존재하지 않습니다.')
    
    ix, iy = -1, -1 # 초기 위치
    drawing = False # 클릭 여부
    ROI = None # ROI 초기화
    
    def draw(event, x, y, flags, param):
        global ix, iy, drawing, img, ROI

    # 요구사항 3: 사용자가 클릭한 시작점에서 드래그하여 사각형을 그리며 영역을 선택
    if event == cv.EVENT_LBUTTONDOWN: # 마우스 왼쪽 버튼 클릭했을 때 초기 위치 저장
        drawing = True
        ix, iy = x, y 

    elif event == cv.EVENT_MOUSEMOVE: # 마우스가 이동 중일 때
        if drawing:
            tmp_img = img.copy()
            cv.rectangle(tmp_img, (ix,iy), (x,y), (0,0,255), 2)
            cv.imshow('Drawing', tmp_img)

    # 요구사항 4: 마우스를 놓으면 해당 영역을 잘라내서 별도의 창에 출력
    elif event == cv.EVENT_LBUTTONUP: # 마우스 왼쪽 버튼 클릭했을 때 직사각형 그리기
        drawing = False
        ROI = img[iy:y, ix:x]
        cv.imshow('ROI', ROI)
    
    cv.namedWindow('Drawing')
    
    # 요구사항 2: cv.setMouseCallback()을 사용하여 마우스 이벤트를 처리
    cv.setMouseCallback('Drawing', draw)
    
    while True:
        # 요구사항 1: 불러온 이미지를 화면에 출력
        cv.imshow('Drawing', img)

    # 요구사항 5: r키를 누르면 영역 선택을 리셋하고 처음부터 다시 선택
    if cv.waitKey(1) == ord('r'):
        ROI = None
        cv.destroyWindow("ROI")
        img = cv.imread('soccer.jpg')
        cv.imshow('Drawing', img)

    # 요구사항 6: s키를 누르면 선택한 영역을 이미지 파일로 저장
    elif cv.waitKey(1) == ord('s') and ROI is not None:
        cv.imwrite('ROI.jpg', ROI)
        print('ROI 저장 완료')
    
    elif cv.waitKey(1) == ord('q'):
        break
  </details>
  
  #### 요구사항 1: 이미지를 불러오고 화면에 출력
    img = cv.imread('soccer.jpg')
    if img is None:
        sys.exit('파일이 존재하지 않습니다.')
  #### 요구사항 2: cv.setMouseCallback()을 사용하여 마우스 이벤트를 처리
    cv.setMouseCallback('Drawing', draw)
  #### 요구사항 3: 사용자가 클릭한 시작점에서 드래그하여 사각형을 그리며 영역을 선택
    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y 

    elif event == cv.EVENT_MOUSEMOVE:
        if drawing:
            tmp_img = img.copy()
            cv.rectangle(tmp_img, (ix,iy), (x,y), (0,0,255), 2)
            cv.imshow('Drawing', tmp_img)
  <img width="1065" height="688" alt="image" src="https://github.com/user-attachments/assets/8f2407bc-da99-45a9-8e2e-e5155983d703" />

  #### 요구사항 4: 마우스를 놓으면 해당 영역을 잘라내서 별도의 창에 출력
    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        ROI = img[iy:y, ix:x]
        cv.imshow('ROI', ROI)
  <img width="1062" height="693" alt="image" src="https://github.com/user-attachments/assets/6a5ac705-ac56-438e-b9a5-3b95b1721bb7" />

  #### 요구사항 5: r키를 누르면 영역 선택을 리셋하고 처음부터 다시 선택
    if cv.waitKey(1) == ord('r'):
        ROI = None
        cv.destroyWindow("ROI")
        img = cv.imread('soccer.jpg')
        cv.imshow('Drawing', img)
  #### 요구사항 6: s키를 누르면 선택한 영역을 이미지 파일로 저장
    elif cv.waitKey(1) == ord('s') and ROI is not None:
        cv.imwrite('ROI.jpg', ROI)
        print('ROI 저장 완료')
  <img width="514" height="389" alt="image" src="https://github.com/user-attachments/assets/c9b7e61c-05b2-4e5b-af2a-1fc50e2e4d10" />
