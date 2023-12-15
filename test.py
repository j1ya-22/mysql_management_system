from db_control import *
r=redgister_db()
data=r.select_all()
print(data)