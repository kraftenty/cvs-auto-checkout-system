import pathlib
import torch
import cv2
import platform
import time
from flask_socketio import SocketIO, emit

socketio = None  # SocketIO 인스턴스

def init_socketio(app):
    global socketio
    socketio = SocketIO(app)

def detection():
    checkRunningPlatform()
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', force_reload=True)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("[ERROR] Could not open webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to grab frame.")
            break

        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = model(img_rgb)

        if len(results.xyxy[0]) > 0:
            annotated_img = results.render()[0]
            annotated_img = cv2.cvtColor(annotated_img, cv2.COLOR_RGB2BGR)

            for *box, conf, cls in results.xyxy[0]:
                product_info = {
                    'class': int(cls),
                    'confidence': round(float(conf), 2),
                    'box': [round(float(coord), 2) for coord in box]
                }
                # 웹소켓을 통해 감지 결과 전송
                socketio.emit('new_product', product_info)

            cv2.imshow('Detection', annotated_img)
        else:
            cv2.imshow('Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.2)

    cap.release()
    cv2.destroyAllWindows()

def checkRunningPlatform():
    system_platform = platform.system()
    if system_platform in ['Linux', 'Darwin', 'Unix']:
        pathlib.WindowsPath = pathlib.PosixPath
        print('[INFO] UNIX 계열 OS에서 실행을 시작합니다.')
    else:
        print('[INFO] WINDOWS에서 실행을 시작합니다.')
