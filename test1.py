import mysql.connector
import datetime
d=datetime.datetime.now()
db=mysql.connector.connect(host="localhost", user="root", password="kanha", database="Banking")
cur=db.cursor()
sql = "select * from fixed_deposits where username=%s"
cur.execute(sql,("Abhijaat",))
for i in cur:
    x = i[9]-i[4]
    y = d-i[4]
    print(x.total_seconds(), y.total_seconds())
db.close()
