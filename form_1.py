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
                return jsonify({'msg': "登录成功", "redirectUrl": "/header"})
            else:
                return jsonify({'msg': "密码错误", "redirectUrl": "/"})
        else:
            return jsonify({'msg': "用户名不存在", "redirectUrl": "/"})
    else:
        return jsonify({'msg': "用户名或密码不能为空哈", "redirectUrl": "/"})


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
    if verify[0][1] == md5_hash(token):
        if data:
            return jsonify({'msg': "用户名已存在", "redirectUrl": "/"})
        else:
            r = redgister_db()
            pwd = md5_hash(pwd)
            r.signup(user, pwd)
            return jsonify({'msg': "注册成功，请去登录", "redirectUrl": "/"})
    else:
        return jsonify({'msg': "token错误", "redirectUrl": "/"})


@app.route('/header', methods=['GET', 'POST'])
@login_required
def home_page():
    if request.method == 'GET':
        return render_template('header.html')


@app.route('/help', methods=['GET', 'POST'])
@login_required
def help_page():
        return render_template('help.html')

@app.route('/select_T', methods=['GET', 'POST'])
@login_required
def select_T():
    r = redgister_db()
    data_all = r.select_Television()
    return render_template('list_Television.html', data_all=data_all, data_num=len(data_all))


@app.route('/select_A', methods=['GET', 'POST'])
@login_required
def select_A():
    r = redgister_db()
    data_all = r.select_Air()
    return render_template('list_Aircondition.html', data_all=data_all, data_num=len(data_all))


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
    data_all = r.select_Light()
    return render_template('list_Light.html', data_all=data_all, data_num=len(data_all))


@app.route('/add_T', methods=['GET', 'POST'])
@login_required
def add_T():
    return render_template('create_television.html')

@app.route('/create_T', methods=['GET', 'POST'])
@login_required
def create_T():
    data = json.loads(request.data)
    r = redgister_db()
    t = redgister_db()
    g = redgister_db()
    max_pid = r.select_maxT()
    Pid = max_pid[:1] + str(int(max_pid[1:]) + 1).zfill(len(max_pid) - 1)
    Tname = data['p_name']
    Rid = int(t.select_Rid(data['p_room']))
    Pon = data['p_on']
    Pstime = data['p_stime']
    Petime = data['p_etime']
    Pvolume = data['p_volume']
    Plight = data['p_light']
    massage=g.add_T(Pid,Tname,Rid,Pon,Pstime,Petime,Pvolume,Plight)
    if massage=="添加成功":
        return jsonify({'msg': massage, "redirectUrl": "/select_T"})
    else:
        return jsonify({'msg': massage, "redirectUrl": "/add_T"})

@app.route('/add_C', methods=['GET', 'POST'])
@login_required
def add_C():
    return render_template('create_curtain.html')

@app.route('/create_C', methods=['GET', 'POST'])
@login_required
def create_C():
    data = json.loads(request.data)
    r = redgister_db()
    t = redgister_db()
    g = redgister_db()
    max_pid=r.select_maxC()
    Pid = max_pid[:1] + str(int(max_pid[1:]) + 1).zfill(len(max_pid) - 1)
    Tname = data['p_name']
    Rid = int(t.select_Rid(data['p_room']))
    Pon = data['p_on']
    Pstime = data['p_stime']
    Petime = data['p_etime']
    Plight = data['p_light']
    massage=g.add_C(Pid,Tname,Rid,Pon,Pstime,Petime,Plight)
    if massage=="添加成功":
        return jsonify({'msg': massage, "redirectUrl": "/select_C"})
    else:
        return jsonify({'msg': massage, "redirectUrl": "/add_C"})




@app.route('/add_A', methods=['GET', 'POST'])
@login_required
def add_A():
    return render_template('create_airconditioner.html')

