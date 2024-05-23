# 편의점 자동 계산 시스템

* 실시간으로 계산대 위의 물건을 카메라로 인식하여 자동으로 계산해 주는 시스템입니다.
<iframe width="560" height="315" src="https://www.youtube.com/embed/2-c_4o9W3u0?si=X86wzD11d4LFIfPo" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## Contents
- [Preparation](#preparation)
- [How To Use](#how-to-use)
- [Detail](#detail)
- [References](#references)
- [License](#license)
---

## Preparation
> 0. `$ git clone https://github.com/kraftenty/cvs-auto-checkout-system.git` 로 다운로드 받은 다음 해당 디렉토리로 이동하세요.
>
> 1. `requirements.txt` 파일에 적혀 있는 파이썬 라이브러리를 pip 등을 통해 설치하세요.  
>     `$ pip install -r requirements.txt` 명령어로 한 번에 설치할 수도 있습니다.
>
> 2. `$ python app.py` 명령어로 애플리케이션을 실행하세요.


---
## How To Use



---
## Detail
> System Environment  
> CPU : Ryzen R5 5600G  
> MEM : 32GB Memory  
> GPU : RTX 4060 - 8GB VRAM  
  
> Model Training   
> 
> 우선 이미지 학습을 위해 총 1,738장의 사진을 찍었습니다. (8개 클래스)  
> 클래스의 종류는 다음과 같습니다.  
> `코카콜라`, `칠성사이다`, `레쓰비`, `칸쵸`, `빼빼로`, `고소미`, `스니커즈`, `짜파게티`  
> ![detail_0](static/images/detail_0.png)
>  
> 그 다음, `labelImg`를 이용하여 이미지들을 라벨링합니다.   
> ![detail_1](static/images/detail_1.png)
>  
> 라벨링한 이미지들과 텍스트 파일들을 train 80%, validation 15%, test 5% 비율로 분할하고, YOLOv5를 이용하여 학습을 돌립니다.  
> Epoch = 120회, 이미지 크기 = 640*640, batch = 16, model = yolo5L
> ![detail_2](static/images/detail_2.png)
> ![detail_3](static/images/detail_3.png)

> How System Works  
> ![detail_4](static/images/detail_4.png)
> 1. 손님이 물건을 계산대 위에 올려놓고, Client Screen의 계산 시작하기 버튼을 누릅니다.
> 2. PyTorch가 미리 학습된 모델 파일을 로드합니다. 
> 3. 카메라가 OpenCV를 통해 계산대 위를 계속해서 찍습니다.
> 4. YOLOv5가 입력되는 프레임에서 객체를 탐지합니다.
> 5. 탐지된 객체는 Socket 통신을 통해 WAS에서 처리하여 실시간으로 Client Screen에 목록으로 표시됩니다.
> 6. 손님이 Client Screen에서 결제 수단을 고르고 결제 버튼을 누르면, DB에 결제 시간과 금액, 그리고 결제 수단이 저장됩니다.


---
## References
- ChatGPT 4.0o
- Github Copilot
- YOLOv5  (https://github.com/ultralytics/yolov5)
---
## License
- MIT License
- Made by `Ko Kyeong Tae` ( `kraftenty` )
- If you have questions, feel free to email `kraftenty@gmail.com`.