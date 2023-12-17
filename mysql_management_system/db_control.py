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
        sql3="SELECT Pid FROM Product WHERE Pname=%s AND Rid=%s;"
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


    def add_C(self,Pid,Pname,Rid,Pon,Pstime,Petime,Plight):
        sql1 = "INSERT INTO Product VALUES (%s, %s, %s, %s);"
        sql2 = "INSERT INTO Curtain VALUES (%s, %s, %s, %s, %s);"
        sql3 = "SELECT Pid FROM Product WHERE Pname=%s AND Rid=%s;"
        pstyle = "窗帘"
        with self.cursor as cursor:
            data_origin = cursor.execute(sql3, (Pname, Rid,))
            if data_origin:
                return "该窗帘已经在该房间存在"
            else:
                cursor.execute(sql1, (Pid, Pname, pstyle, Rid,))
                cursor.execute(sql2, (Pid, Pon, Pstime, Petime, Plight,))
                self.connect.commit()
                return "添加成功"


    def add_A(self,Pid,Pname,Rid,Pon,Pstime,Petime,Ptemperature,Pwet):
        sql1 = "INSERT INTO Product VALUES (%s, %s, %s, %s);"
        sql2 = "INSERT INTO AirConditioner VALUES (%s, %s, %s, %s, %s, %s);"
        sql3 = "SELECT Pid FROM Product WHERE Pname=%s AND Rid=%s;"
        pstyle = "空调"
        with self.cursor as cursor:
            data_origin = cursor.execute(sql3, (Pname, Rid,))
            if data_origin:
                return "该空调已经在该房间存在"
            else:
                cursor.execute(sql1, (Pid, Pname, pstyle, Rid,))
                cursor.execute(sql2, (Pid, Pon, Pstime, Petime, Ptemperature,Pwet,))
                self.connect.commit()
                return "添加成功"



    def add_L(self,Pid,Pname,Rid,Pon,Pstime,Petime,Plight,Pcolor):
        sql1 = "INSERT INTO Product VALUES (%s, %s, %s, %s);"
        sql2 = "INSERT INTO Light VALUES (%s, %s, %s, %s, %s,%s);"
        sql3 = "SELECT Pid FROM Product WHERE Pname=%s AND Rid=%s;"
        pstyle = "电灯"
        with self.cursor as cursor:
            data_origin = cursor.execute(sql3, (Pname, Rid,))
            if data_origin:
                return "该电灯已经在该房间存在"
            else:
                cursor.execute(sql1, (Pid, Pname, pstyle, Rid,))
                cursor.execute(sql2, (Pid, Pon, Pstime, Petime, Plight,Pcolor,))
                self.connect.commit()
                return "添加成功"


    def del_T(self,Tname,Rid):
        sql1="SELECT Pid FROM Product WHERE Pname=%s AND Rid=%s"
        with self.cursor as cursor:
            cursor.execute(sql1, (Tname,Rid))
            data_origin = cursor.fetchall()
            if data_origin and data_origin[0][0][0]=='T':
                Pid=data_origin[0][0]
                sql2 = "DELETE  FROM Product WHERE Pid=%s;"
                sql3 = "DELETE  FROM Television WHERE Pid=%s;"
                cursor.execute(sql2, (Pid,))
                cursor.execute(sql3, (Pid,))
                self.connect.commit()
                return "删除成功"
            else:
                return "没有这个电视哦"


    def del_C(self,Cname,Rid):
        sql1="SELECT Pid FROM Product WHERE Pname=%s AND Rid=%s"
        with self.cursor as cursor:
            cursor.execute(sql1, (Cname,Rid))
            data_origin = cursor.fetchall()
            if data_origin and data_origin[0][0][0]=='C':
                Pid=data_origin[0][0]
                sql2 = "DELETE  FROM Product WHERE Pid=%s;"
                sql3 = "DELETE  FROM Curtain WHERE Pid=%s;"
                cursor.execute(sql2, (Pid,))
                cursor.execute(sql3, (Pid,))
                self.connect.commit()
                return "删除成功"
            else:
                return "没有这个窗帘哦"


    def del_A(self,Aname,Rid):
        sql1="SELECT Pid FROM Product WHERE Pname=%s AND Rid=%s"
        with self.cursor as cursor:
            cursor.execute(sql1, (Aname,Rid))
            data_origin = cursor.fetchall()
            if data_origin and data_origin[0][0][0]=='A':
                Pid=data_origin[0][0]
                print(Pid)
                sql2 = "DELETE  FROM Product WHERE Pid=%s;"
                sql3 = "DELETE  FROM AirConditioner WHERE Pid=%s;"
                cursor.execute(sql2, (Pid,))
                cursor.execute(sql3, (Pid,))
                self.connect.commit()
                return "删除成功"
            else:
                return "没有这个空调哦"

    def del_L(self, Lname, Rid):
        sql1 = "SELECT Pid FROM Product WHERE Pname=%s AND Rid=%s"
        with self.cursor as cursor:
            cursor.execute(sql1, (Lname, Rid))
            data_origin = cursor.fetchall()
            if data_origin and data_origin[0][0][0]=='L':
                Pid = data_origin[0][0]

                sql2 = "DELETE  FROM Product WHERE Pid=%s;"
                sql3 = "DELETE  FROM Light WHERE Pid=%s;"
                cursor.execute(sql2, (Pid,))
                cursor.execute(sql3, (Pid,))
                self.connect.commit()
                return "删除成功"
            else:
                return "没有这个电灯哦"

    def mod_T(self, Pname,Rid,Pon,Pstime,Petime,Pvolume,Plight):
        sql1 = "UPDATE Television SET Pon=%s, Pstime=%s, Petime=%s, Pvolume=%s, Plight=%s WHERE Pid=%s;"
        sql2 = "SELECT Pid FROM Product WHERE Pname=%s AND Rid=%s"
        with self.cursor as cursor:
            cursor.execute(sql2, (Pname, Rid))
            data_origin = cursor.fetchall()
            if data_origin and data_origin[0][0][0]=='T':
                Pid = data_origin[0][0]
                cursor.execute(sql1, (Pon, Pstime, Petime, Pvolume, Plight, Pid))
                self.connect.commit()
                return "自定义成功"
            else:
                return "没有这个电视哦"

    def mod_C(self, Pname, Rid, Pon, Pstime, Petime, Plight):
        sql1 = "UPDATE Curtain SET Pon=%s, Pstime=%s, Petime=%s, Plight=%s WHERE Pid=%s;"
        sql2 = "SELECT Pid FROM Product WHERE Pname=%s AND Rid=%s"
        with self.cursor as cursor:
            cursor.execute(sql2, (Pname, Rid))
            data_origin = cursor.fetchall()
            if data_origin and data_origin[0][0][0]=='C':
                Pid = data_origin[0][0]
                cursor.execute(sql1, (Pon, Pstime, Petime, Plight, Pid))
                self.connect.commit()
                return "自定义成功"
            else:
                return "没有这个窗帘哦"


    def mod_A(self, Pname, Rid, Pon, Pstime, Petime, Ptemperature, Pwet):
        sql1 = "UPDATE AirConditioner SET Pon=%s, Pstime=%s, Petime=%s, Ptemperature=%s, Pwet=%s  WHERE Pid=%s;"
        sql2 = "SELECT Pid FROM Product WHERE Pname=%s AND Rid=%s"
        with self.cursor as cursor:
            cursor.execute(sql2, (Pname, Rid))
            data_origin = cursor.fetchall()
            if data_origin and data_origin[0][0][0]=='A':
                Pid = data_origin[0][0]
                cursor.execute(sql1, (Pon, Pstime, Petime, Ptemperature, Pwet, Pid))
                self.connect.commit()
                return "自定义成功"
            else:
                return "没有这个空调哦"


    def mod_L(self, Pname, Rid, Pon, Pstime, Petime, Plight, Pcolor):
        sql1 = "UPDATE Light SET Pon=%s, Pstime=%s, Petime=%s, Plight=%s, Pcolor=%s  WHERE Pid=%s;"
        sql2 = "SELECT Pid FROM Product WHERE Pname=%s AND Rid=%s"
        with self.cursor as cursor:
            cursor.execute(sql2, (Pname, Rid))
            data_origin = cursor.fetchall()
            if data_origin and data_origin[0][0][0]=='L':
                Pid = data_origin[0][0]
                cursor.execute(sql1, (Pon, Pstime, Petime, Plight, Pcolor, Pid))
                self.connect.commit()
                return "自定义成功"
            else:
                return "没有这个电灯哦"


    def getup(self):
        sql1='UPDATE Light SET Pstime="7:00",Petime="8:00",Plight=50;'
        sql2='UPDATE Curtain SET Pstime="7:00",Petime="18:00",Plight=100;'
        with self.cursor as cursor:
            cursor.execute(sql1)
            cursor.execute(sql2)
            self.connect.commit()
            return "起床模式开启成功"


    def leave_home(self):
        sql1='UPDATE Television SET Petime = CURTIME();'
        sql2='UPDATE AirConditioner SET Petime = CURTIME();'
        sql3='UPDATE Light SET Petime = CURTIME();'
        with self.cursor as cursor:
            cursor.execute(sql1)
            cursor.execute(sql2)
            cursor.execute(sql3)
            self.connect.commit()
            return "离家模式开启成功"


    def home_back(self):
        sql1='UPDATE Light SET Pon=CURTIME(),Plight=70,Petime=null;'
        sql2='UPDATE Curtain SET Plight=20 WHERE Pon="on";'
        with self.cursor as cursor:
            cursor.execute(sql1)
            cursor.execute(sql2)
            self.connect.commit()
            return "回家模式开启成功"


    def night(self):
        sql1='UPDATE Curtain SET Petime=CURTIME();'
        sql2='UPDATE Television SET Petime=CURTIME();'
        sql3='UPDATE AirConditioner SET Petime=CURTIME();'
        sql4='UPDATE Light SET Pcolor="yellow",Plight=20 WHERE Pon="on";'
        with self.cursor as cursor:
            cursor.execute(sql1)
            cursor.execute(sql2)
            cursor.execute(sql3)
            cursor.execute(sql4)
            self.connect.commit()
            return "深夜模式开启成功"

    def select_all(self):
        sql1 = "SELECT COUNT(*) FROM Television WHERE Pon='on'"
        sql2 = "SELECT COUNT(*) FROM Television WHERE Pon='off'"
        sql3 = "SELECT COUNT(*) FROM Curtain WHERE Pon='on'"
        sql4 = "SELECT COUNT(*) FROM Curtain WHERE Pon='off'"
        sql5 = "SELECT COUNT(*) FROM AirConditioner WHERE Pon='on'"
        sql6 = "SELECT COUNT(*) FROM AirConditioner WHERE Pon='off'"
        sql7 = "SELECT COUNT(*) FROM Light WHERE Pon='on'"
        sql8 = "SELECT COUNT(*) FROM Light WHERE Pon='off'"
        list= []
        with self.cursor as cursor:
            cursor.execute(sql1)
            data_origin1 = cursor.fetchall()
            cursor.execute(sql2)
            data_origin2 = cursor.fetchall()
            cursor.execute(sql3)
            data_origin3 = cursor.fetchall()
            cursor.execute(sql4)
            data_origin4 = cursor.fetchall()
            cursor.execute(sql5)
            data_origin5 = cursor.fetchall()
            cursor.execute(sql6)
            data_origin6 = cursor.fetchall()
            cursor.execute(sql7)
            data_origin7 = cursor.fetchall()
            cursor.execute(sql8)
            data_origin8 = cursor.fetchall()
            list.append(data_origin1[0])
            list.append(data_origin2[0])
            list.append(data_origin3[0])
            list.append(data_origin4[0])
            list.append(data_origin5[0])
            list.append(data_origin6[0])
            list.append(data_origin7[0])
            list.append(data_origin8[0])
            return list
