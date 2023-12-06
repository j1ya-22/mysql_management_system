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
    def select_maxT(self):
        sql="SELECT MAX(Pid) FROM 查询电视类;"
        with self.cursor as cursor:
            cursor.execute(sql)
            data_origin = cursor.fetchall()
        return  data_origin[0][0]
    def select_maxC(self):
        sql="SELECT MAX(Pid) FROM 查询窗帘类;"
        with self.cursor as cursor:
            cursor.execute(sql)
            data_origin = cursor.fetchall()
        return  data_origin[0][0]

    def select_maxA(self):
        sql="SELECT MAX(Pid) FROM 查询空调类;"
        with self.cursor as cursor:
            cursor.execute(sql)
            data_origin = cursor.fetchall()
        return  data_origin[0][0]

    def select_maxL(self):
        sql = "SELECT MAX(Pid) FROM 查询电灯类;"
        with self.cursor as cursor:
            cursor.execute(sql)
            data_origin = cursor.fetchall()
        return data_origin[0][0]
    def select_Rid(self,Rname):
        sql="SELECT Rid FROM Room WHERE Rname=%s;"
        with self.cursor as cursor:
            cursor.execute(sql, (Rname,))
            data_origin = cursor.fetchall()
        return data_origin[0][0]
    def add_T(self,Pid,Pname,Rid,Pon,Pstime,Petime,Pvolume,Plight):
        sql1="INSERT INTO Product VALUES (%s,%s,%s,%s);"
        sql2="INSERT INTO Television VALUES (%s, %s, %s, %s, %s, %s);"
        sql3="SELECT Pid FROM Product WHERE Pname=%s AND Rid=%s "
        pstyle="电视机"
        with self.cursor as cursor:
            data_origin=cursor.execute(sql3, (Pname, Rid,))
            if data_origin:
                return "该电视已经在该房间存在"
            else:
                cursor.execute(sql1,(Pid,Pname,pstyle,Rid,))
                cursor.execute(sql2,(Pid,Pon,Pstime,Petime,Pvolume,Plight,))
                self.connect.commit()
                return "添加成功"


    def add_C(self,Pid,Cname,Rid,Pon,Pstime,Petime,Plight):
        sql1 = "INSERT INTO Product VALUES (%s, %s, %s, %s);"
        sql2 = "INSERT INTO Curtain VALUES (%s, %s, %s, %s, %s);"
        pstyle = "窗帘"
        with self.cursor as cursor:
            cursor.execute(sql1, (Pid, Cname, pstyle, Rid,))
            cursor.execute(sql2, (Pid, Pon, Pstime, Petime, Plight,))
            self.connect.commit()


    def add_A(self,Pid,Aname,Rid,Pon,Pstime,Petime,Ptemperature,Pwet):
        sql1 = "INSERT INTO Product VALUES (%s, %s, %s, %s);"
        sql2 = "INSERT INTO Curtain VALUES (%s, %s, %s, %s, %s);"
        pstyle = "空调"
        with self.cursor as cursor:
            cursor.execute(sql1, (Pid, Aname, pstyle, Rid,))
            cursor.execute(sql2, (Pid, Pon, Pstime, Petime, Ptemperature,Pwet,))
            self.connect.commit()



    def add_L(self,Pid,Aname,Rid,Pon,Pstime,Petime,Plight,Pcolor):
        sql1 = "INSERT INTO Product VALUES (%s, %s, %s, %s);"
        sql2 = "INSERT INTO Curtain VALUES (%s, %s, %s, %s, %s);"
        pstyle = "电灯"
        with self.cursor as cursor:
            cursor.execute(sql1, (Pid, Aname, pstyle, Rid,))
            cursor.execute(sql2, (Pid, Pon, Pstime, Petime, Plight,Pcolor,))
            self.connect.commit()
    def del_T(self,Tname,Rid):
        sql1="SELECT Pid FROM Product WHERE Pname=%s AND Rid=%s"
        with self.cursor as cursor:
            cursor.execute(sql1, (Tname,Rid))
            data_origin = cursor.fetchall()
            if data_origin:
                Pid=data_origin[0][0]
                sql2 = "DELETE  FROM Product WHERE Pid=%s"
                sql3 = "DELETE  FROM Television WHERE Pid=%s"
                cursor.execute(sql2, (Pid,))
                cursor.execute(sql3, (Pid,))
                self.connect.commit()
                return "删除成功"
            else:
                return "没有这个电视哦"