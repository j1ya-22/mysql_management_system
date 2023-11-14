from flask import Flask, redirect, request, render_template, session
from functools import wraps
import secrets
from hashlib import md5
from db_control import *


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.secret_key = secrets.token_hex(16)  # 对用户信息加密,随机生成密钥更加安全


def md5_hash(text):
    text = text.encode('utf-8')
    md5_encode = md5(text)
    return md5_encode.hexdigest()


def login_required(func):  # 实现鉴权
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_info' in session:
            return func(*args, **kwargs)
        else:
            return redirect('/')

    return wrapper


@app.route('/', methods=['GET'])
def log_reg():
    return render_template('login.html')


@app.route('/signin', methods=['POST'])  # 登录界面
def login():
    r = redgister_db()
    print(1)
    user = request.form.get('user')
    pwd = request.form.get('pwd')
    data = r.signin(user)
    print(data)
    if data:
        if md5_hash(pwd) == data[0][1] and user == data[0][0]:  # 将密码和数据库中存放的密码进行比对
            session['user_info'] = user  # 生成session，后期可以进行鉴权
            return redirect('/header')
        else:
            return render_template('login.html', msg='用户名或密码输入错误')
    else:
        return render_template('login.html', msg='用户名或密码输入错误')


@app.route('/signup', methods=['GET', 'POST'])
def logup():
    r = redgister_db()
    user = request.form.get('user')
    pwd = request.form.get('pwd')
    data=r.signin(user)
    if data:
        return
    else:
        r.signup(user,pwd)
        return

@app.route('/header', methods=['GET', 'POST'])
@login_required
def home_page():
    if request.method == 'GET':
        return render_template('header.html')


if __name__ == '__main__':
    app.run()
