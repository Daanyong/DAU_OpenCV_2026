# 페인팅 붓 크기 조절 기능 추가
# 마우스 입력으로 이미지 위에 붓질
# 키보드 입력을 이용해 붓의 크기를 조절하는 기능 추가

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