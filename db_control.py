import pymysql
class redgister_db(object):
    def __init__(self):
        self.connect = pymysql.connect(host='111.229.162.217', db='test', user='guest', passwd='Guest111@', port=3306, charset='utf8')
        self.cursor = self.connect.cursor()
    # 插入数据的函数
    def signin(self, username):
        sql = "SELECT * FROM secret WHERE user=%s;"
        with self.cursor as cursor:
            cursor.execute(sql, (username,))
            data_origin = cursor.fetchall()
        return data_origin

    def signup(self, username, password):
        sql = "INSERT INTO secret VALUES (%s, %s);"
        with self.cursor as cursor:
            cursor.execute(sql, (username, password,))
            self.connect.commit()

    def select_Television(self):
        sql = "select * from 查询电视类"
        with self.cursor as cursor:
            cursor.execute(sql)
            data_origin = cursor.fetchall()
        return  data_origin

    def select_Air(self):
        sql = "select * from 查询空调类"
        with self.cursor as cursor:
            cursor.execute(sql)
            data_origin = cursor.fetchall()
        return  data_origin

    def select_Curtain(self):
        sql = "select * from 查询窗帘类"
        with self.cursor as cursor:
            cursor.execute(sql)
            data_origin = cursor.fetchall()
        return  data_origin

    def select_Light(self):
        sql = "select * from 查询电灯类"
        with self.cursor as cursor:
            cursor.execute(sql)
            data_origin = cursor.fetchall()
        return  data_origin