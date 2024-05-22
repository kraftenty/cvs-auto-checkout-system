from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from flask_socketio import SocketIO, emit, disconnect
import sqlite3
import threading

from properties import constant
import detectioner


bp = Blueprint('main', __name__)
socketio = SocketIO()


@bp.route('/', methods=['GET'])
def index():
    if constant.MANAGER_SESSION in session:
        return render_template('main.html')
    else:
        return render_template('index.html')
    
@bp.route('/', methods=['POST'])
def index_login():
    if request.method == 'POST':
        password = request.form['password']
        conn = sqlite3.connect('data/data.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM manager WHERE password = ?', (password,))
        manager = cursor.fetchone()
        cursor.close()
        conn.close()

        if manager:
            session[constant.MANAGER_SESSION] = True
            return redirect('/')
        else:
            flash('비밀번호가 일치하지 않습니다.', 'error')
            return render_template('index.html')

@bp.route('/auth/update', methods=['GET'])
def auth_update():
    if constant.MANAGER_SESSION in session:
        return render_template('manager/update_password_form.html')
    else:
        return render_template('index.html')

@bp.route('/auth/update', methods=['POST'])
def auth_update_post():
    if constant.MANAGER_SESSION in session:
        if request.method == 'POST':
            oldpassword = request.form['oldpassword']
            newpassword_1 = request.form['newpassword_1']
            newpassword_2 = request.form['newpassword_2']

            # 새로운 비밀번호가 일치하는지 체크
            if newpassword_1 != newpassword_2:
                flash('새로운 비밀번호가 일치하지 않습니다.', 'error')
                return render_template('manager/update_password_form.html')

            conn = sqlite3.connect('data/data.db')
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM manager WHERE password = ?', (oldpassword, ))
            manager = cursor.fetchone()
            if manager:
                cursor.execute('UPDATE manager SET password = ? WHERE password = ?', (newpassword_1, oldpassword, ))
                conn.commit()
                cursor.close()
                return redirect('/')
            else:
                flash('현재 비밀번호가 일치하지 않습니다.', 'error')
                return render_template('manager/update_password_form.html')
    else:
        return render_template('index.html')

@bp.route('/auth/logout', methods=['GET'])
def auth_logout():
    if constant.MANAGER_SESSION in session:
        session.pop(constant.MANAGER_SESSION, None)
        return redirect('/')
    else:
        return render_template('index.html')


### 고객 서비스 관련 라우팅

@bp.route('/customer/start', methods=['GET'])
def customer_start():
    detectioner.stop_detection()

    if constant.MANAGER_SESSION in session:
        return render_template('customer/start.html')
    else:
        return render_template('index.html')
    
@bp.route('/customer/scan', methods=['GET'])
def customer_scan():
    if constant.MANAGER_SESSION in session:
        # 인식 로직을 별도 스레드로 실행
        # 스레드 중복 실행 방지
        if not hasattr(bp, 'detection_thread') or not bp.detection_thread.is_alive():
            detectioner.restart_detection()
            detection_thread = threading.Thread(target=detectioner.detection, args=(detectioner.stop_event,))
            detection_thread.daemon = True  # 데몬으로 지정
            detection_thread.start()  # 스레드 시작
            bp.detection_thread = detection_thread
        return render_template('customer/scan.html')
    else:
        return render_template('index.html')

@bp.route('/customer/pay', methods=['POST'])
def pay_creditcard():
    detectioner.stop_detection()

    if constant.MANAGER_SESSION in session:
        total_price = request.form['total_price']
        payment_method = request.form['payment_method']
        year = request.form['year']
        month = request.form['month']
        day = request.form['day']

        conn = sqlite3.connect('data/data.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO sales (amount, payment_method, year, month, day) VALUES (?, ?, ?, ?, ?)', (total_price, payment_method, year, month, day))
        conn.commit()
        cursor.close()

        return redirect('/customer/complete')
    else:
        return render_template('index.html')

@bp.route('/customer/complete', methods=['GET'])
def customer_complete():
    if constant.MANAGER_SESSION in session:
        return render_template('customer/complete.html')
    else:
        return render_template('index.html')
    

# 통계
@bp.route('/statistics', methods=['GET'])
def statistics():
    if constant.MANAGER_SESSION in session:
        year = request.args.get('year')
        month = request.args.get('month')
        
        if year and month:
            conn = sqlite3.connect('data/data.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM sales WHERE year = ? AND month = ?''', (year, month))
            results = cursor.fetchall()
            conn.close()

            return render_template('manager/statistics.html', results=results, selected_year=year, selected_month=month)
        
        return render_template('manager/statistics.html')
    else:
        return render_template('index.html')
