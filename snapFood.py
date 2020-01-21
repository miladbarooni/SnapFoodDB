import mysql.connector
import sys
sys.path.insert(0, '..')
from config import *

class SnapFoodDB:

    def __init__(self):
        self._mydb = mysql.connector.connect(
            host = host,
            user = user,
            passwd = password,
            database = database
        )
        self._mycursor = self._mydb.cursor()

    def registerUser(self, phone_number, password, f_name = "", l_name = "", email = ""):
        self._mycursor.execute("INSERT INTO WALLET(balance) VALUES (0);")
        wallet_id = self._mycursor.lastrowid
        self._mycursor.execute("INSERT INTO USER (`first-name`, `last-name`, `phone-number`, email, password, WALLETwalletid) VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\');"
        .format(f_name, l_name, phone_number , email, password, wallet_id))
        self._mydb.commit()


    def login(self, phone_number):
        self._mycursor.execute("SELECT `phone-number`, password FROM USER WHERE `phone-number`=\'{}\'".format(phone_number))
        return self._mycursor.fetchall()

    def showUser(self, phone_number):
        self._mycursor.execute("SELECT * FROM USER WHERE `phone-number`=\'{}\'".format(phone_number))
        return self._mycursor.fetchall()

    def updateUserProfile(self, user_id, f_name = "", l_name = "", phone_number = "", email = "", passwd = ""):
        self._mycursor.execute("SELECT * FROM USER WHERE userid=\'{}\'".format(user_id))
        tmp = self._mycursor.fetchall()
        if len(tmp) != 1 :
            return "ERROR"
        if f_name == "" :
            f_name = tmp[0][1]
        if l_name == "" :
            l_name = tmp[0][2]
        if phone_number == "" :
            phone_number = tmp[0][3]
        if email == "" :
            email = tmp[0][4]
        if passwd == "" :
            passwd = tmp[0][5]
        self._mycursor.execute("UPDATE USER SET `first-name` = \'{}\', `last-name` = \'{}\', `phone-number` = \'{}\', `email` = \'{}\', `password` = \'{}\' WHERE userid = \'{}\';"
        .format(f_name, l_name, phone_number, email, passwd, user_id))
        self._mydb.commit()
        return "DONE"

    def showAddress(self, user_id) :
        self._mycursor.execute("SELECT ADDRESS.* FROM ADDRESS WHERE USERuserid = \'{}\'".format(user_id))
        return self._mycursor.fetchall()

    #def addAddress(self, city, x, y)

    def close(self):
        self._mydb.close()

db = SnapFoodDB()
db.updateUserProfile("2", email="temp1@gmail.com")
db.close()