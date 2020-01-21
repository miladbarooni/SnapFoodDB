import mysql.connector

class SnapFoodDB:

    def __init__(self):
        self._mydb = mysql.connector.connect(
            host = "87.236.212.181",
            user = "myproject",
            passwd = "myproject",
            database = "snapFood"
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

    def updateUserProfile(self, phone_number, f_name = "", l_name = "", email = "", passwd = ""):
        self._mycursor.execute("SELECT * FROM USER WHERE phone-number=\'{}\'".format(phone_number))
        tmp = self._mycursor.fetchall()
        if len(tmp) != 1 :
            return "ERROR"
        if f_name == "" :
            f_name = tmp[0][1]
        if l_name == "" :
            l_name = tmp[0][2]
        if email == "" :
            email = tmp[0][4]
        if passwd == "" :
            passwd = tmp[0][5]
        self._mycursor.execute("UPDATE USER SET `first-name` = \'{}\', `last-name` = \'{}\', email = \'{}\', password = \'{}\' WHERE phone-number = \'{}\';"
        .format(f_name, l_name, email, passwd, phone_number))
        self._mydb.commit()
        return "DONE"

    def showAddress(self, user_id) :
        self._mycursor.execute("SELECT ADDRESS.* FROM ADDRESS WHERE USERuserid = \'{}\'".format(user_id))
        return self._mycursor.fetchall()

    #def addAddress(self, city, x, y)

    def close(self):
        self._mydb.close()
