import json

from flask import Flask, redirect, request, render_template, session, jsonify
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
    data = json.loads(request.data)
    username = data['username']
    password = data['password']
    data = r.signin(username)
    if username and password:
        if data:
            if md5_hash(password) == data[0][1] and username == data[0][0]:  # 将密码和数据库中存放的密码进行比对
                session['user_info'] = username  # 生成session，后期可以进行鉴权
                return jsonify({'msg': "登录成功","redirectUrl":"/header"})
            else:
                return jsonify({'msg': "密码错误","redirectUrl":"/"})
        else:
            return jsonify({'msg': "用户名不存在","redirectUrl":"/"})
    else:
        return jsonify({'msg': "用户名或密码不能为空哈","redirectUrl":"/"})


@app.route('/signup', methods=['GET', 'POST'])
def logup():
    r = redgister_db()
    t = redgister_db()
    data = json.loads(request.data)
    user = data['username']
    pwd = data['password1']
    token = data['token']
    verify = t.signin('admin')
    data = r.signin(user)
    if verify[0][1]==md5_hash(token):
        if data:
            return jsonify({'msg': "用户名已存在","redirectUrl":"/"})
        else:
            r = redgister_db()
            pwd = md5_hash(pwd)
            r.signup(user, pwd)
            return jsonify({'msg': "注册成功，请去登录","redirectUrl":"/"})
    else:
        return jsonify({'msg': "token错误", "redirectUrl": "/"})
@app.route('/header', methods=['GET', 'POST'])
@login_required
def home_page():
    if request.method == 'GET':
        return render_template('header.html')


if __name__ == '__main__':
    app.run()
