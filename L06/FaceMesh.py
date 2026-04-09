# Mediapipe를 활용한 얼굴 랜드마크 추출 및 시각화
# Mediapipe의 FaceMesh 모듈을 사용하여 얼굴의 486개 랜드마크를 추출하고, 이를 실시간 영상에 시각화하는 프로그램을 구현합니다

import cv2
import mediapipe as mp

# 요구사항 1: Mediapipe의 FaceMesh 모듈을 사용하여 얼굴 랜드마크 검출기를 초기화합니다
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# 요구사항 2: OpenCV를 사용하여 웹캠으로부터 실시간 영상을 캡처합니다
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 요구사항 3: 검출된 얼굴 랜드마크를 실시간 영상에 점으로 표시합니다
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        for landmarks in results.multi_face_landmarks:
            for lm in landmarks.landmark:
                ih, iw, ic = frame.shape
                x, y = int(lm.x * iw), int(lm.y * ih)
                cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

    cv2.imshow("Mediapipe FaceMesh", frame)

    # 요구사항 4: ESC 키를 누르면 프로그램이 종료되도록 설정합니다.
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()