@app.route('/create_A', methods=['GET', 'POST'])
@login_required
def create_A():
    data = json.loads(request.data)
    r = redgister_db()
    t = redgister_db()
    g = redgister_db()
    max_pid=r.select_maxA()
    Pid = max_pid[:1] + str(int(max_pid[1:]) + 1).zfill(len(max_pid) - 1)
    Tname = data['p_name']
    Rid = int(t.select_Rid(data['p_room']))
    Pon = data['p_on']
    Pstime = data['p_stime']
    Petime = data['p_etime']
    Ptemperature = data['p_temperature']
    Pwet = data['p_wet']
    massage=g.add_A(Pid,Tname,Rid,Pon,Pstime,Petime,Ptemperature,Pwet)
    if massage=="添加成功":
        return jsonify({'msg': massage, "redirectUrl": "/select_A"})
    else:
        return jsonify({'msg': massage, "redirectUrl": "/add_A"})



@app.route('/add_L', methods=['GET', 'POST'])
@login_required
def add_L():
    return render_template('create_light.html')

@app.route('/create_L', methods=['GET', 'POST'])
@login_required
def create_L():
    data = json.loads(request.data)
    r = redgister_db()
    t = redgister_db()
    g = redgister_db()
    max_pid=r.select_maxL()
    Pid = max_pid[:1] + str(int(max_pid[1:]) + 1).zfill(len(max_pid) - 1)
    Tname = data['p_name']
    Rid = int(t.select_Rid(data['p_room']))
    Pon = data['p_on']
    Pstime = data['p_stime']
    Petime = data['p_etime']
    Plight = data['p_light']
    Pcolor = data['p_color']

    massage=g.add_L(Pid,Tname,Rid,Pon,Pstime,Petime,Plight,Pcolor)

    if massage=="添加成功":
        return jsonify({'msg': massage, "redirectUrl": "/select_L"})
    else:
        return jsonify({'msg': massage, "redirectUrl": "/add_L"})




@app.route('/del_T', methods=['GET', 'POST'])
@login_required
def del_T():
    return render_template('delete_television.html')

@app.route('/delete_T', methods=['GET', 'POST'])
@login_required
def delete_T():
    data = json.loads(request.data)
    Tname=data['p_name']
    Rname = data['p_room']
    r = redgister_db()
    t = redgister_db()
    Rid = t.select_Rid(Rname)
    massage = r.del_T(Tname,Rid)
    if massage=="删除成功":
        return jsonify({'msg': massage, "redirectUrl": "/select_T"})
    else:
        return jsonify({'msg': massage, "redirectUrl": "/del_T"})


@app.route('/del_C', methods=['GET', 'POST'])
@login_required
def del_C():
    return render_template('delete_curtain.html')

@app.route('/delete_C', methods=['GET', 'POST'])
@login_required
def delete_C():
    data = json.loads(request.data)
    Cname=data['p_name']
    Rname = data['p_room']
    r = redgister_db()
    t = redgister_db()
    Rid = t.select_Rid(Rname)
    massage = r.del_C(Cname,Rid)
    if massage=="删除成功":
        return jsonify({'msg': massage, "redirectUrl": "/select_C"})
    else:
        return jsonify({'msg': massage, "redirectUrl": "/del_C"})



@app.route('/del_A', methods=['GET', 'POST'])
@login_required
def del_A():
    return render_template('delete_airconditioner.html')

@app.route('/delete_A', methods=['GET', 'POST'])
@login_required
def delete_A():
    data = json.loads(request.data)
    Aname=data['p_name']
    Rname = data['p_room']
    r = redgister_db()
    t = redgister_db()
    Rid = t.select_Rid(Rname)
    massage = r.del_A(Aname,Rid)
    if massage=="删除成功":
        return jsonify({'msg': massage, "redirectUrl": "/select_A"})
    else:
        return jsonify({'msg': massage, "redirectUrl": "/del_A"})



@app.route('/del_L', methods=['GET', 'POST'])
@login_required
def del_L():
    return render_template('delete_light.html')

@app.route('/delete_L', methods=['GET', 'POST'])
@login_required
def delete_L():
    data = json.loads(request.data)
    Lname = data['p_name']
    Rname = data['p_room']
    r = redgister_db()
    t = redgister_db()
    Rid = t.select_Rid(Rname)
    massage = r.del_L(Lname,Rid)
    if massage=="删除成功":
        return jsonify({'msg': massage, "redirectUrl": "/select_L"})
    else:
        return jsonify({'msg': massage, "redirectUrl": "/del_L"})



