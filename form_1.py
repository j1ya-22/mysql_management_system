from flask import Flask, redirect, request, render_template,session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from functools import wraps
import pymysql
import secrets
connect = pymysql.connect(host='111.229.162.217', db='test', user='guest', passwd='Guest111@',port=3306,charset='utf8')
# 创建数据库访问的游标
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
# 首页
app.secret_key = secrets.token_hex(16)  # 对用户信息加密,随机生成密钥更加安全
def login_required(func):#实现鉴权
    """
    Custom decorator to check if the user is authenticated.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_info' in session:
            return func(*args, **kwargs)
        else:
            return redirect('/')
    return wrapper
@app.route('/', methods=['GET', "POST"])  # 路由默认接收请求方式位POST，然而登录所需要请求都有，所以要特别声明。
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        user = request.form.get('user')
        pwd = request.form.get('pwd')
        sql = f"select * from secret where user={0}".format(user)#获取用户的数据
        cursor = connect.cursor()
        cursor.execute(sql)
        data_origin = cursor.fetchall()
        connect.commit()
        if  pwd == data_origin[0][1] and user==data_origin[0][0]:   #将密码和数据库中存放的密码进行比对
            session['user_info'] = user #生成session，后期可以进行鉴权
            return redirect('/header')
        else:
            return render_template('login.html', msg='用户名或密码输入错误')
@app.route('/header', methods=['GET', 'POST'])
@login_required
def home_page():
    if request.method == 'GET':
        return render_template('header.html')
# 添加联系人
@app.route('/create', methods=['GET', 'POST'])
@login_required
def insert_person():
    cursor = connect.cursor()
    if request.method == 'GET':
        return render_template('create.html')
    if request.method == 'POST':
        name = request.form.get('name')
        UserAddress = request.form.get('UserAddress')
        UserPhone = request.form.get('UserPhone')
        # sql="INSERT INTO address_list VALUES (%s, %s, %s)"
        cursor.execute("INSERT INTO address_list VALUES (%s, %s, %s)", (name, UserAddress, UserPhone))
        connect.commit()
        cursor.close()
        return render_template('success.html')
# 删除联系人
@app.route('/delete', methods=['GET', 'POST'])
@login_required
def delete_person():
    cursor = connect.cursor()
    if request.method == 'GET':
        return render_template('delete.html')
    if request.method == 'POST':
        name = request.form.get('name')
        print(name)
        cursor.execute("delete from address_list where 商品名 = (%s)",(name))
        connect.commit()
        cursor.close()
        return render_template('success.html')
# 查找一个联系人
@app.route('/query_1', methods=['GET', 'POST'])
@login_required
def select_person():
    cursor = connect.cursor()
    if request.method == 'GET':
        return render_template('query_1.html')
    if request.method == 'POST':
        name = request.form.get('name')
        print(name)
        print(cursor.execute(" select 价格,编码 from address_list where 商品名 = (%s)",(name)))
        cursor.execute(" select 价格,编码 from address_list where 商品名 = (%s)",(name))
        data_origin = cursor.fetchall()
        connect.commit()
        cursor.close()
        return render_template('query_all.html', name=name, address=data_origin[0][0], phone=data_origin[0][1])
@app.route('/list', methods=['GET', 'POST'])
@login_required
def select_all():
    cursor = connect.cursor()
    if request.method == 'GET':
        cursor.execute("select * from address_list")
        # if type(data_all) != 'str':
        #     data_all = str(data_all)
        data_all=cursor.fetchall()
        print(data_all)
        print(len(data_all))
        connect.commit()
        cursor.close()
        return render_template('list.html', data_all=data_all, data_num=len(data_all))
if __name__ == '__main__':
    app.run()
