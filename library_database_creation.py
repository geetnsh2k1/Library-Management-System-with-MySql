import mysql.connector as mysql
mydb = mysql.connect(host='localhost', user='root', password='geetansh2k1')
cur = mydb.cursor()
cur.execute("create database library")
mydb.commit()