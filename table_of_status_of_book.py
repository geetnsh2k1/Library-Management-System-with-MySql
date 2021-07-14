import mysql.connector as mysql
mydb = mysql.connect(host='localhost', user='root', password='geetansh2k1', database='library')
cur = mydb.cursor()
cur.execute("create table status(book_id varchar(20), title varchar(30), availability varchar(15))")
mydb.commit()