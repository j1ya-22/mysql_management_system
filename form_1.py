from flask import Flask, redirect, request, abort, make_response, render_template, url_for, jsonify
import pymysql
from cryptography import *
connect = pymysql.connect(host='111.229.162.217', db='test', user='guest', passwd='Guest111@',port=3306,charset='utf8')
# 创建数据库访问的游标
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
# 首页
@app.route('/', methods=['GET', 'POST'])
def home_page():
    if request.method == 'GET':
        return render_template('header.html')
# 添加联系人
@app.route('/create', methods=['GET', 'POST'])
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
