import mysql.connector as mysql
mydb = mysql.connect(host='localhost',user='root', password='geetansh2k1', database='library')
cur = mydb.cursor()
cur.execute("create table student_list(book_id varchar(20),title varchar(30),student_name varchar(30),student_phone varchar(10),student_address varchar(50),issued_on varchar(15),return_date varchar(15),fine float(6,2))")
mydb.commit()