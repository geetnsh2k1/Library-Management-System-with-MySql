import mysql.connector as mysql
mydb = mysql.connect(host='localhost', user='root', password='geetansh2k1', database='library')
cur = mydb.cursor()
query = "create table books(sNo integer(4),book_id varchar(20),title varchar(30),price float(5,2))"
cur.execute(query)
mydb.commit()