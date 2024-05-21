import pathlib
import torch
import cv2
import platform

# 실행 플랫폼 체크
system_platform = platform.system()
print(f'system platform = {system_platform}')
if system_platform in ['Linux', 'Darwin', 'Unix']:
    pathlib.WindowsPath = pathlib.PosixPath

model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', force_reload=True)
# 웹캠 캡처
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break
    
    # 이미지 전처리
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # 모델에 이미지 전달 및 추론 수행
    results = model(img_rgb)
    
    # 결과를 이미지 위에 그리기
    if len(results.xyxy[0]) > 0:  # 감지된 객체가 있는 경우
        annotated_img = results.render()[0]
        annotated_img = cv2.cvtColor(annotated_img, cv2.COLOR_RGB2BGR)
        
        # 콘솔에 로그 출력
        for *box, conf, cls in results.xyxy[0]:
            print(f'Class: {int(cls)}, Confidence: {conf:.2f}, Box: {box}')
        
        # 결과 이미지 표시
        cv2.imshow('Detection', annotated_img)
    else:
        print("No detections")
        cv2.imshow('Detection', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 리소스 해제
cap.release()
cv2.destroyAllWindows()
