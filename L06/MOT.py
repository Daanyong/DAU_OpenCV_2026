# SORT 알고리즘을 활용한 다중 객체 추적기 구현
# 이 실습에서는 SORT 알고리즘을 사용하여 비디오에서 다중 객체를 실시간으로 추적하는 프로그램을 구현합니다.
# 이를 통해 객체 추적의 기본 개념과 SORT 알고리즘의 적용 방법을 학습할 수 있습니다.

import numpy as np
import cv2 as cv
import sys
from sort.sort import Sort

# 요구사항 1: 객체 검출기 구현: YOLOv3와 같은 사전 훈련된 객체 검출 모델을 사용하여 각 프레임에서 객체를 검출합니다
def construct_yolo_v3():
    with open('coco_names.txt', 'r', encoding='utf-8') as f:
        class_names = [line.strip() for line in f.readlines()]

    model = cv.dnn.readNet('yolov3.weights', 'yolov3.cfg')
    layer_names = model.getLayerNames()
    output_layers = [layer_names[i - 1] for i in model.getUnconnectedOutLayers().flatten()]

    return model, output_layers, class_names

def yolo_detect(img, yolo_model, out_layers):
    height, width = img.shape[:2]
    blob = cv.dnn.blobFromImage(
        img, 1 / 255.0, (416, 416), (0, 0, 0),
        swapRB=True, crop=False
    )

    yolo_model.setInput(blob)
    outputs = yolo_model.forward(out_layers)

    boxes = []
    confidences = []
    class_ids = []

    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5:
                center_x, center_y, w, h = (
                    detection[0:4] * np.array([width, height, width, height])
                ).astype(int)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indices = cv.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    objects = []
    if len(indices) > 0:
        for i in indices.flatten():
            x, y, w, h = boxes[i]
            objects.append([x, y, x + w, y + h, confidences[i], class_ids[i]])

    return objects

model, out_layers, class_names = construct_yolo_v3()
colors = np.random.uniform(0, 255, size=(100, 3))

# 요구사항 2: mathworks.comSORT 추적기 초기화: 검출된 객체의 경계 상자를 입력으로 받아 SORT 추적기를 초기화합니다
tracker = Sort()

cap = cv.VideoCapture('slow_traffic_small.mp4')
if not cap.isOpened():
    print("비디오 파일을 열 수 없습니다.")
    sys.exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("비디오 재생이 종료되었거나 프레임을 읽을 수 없습니다.")
        break

    objects = yolo_detect(frame, model, out_layers)

    dets_for_sort = []
    for obj in objects:
        # obj = [x1, y1, x2, y2, confidence, class_id]
        dets_for_sort.append(obj[:5])

    dets_for_sort = np.array(dets_for_sort) if len(dets_for_sort) > 0 else np.empty((0, 5))
    
    # 요구사항 3: 객체 추적: 각 프레임마다 검출된 객체와 기존 추적 객체를 연관시켜 추적을 유지합니다
    tracks = tracker.update(dets_for_sort)

    # 요구사항 4: 결과 시각화: 추적된 각 객체에 고유 ID를 부여하고, 해당 ID와 경계 상자를 비디오 프레임에 표시하여 실시간으로 출력합니다
    for d in tracks:
        x1, y1, x2, y2, track_id = d
        x1, y1, x2, y2, track_id = int(x1), int(y1), int(x2), int(y2), int(track_id)

        color = colors[track_id % 100]
        color = tuple(map(int, color))

        cv.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv.putText(frame, f"ID: {track_id}", (x1, y1 - 5),
                   cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    cv.imshow("Multi-Object Tracking", frame)

    if cv.waitKey(30) & 0xFF == 27:
        break

cap.release()
cv.destroyAllWindows()