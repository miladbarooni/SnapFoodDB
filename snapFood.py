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
        data = self.showAllCity()
        for city in data :
            if city_name == city[1]:
                return city[0]
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

    def searchShopByLocation(self, address_id, radius):
        self._mycursor.execute("SELECT * FROM LOCATION WHERE ADDRESSaddressid = \'{}\';".format(address_id))
        data = self._mycursor.fetchall()
        x = data[0][1]
        y = data[0][2]
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
        self._mycursor.execute("SELECT CATEGORY.* FROM (CATEGORY JOIN FOOD ON CATEGORYcategoryid = categoryid WHERE SHOPshopid = \'{}\'"
        .format(shop_id))
        return self._mycursor.fetchall()

    def addShopAndAdmin(self, user_name, password, city_id, x, y, shop_name = "", shop_about = "", shop_bill_value = "",
     street = "", alley = "", plaque = "", address = ""): #NOT CHECKED
        address_id = self.addAddress(x, y, NULL, city_id, street=street, alley=allay, plaque=plaque, address_text=address)
        self._mycursor.execute("INSERT INTO SHOP(name, `about-text`, `minimum-bill-value`, ADDRESSaddressid) VALUES (\'{}\', \'{}\', \'{}\', \'{}\');"
        .format(shop_name, shop_about, shop_bill_value, address_id))
        shop_id = self._mycursor.lastrowid
        self._mycursor.execute("INSERT INTO ADMIN(username, password, SHOPshopid) VALUES (?, ?, ?);"
        .format(user_name, password, shop_id))
        self._mydb.commit()
        return self._mycursor.lastrowid

    def addFoodToCart(self, food_id, user_id): #NOT CHECKED
        self._mycursor.execute("INSERT INTO CART(USERuserid, FOODfoodid) VALUES (\'{}\', \'{}\');"
        .format(user_id, food_id))
        self._mydb.commit()
        return self._mycursor.lastrowid

    def finalizeCart(self, user_id, address_id, discount_code = None): #NOT CHECKED
        self._mycursor.execute("SELECT FOODfoodid FROM CART WHERE USERuserid = \'{}\';".format(user_id))
        foods = self._mycursor.fetchall()
        if discount_code != None :
            self._mycursor.execute("""SELECT discountid, percent FROM DISCOUNT_USER JOIN DISCOUNT ON discountid = DISCOUNTdiscountid
             WHERE Useruserid = \'{}\' AND text = \'{}\';""".format(user_id, discount_code))
            data = self._mycursor.fetchall()
            if len(data) != 0:
                discount_id = data[0][0]
                discount_percent = int(data[0][1])
            else:
                discount_id = NULL
                discount_percent = 0
        self._mycursor.execute("INSERT INTO STATUS(name) VALUES (\'preparation\');")
        status_id = self._mycursor.lastrowid
        self._mycursor.execute("SELECT WALLETwalletid FROM USER WHERE userid = \'{}\';".format(user_id))
        wallet_id = self._mycursor.fetchall()[0][0]
        self._mycursor.execute("""INSERT INTO INVOIC(DISCOUNTdiscountid, COMMENTcommentid, STATUSstatusid, ADDRESSaddressid, WALLETwalletid, `total-price`)
         VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', 0);""".format(discount_id, NULL, status_id, address_id, wallet_id))
        invoic_id = self._mycursor.lastrowid
        total_price = 0
        for food in foods:
            self._mycursor.execute("INSERT INTO FOOD_INVOIC(FOODfoodid, INVOICinvoiceid) VALUES (\'{}\', \'{}\');"
            .format(food[0], invoic_id))
            self._mycursor.execute("SELECT minimum-bill-value, price FROM SHOP JOIN FOOD ON shopid = SHOPshopid AND foodid = \'{}\'"
            .format(food[0]))
            data = self._mycursor.fetchall()
            price = int(data[0][1])
            shop_bill_value = int(data[0][0])
            if shop_bill_value > price - (price * discount_percent):
                total_price += shop_bill_value
            else:
                total_price += price - (price * discount_percent);
        self._mycursor.execute("SELECT balance FROM WALLET WHERE walletid = \'{}\'".format(wallet_id))
        balance = int(self._mycursor.fetchall()[0][0])
        self._mycursor.execute("UPDATE WALLET SET balance = \'{}\' WHERE walletid = \'{}\';".format(balance - total_price, wallet_id))
        self._mycursor.execute("UPDATE INVOIC SET `total-price` = \'{}\' WHERE invoicid = \'{}\';".format(total_price, invoic_id))
        self._mydb.commit()
        return invoic_id

    def showBuyHistory(self, user_id): #NOT CHECKED
        """
            invoiceid, total-price, DISCOUNT.text, ADDRESSaddressid, FOODfoodid, COMMENT.commentid, STATUS.name
        """
        self._mycursor.execute("""SELECT invoiceid, `total-price`, DISCOUNT.text, ADDRESSaddressid, FOODfoodid, COMMENT.commentid, STATUS.name FROM
        ((((((INVOIC JOIN DISCOUNT ON DISCOUNTdiscountid = discountid)
        JOIN COMMENT ON COMMENTcomentid = commentid)
        JOIN (FOOD_INVOIC ON INVOICinvoicid = invoiceid) JOIN FOOD ON FOODfoodid = foodid)
        JOIN STATUS ON STATUSstatusid = statusid)
        JOIN ADDRESS ON ADDRESSaddressid = addressid)
        JOIN WALLET ON WALLETwalletid = walletid)
        JOIN USER ON WALLET.walletid = USER.WALLETwalletid WHERE USER.userid = \'{}\'""".format(user_id))
        return self._mycursor.fetchall()

    def addComment(self, invoic_id, rate, text = None): #NOT CHECKED
        self._mycursor.execute("INSERT INTO COMMENT(rate, text) VALUES (\'{}\', \'{}\');".format(rate, text))
        comment_id = self._mycursor.lastrowid
        self._mycursor.execute("UPDATE INVOIC SET COMMENTcommentid = \'{}\' WHERE invoiceid = \'{}\';".format(comment_id,invoic_id))
        self._mydb.commit()
        return comment_id

    def showFoods(self, food_ids):  #NOT CHECKED
        """
            food_ids in a list
        """
        sql = "SELECT * FROM FOOD WHERE foodid IN ("
        lst = ""
        for food_id in food_ids:
            if len(lst) == 0:
                lst += str(food_id)
            else:
                lst += (", " + str(food_id))
        sql += (lst + ");")
        self._mycursor.execute(sql)
        return self._mycursor.fetchall()

    def ShowStatus(self, invoic_id):  #NOT CHECKED
        self._mycursor.execute("SELECT STATUS.name FROM STATUS JOIN INVOICE ON statusid = STATUSstatusid WHERE invoiceid = \'{}\'"
        .format(invoic_id))
        return self._mycursor.fetchall()

    def showOrderByShop(self, user_id, shop_id): #NOT CHECKED
        self._mycursor.execute("""SELECT FOOD.* FROM 
        ((FOOD JOIN JOIN `FOOD-INVOIC` ON FOODfoodid = foodid)
        JOIN INVOIC ON INVOICEinvoiceid = invoiceid)
        JOIN USER ON USER.WALLETwalletid = INVOIC.WALLETwalletid
        WHERE USER.userid = \'{}\' AND FOOD.SHOPshopid = \'{}\'""".format(user_id, shop_id))
        return self._mycursor.fetchall()

    def close(self):
        self._mydb.close()

