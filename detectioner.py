import pathlib
import torch
import cv2
import platform
import time
from flask_socketio import SocketIO, emit
import threading

import properties

socketio = None  # SocketIO 인스턴스
stop_event = threading.Event()  # Event 객체 생성

item_list = [False for _ in range(8)]

def init_socketio(app):
    global socketio
    socketio = SocketIO(app)

def detection(stop_event):
    checkRunningPlatform()
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', force_reload=False)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("[ERROR] Could not open webcam.")
        return

    while not stop_event.is_set():
        print('loop 도는 중....')
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to grab frame.")
            break

        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = model(img_rgb)

        if len(results.xyxy[0]) > 0:
            annotated_img = results.render()[0]
            annotated_img = cv2.cvtColor(annotated_img, cv2.COLOR_RGB2BGR)
            print(results.xyxy[0])

            classes = { 0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}
            for *box, conf, cls in results.xyxy[0]:
                classes[int(cls)] += 1
            
            # classes 딕셔너리를 순회하면서, value가 1 이상인 아이템을 item 객체로 만들고 웹소켓을 통해 감지 결과 전송한다.
            for key, value in classes.items():
                if value > 0:
                    if item_list[key]:
                        continue
                    item_list[key] = True
                    item = {
                        'id': key,
                        'name': properties.getItemName(key),
                        'price': properties.getItemPrice(key),
                        'quantity': value
                    }
                    socketio.emit('item', item)

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

def stop_detection():
    print('[INFO] detection stopped.')
    stop_event.set() 

def restart_detection():
    print('[INFO] detection restarted.')
    # 아이템 리스트 초기화
    global item_list
    item_list = [False for _ in range(8)]
    stop_event.clear()
