# 마우스로 영역 선택 및 ROI(관심영역) 추출
# 이미지를 불러오고 사용자가 마우스로 클릭하고 드래그하여 관심영역(ROI)을 선택
# 선택한 영역만 따로 저장하거나 표시

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