@app.route('/mod_T', methods=['GET', 'POST'])
@login_required
def mod_T():
    return render_template('modify_television.html')


@app.route('/modify_T', methods=['GET', 'POST'])
@login_required
def modify_T():
    data = json.loads(request.data)
    t = redgister_db()
    Tname = data['p_name']
    Rid = int(t.select_Rid(data['p_room']))
    Pon = data['p_on']
    Pstime = data['p_stime']
    Petime = data['p_etime']
    Plight = data['p_light']
    Pvolume = data['p_volume']
    r = redgister_db()
    massage=r.mod_T(Tname, Rid, Pon, Pstime, Petime, Pvolume, Plight)
    if massage=="自定义成功":
        return jsonify({'msg': massage, "redirectUrl": "/select_T"})
    else:
        return jsonify({'msg': massage, "redirectUrl": "/mod_T"})


@app.route('/mod_C', methods=['GET', 'POST'])
@login_required
def mod_C():
    return render_template('modify_curtain.html')


@app.route('/modify_C', methods=['GET', 'POST'])
@login_required
def modify_C():
    data = json.loads(request.data)
    t = redgister_db()
    Tname = data['p_name']
    Rid = int(t.select_Rid(data['p_room']))
    Pon = data['p_on']
    Pstime = data['p_stime']
    Petime = data['p_etime']
    Plight = data['p_light']
    r = redgister_db()
    massage=r.mod_C(Tname, Rid, Pon, Pstime, Petime, Plight)
    if massage=="自定义成功":
        return jsonify({'msg': massage, "redirectUrl": "/select_C"})
    else:
        return jsonify({'msg': massage, "redirectUrl": "/mod_C"})


@app.route('/mod_A', methods=['GET', 'POST'])
@login_required
def mod_A():
    return render_template('modify_airconditioner.html')


@app.route('/modify_A', methods=['GET', 'POST'])
@login_required
def modify_A():
    data = json.loads(request.data)
    t = redgister_db()
    Tname = data['p_name']
    Rid = int(t.select_Rid(data['p_room']))
    Pon = data['p_on']
    Pstime = data['p_stime']
    Petime = data['p_etime']
    P_temperature = data['p_temperature']
    P_wet = data['p_wet']
    r = redgister_db()
    massage=r.mod_A(Tname, Rid, Pon, Pstime, Petime, P_temperature, P_wet)
    if massage=="自定义成功":
        return jsonify({'msg': massage, "redirectUrl": "/select_A"})
    else:
        return jsonify({'msg': massage, "redirectUrl": "/mod_A"})


@app.route('/mod_L', methods=['GET', 'POST'])
@login_required
def mod_L():
    return render_template('modify_light.html')


@app.route('/modify_L', methods=['GET', 'POST'])
@login_required
def modify_L():
    data = json.loads(request.data)
    t = redgister_db()
    Tname = data['p_name']
    Rid = int(t.select_Rid(data['p_room']))
    Pon = data['p_on']
    Pstime = data['p_stime']
    Petime = data['p_etime']
    P_light = data['p_light']
    P_color = data['p_color']
    r = redgister_db()
    massage=r.mod_L(Tname, Rid, Pon, Pstime, Petime, P_light, P_color)
    if massage=="自定义成功":
        return jsonify({'msg': massage, "redirectUrl": "/select_L"})
    else:
        return jsonify({'msg': massage, "redirectUrl": "/mod_L"})



@app.route('/modefy', methods=['GET', 'POST'])
@login_required
def modify():
    return render_template('modes.html')


@app.route('/modes', methods=['GET', 'POST'])
@login_required
def modes():
    data = json.loads(request.data)
    t = redgister_db()
    mode=data['mode']
    if mode=="起床":
        massage=t.getup()
        return jsonify({'msg': massage})
    if mode=="出门":
        massage=t.leave_home()
        return jsonify({'msg': massage})
    if mode=="回家":
        massage=t.home_back()
        return jsonify({'msg': massage})
    if mode=="深夜":
        massage=t.night()
        return jsonify({'msg': massage})






if __name__ == '__main__':
    app.run(host='0.0.0.0',port=12345)
