import os
import datetime
import mysql.connector as mysql
class Library:
    def __init__(self,title = None,price = 0.0):
        if title == None and price == 0.0:
            error = 0
            self.__title = input("Enter Book Title : ")
            self.__title = self.__title.upper()
            try:
                self.__price = eval(input("Enter Book Price : "))
            except:
                error = 1
                print("\nInvalid ValueType : for price.")
            if error == 0:
                self.__avail = "Available"
                self.generate_book_id()
                self.store_book_to_database()
                self.store_status_of_book()
                print("Book-Successfully-Added.\n")
            else:
                print("Failed : Book can't be added.")
    def generate_book_id(self):
        fin =  open("E:/Python-Sql/LibraryManagement/Book_Id.txt",'r')
        fout = open("E:/Python-Sql/LibraryManagement/Temp_Book_Id.txt",'w')
        current = int(fin.read())
        self.__book_id = "GGLIB" + str(current)
        current += 1
        fout.write(str(current))
        fin.close()
        fout.close()
        os.remove("E:/Python-Sql/LibraryManagement/Book_Id.txt")
        os.rename("E:/Python-Sql/LibraryManagement/Temp_Book_Id.txt","E:/Python-Sql/LibraryManagement/Book_Id.txt")
    def store_book_to_database(self):
        fin = open("E:/Python-Sql/LibraryManagement/Serial_Number.txt",'r')
        fout = open("E:/Python-Sql/LibraryManagement/Temp_Serial_Number.txt",'w')
        current_sno = (fin.read())
        sno = int(current_sno)+1
        fout.write(str(sno))
        fin.close()
        fout.close()
        os.remove("E:/Python-Sql/LibraryManagement/Serial_Number.txt")
        os.rename("E:/Python-Sql/LibraryManagement/Temp_Serial_Number.txt","E:/Python-Sql/LibraryManagement/Serial_Number.txt")
        mydb = mysql.connect(host='localhost', user='root', password='geetansh2k1', database='library')
        cur = mydb.cursor()
        query = "insert books(sNo,book_id,title,price) values(%s,%s,%s,%s)"
        book = (sno,self.__book_id,self.__title,self.__price)
        cur.execute(query,book)
        mydb.commit()
    def store_status_of_book(self):
        mydb = mysql.connect(host='localhost', user='root', password='geetansh2k1', database='library')
        cur = mydb.cursor()
        query = "insert status(book_id,title,availability) values(%s,%s,%s)"
        book = (self.__book_id,self.__title,self.__avail)
        cur.execute(query,book)
        mydb.commit()
    @staticmethod
    def delete_book_from_database(b_id):
        delete = 0
        fin = open("E:/Python-Sql/LibraryManagement/Serial_Number.txt",'r')
        fout = open("E:/Python-Sql/LibraryManagement/Temp_Serial_Number.txt",'w')
        sno = int(fin.read())
        sno -= 1
        fout.write(str(sno))
        fin.close()
        fout.close()
        os.remove("E:/Python-Sql/LibraryManagement/Serial_Number.txt")
        os.rename("E:/Python-Sql/LibraryManagement/Temp_Serial_Number.txt","E:/Python-Sql/LibraryManagement/Serial_Number.txt")
        b_id = b_id.upper()
        mydb = mysql.connect(host='localhost', user='root', password='geetansh2k1', database='library')
        cur = mydb.cursor()
        cur.execute("select * from books where book_id='%s'" %(b_id))
        book = cur.fetchall()
        if book != []:
            cur.execute("delete from books where book_id='%s'"%(b_id))
        else:
            print("NO BOOK FOUND.")
            delete = 1
        mydb.commit()

        #DELETING STATUS ALSO
        mydb = mysql.connect(host='localhost', user='root', password='geetansh2k1', database='library')
        cur = mydb.cursor()
        cur.execute("delete from status where book_id='%s'" %(b_id))
        cur.execute("delete from student_list where book_id='%s'" %(b_id))
        mydb.commit()

        if delete == 0:
            print("\nBook-Successfully-Removed.\n")
    @staticmethod
    def show_all_books():
        mydb = mysql.connect(host='localhost', user='root', password='geetansh2k1', database='library')
        cur = mydb.cursor()
        query = "select * from books"
        cur.execute(query)
        person = cur.fetchall()
        for i in person:
            print("\nS.No.   : ",i[0])
            print("Book-Id : ",i[1])
            print("Title   : ",i[2])
            print("Price   : ",i[3])
        mydb.commit()
    @staticmethod
    def gather_particular_book_details(b_id):
        b_id = b_id.upper()
        mydb = mysql.connect(host='localhost', user='root', password='geetansh2k1', database='library')
        cur = mydb.cursor()
        cur.execute("select * from books where book_id='%s'" %(b_id))
        person = cur.fetchall()
        for i in person:
            print("\nS.No.   : ",i[0])
            print("Book-Id : ",i[1])
            print("Title   : ",i[2])
            print("Price   : ",i[3])
        mydb.commit()
        Library.check_book_availability(b_id)
    @staticmethod
    def update_price(b_id):
        mydb = mysql.connect(host='localhost', user='root', password='geetansh2k1', database='library')
        cur = mydb.cursor()
        new_price = eval(input("Enter New-Price : "))
        cur.execute("update books set price=%s where book_id='%s'" %(new_price,b_id))
        print("\nPrice-Updated-Successfully.")
        mydb.commit()

        print("Price-Updated-Successfully.\n")
    @staticmethod
    def issue_book(b_id):
        b_id = b_id.upper()
        mydb = mysql.connect(host='localhost', user='root', password='geetansh2k1', database='library')
        cur = mydb.cursor()
        cur.execute("select * from status where book_id = '%s'" %(b_id))
        book = cur.fetchall()
        found = 1
        if book != []:
            for i in book:
                if i[2] == "Available":
                    availability = True
                    book_name = i[1]
                else:
                    availability = False
        else:
            availability = False
            print("\nFailed : No Book Found.\n")
            found = 0
        if availability == True:
            print(book_name,", Is this the book you want to issue? (y/n) : ",end='')
            issue = input()
            if issue == 'y' or issue == 'yes' or issue == 'Y':
                if Library.store_student_details_who_issued(b_id,book_name):
                    cur.execute("update status set availability = 'Issued' where book_id = '%s'" %(b_id))
                    print("Book-Issued Successfully.")
                else:
                    print("ERROR!! : BOOK CAN'T BE ISSUED. (try again).")
            else:
                pass
        else:
            if found == 0:
                pass
            else:
                print("Not Available : BOOK ALREADY ISSUED.") 
        mydb.commit()
    @staticmethod
    def check_book_availability(b_id):
        mydb = mysql.connect(host='localhost', user='root', password='geetansh2k1', database='library')
        cur = mydb.cursor()
        cur.execute("select * from status where book_id = '%s'" %(b_id))
        book = cur.fetchall()
        if book != []:
            for i in book:
                print("Book-Status  :",i[2],end='\n\n')
        else:
            print("No BOOK FOUND.")
        mydb.commit()
    @staticmethod
    def get_book_id(b_title):
        mydb = mysql.connect(host='localhost', user='root', password='geetansh2k1', database='library')
        cur = mydb.cursor()
        cur.execute("select * from books where title='%s'" %(b_title))
        book = cur.fetchall()
        if book != []:
            for i in book:
                print("Book-Id :",i[1])
        else:
            print("Failed : NO BOOK FOUND (with this title.)")
        mydb.commit()
    @staticmethod
    def show_status_of_all_books():
        mydb = mysql.connect(host='localhost', user='root', password='geetansh2k1', database='library')
        cur = mydb.cursor()
        cur.execute("select * from status")
        result = cur.fetchall()
        for i in result:
                print("\nBook-Id :",i[0])
                print("Title   :",i[1])
                print("Status  :",i[2])
            
        print(end='\n')
        mydb.commit()
    @staticmethod
    def return_book(b_id):
        mydb = mysql.connect(host='localhost', user='root', password='geetansh2k1', database='library')
        cur = mydb.cursor()
        cur.execute("select * from status where book_id='%s'" %(b_id))
        book = cur.fetchall()
        if book != []:
            for i in book:
                availability = i[2]
                b_name = i[1]
            if availability == "issued" or availability == "Issued":
                print(b_name,"Returning......")
                cur.execute("update status set availability='Available' where book_id='%s'" %(b_id))
                Library.remove_student_details(b_id)
                print("Fine Pending : Rs.",Library.calculate_fine(b_id))
                print("Book Successfully Returned....")
            else:
                print("ERROR!! : THIS BOOK IS STILL AVAILABLE i.e. NOT ISSUED.")
        else:
            print("Failed : NO BOOK FOUND.")
        mydb.commit()
    @staticmethod
    def store_student_details_who_issued(b_id,book_name):
        print("\nHey, Welcome to the Book-Issue Process......")
        print("Please, Specify your details to continue...\n")
        class Student:
            def __init__(self):
                self.created = True
                self.__name = input("Enter your name : ")
                self.__phone_number = int(input("Enter your 10 digit phone-number : "))
                digits = 0
                temp = self.__phone_number 
                while temp!=0:
                    temp//=10
                    digits+=1
                if digits == 10:
                    self.__address = input("Enter your current address : ")
                else:
                    print("Failed : Invalid Phone-Number.")
                    self.created = False
            def get_name(self):
                return self.__name
            def get_phone_number(self):
                return str(self.__phone_number)
            def get_address(self):
                return self.__address
        s1 = Student()
        if s1.created == True:
            currentDT = str(datetime.datetime.now())
            currentDT = currentDT[0:10]
            date = currentDT[8:10]
            date = int(date) + 15
            if date >= 31:
                date -= 30
                temp = date
                digit = 0
                while(temp!=0):
                    temp//=10
                    digit += 1
                if digit == 1:
                    date = str(0)+str(date)
                month = currentDT[5:7]
                month = int(month) + 1
            returnDT = currentDT[0:5] + str(0) + str(month) + "-" + str(date)
            mydb = mysql.connect(host='localhost', user='root', password='geetansh2k1', database='library')
            cur = mydb.cursor()
            query = "insert into student_list(book_id,title,student_name,student_phone,student_address,issued_on,return_date,fine) values (%s,%s,%s,%s,%s,%s,%s,%s)"
            add_on = (b_id,book_name,s1.get_name(),s1.get_phone_number(),s1.get_address(),currentDT,returnDT,0.0)
            cur.execute(query,add_on)
            mydb.commit()
            return True
        else:
            return False
    @staticmethod
    def remove_student_details(b_id):
        mydb = mysql.connect(host='localhost', user='root', password='geetansh2k1', database='library')
        cur = mydb.cursor()
        cur.execute("delete from student_list where book_id='%s'" %(b_id))
        mydb.commit()
    @staticmethod
    def calculate_fine(b_id):
        mydb = mysql.connect(host='localhost', user='root', password='geetansh2k1', database='library')
        cur = mydb.cursor()
        cur.execute("select * from student_list where book_id='%s'" %(b_id))
        result = cur.fetchall()
        if result != []:
            for i in result:
                returnDt = i[6]
            currentDt = str(datetime.datetime.now())
            currentDt = currentDt[0:10]
            returnDate = returnDt[8:10]
            currentDate = currentDt[8:10]
            returnMonth = returnDt[5:7]
            currentMonth = currentDt[5:7]
            if currentMonth == returnMonth:
                if int(returnDate) - int(currentDate) < 0:
                    days = int(currentDate) - int(returnDate)
                    return abs(days)*50.0
                else:
                    return 0.0
            else:
                currentMonth = int(currentMonth) + 1
                returnDate = abs(int(returnDate) - 30)
                days = int(returnDate) + int(currentDate)
                return abs(days)*50.0
        else:
            return 0.0
        mydb.commit()
    @staticmethod
    def gather_who_issued_book(b_id):
        b_id = b_id.upper()
        mydb = mysql.connect(host='localhost', user='root', password='geetansh2k1', database='library')
        cur = mydb.cursor()
        cur.execute("select * from status where book_id='%s'" %(b_id))
        book = cur.fetchall()
        work = True
        if book != []:
            for i in book:
                if i[2] == "Issued":
                    work = True
                else:
                    work = False
            if work == True:
                cur.execute("select * from student_list where book_id='%s'" %(b_id))
                result = cur.fetchall()
                for i in result:
                    print("\nStudent-Name         :",i[2])
                    print("Student-Phone-Number :",i[3])
                    print("Issued-On            :",i[5])
                    print("Return-Date          :",i[6],end='\n\n')
            else:
                print("Failed : Book is still available i.e. not issued by anyone.")
        else:
            print("No BOOK FOUND.")
        mydb.commit()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      