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
        return self._mycursor.lastrowid


    def login(self, phone_number):
        self._mycursor.execute("SELECT `phone-number`, password, userid FROM USER WHERE `phone-number`=\'{}\'".format(phone_number))
        return self._mycursor.fetchall()

    def showUser(self, user_id):
        self._mycursor.execute("SELECT * FROM USER WHERE `userid`=\'{}\'".format(user_id))
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

    def showAllCity(self):
        self._mycursor.execute("SELECT * FROM CITY")
        return self._mycursor.fetchall()

    def addCity(self, city_name):
        self._mycursor.execute("INSERT INTO CITY (name) VALUES (\'{}\');".format(city_name))
        self._mydb.commit()
        return self._mycursor.lastrowid

    def addAddress(self, x, y, user_id, city_id, street = "", alley = "", plaque = "", address_text = ""):
        self._mycursor.execute("INSERT INTO ADDRESS(street, alley, plaque, `address-text`, USERuserid, CITYcityid) VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\');"
        .format(street, alley, plaque, address_text, user_id, city_id))
        address_id = self._mycursor.lastrowid
        self._mycursor.execute("INSERT INTO LOCATION(x, y, ADDRESSaddressid) VALUES (\'{}\', \'{}\', \'{}\');"
        .format(x, y, address_id))
        self._mydb.commit()
        return address_id

    def searchShopByLocation(self, x, y, radius):
        self._mycursor.execute("SELECT * FROM LOCATION;")
        data = self._mycursor.fetchall()
        sql = "SELECT * FROM SHOP WHERE ADDRESSaddressid IN ("
        lst = ""
        for location in data:
            l_x = int(location[1])
            l_y = int(location[2])
            if (l_x - x)^2 + (l_y - y)^2 <= radius^2:
                if len(lst) == 0 :
                    lst += str(location[3])
                else:
                    lst += (", " + str(location[3]))
        sql += (lst + ");")
        self._mycursor.execute(sql)
        return self._mycursor.fetchall()

    def searchShopByCity(self, city_id):  #NOT CHECKED
        self._mycursor.execute("SELECT SHOP.* FROM SHOP JOIN ADDRESS ON ADDRESSaddressid = addressid WHERE CITYcityid = \'{}\'"
        .format(city_id))
        return self._mycursor.fetchall()

    def showShop(self, shop_id = None): #NOT CHECKED
        if shop_id == None:
            self._mycursor.execute("SELECT * FROM SHOP;")
        else:
            self._mycursor.execute("SELECT * FROM SHOP WHERE shopid = \'{}\';"
            .format(shop_id))
        return self._mycursor.fetchall()

    def showFoodsOfShop(self, shop_id): #NOT CHECKED
        self._mycursor.execute("SELECT * FROM FOOD WHERE SHOPshopid = \'{}\';".format(shop_id))
        return self._mycursor.fetchall()

    def showCategoryOfShop(self, shop_id): #NOT CHECKED
        self._mycursor.execute("SELECT CATEGORY.* FROM CATEGORY JOIN ")

    def close(self):
        self._mydb.close()

<<<<<<< HEAD
db = SnapFoodDB()
# print(db.addAddress("0", "0", 1, 2, "Pasdaran BLVD.", "Aghaee St.", "22", "Hadis St."))
# print(db.showAddress(1))
db.close()
=======
>>>>>>> 7c3d2a10261e5267dd0ae2a3cc90e225adbe57a3
