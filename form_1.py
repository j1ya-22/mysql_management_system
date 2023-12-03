import json

from flask import Flask, redirect, request, render_template, session, jsonify
from functools import wraps
import secrets
from hashlib import md5
from db_control import *

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.secret_key = secrets.token_hex(16)  # 对用户信息加密,随机生成密钥更加安全
print(app.secret_key)

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

@app.route('/select_T', methods=['GET', 'POST'])
@login_required
def select_T():
    r = redgister_db()
    data_all=r.select_Television()
    return render_template('list_Television.html',data_all=data_all,data_num=len(data_all))
@app.route('/select_A', methods=['GET', 'POST'])
@login_required
def select_A():
    r = redgister_db()
    data_all=r.select_Air()
    return render_template('list_Aircondition.html',data_all=data_all,data_num=len(data_all))
@app.route('/select_C', methods=['GET', 'POST'])
@login_required
def select_C():
    r = redgister_db()
    data_all=r.select_Curtain()
    return render_template('list_Curtain.html',data_all=data_all,data_num=len(data_all))
@app.route('/select_L', methods=['GET', 'POST'])
@login_required
def select_L():
    r = redgister_db()
    data_all=r.select_Light()
    return render_template('list_Light.html',data_all=data_all,data_num=len(data_all))
@app.route('/add_T', methods=['GET', 'POST'])
@login_required
def add_T():
    return render_template('create_television.html')

@app.route('/create_T', methods=['GET', 'POST'])
@login_required
def create_T():
    data = json.loads(request.data)
    print(data)
    r = redgister_db()
    t = redgister_db()
    g = redgister_db()
    max_pid=r.select_maxT()
    Pid = max_pid[:1] + str(int(max_pid[1:]) + 1).zfill(len(max_pid) - 1)
    Tname = data['p_name']
    Rid = int(t.select_Rid(data['p_room']))
    Pon = data['p_on']
    Pstime = data['p_stime']
    Petime = data['p_etime']
    Pvolume = data['p_volume']
    Plight = data['p_light']
    g.add_T(Pid,Tname,Rid,Pon,Pstime,Petime,Pvolume,Plight)
    return jsonify({'msg': "添加成功", "redirectUrl": "/select_T"})






if __name__ == '__main__':
    app.run()
