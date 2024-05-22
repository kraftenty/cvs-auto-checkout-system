from flask import Flask
from flask_socketio import SocketIO

import data.initializer
import routes
import detectioner

app = Flask(__name__)
app.secret_key = '1234'

socketio = SocketIO(app)
data.initializer.initialize()  # DB 초기화
app.register_blueprint(routes.bp)  # 블루프린트 등록

detectioner.init_socketio(app)  # 소켓 초기화

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=False, port=65535)
