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

    def showUserAddress(self, user_id) :
        self._mycursor.execute("SELECT CITY.name, ADDRESS.* FROM ADDRESS JOIN CITY ON ADDRESS.CITYcityid = CITY.cityid WHERE ADDRESS.USERuserid = \'{}\'".format(user_id))
        return self._mycursor.fetchall()

    def showAddress(self, address_id):
        self._mycursor.execute("SELECT CITY.name, ADDRESS.* FROM ADDRESS JOIN CITY ON ADDRESS.CITYcityid = CITY.cityid WHERE addressid = \'{}\'".format(address_id))
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

    def deletAddress(self, address_id):
        self._mycursor.execute("DELETE FROM ADDRESS WHERE addressid = \'{}\';".format(address_id))
        self._mydb.commit()

    def updateAddress(self, x = None, y = None, city_id = None, street = None, alley = None, plaque = None, address_text = None):
        data = self.showAddress(address_id)
        #if x == None:
        #if x == None:
        #if x == None:
        #if x == None:
        #if x == None:
        #if x == None:

    def searchShopByLocation(self, address_id, radius):
        self._mycursor.execute("SELECT * FROM LOCATION WHERE ADDRESSaddressid = \'{}\';".format(address_id))
        data = self._mycursor.fetchall()
        x = int(data[0][1])
        y = int(data[0][2])
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

    def searchShopByCity(self, city_id):
        self._mycursor.execute("SELECT SHOP.* FROM SHOP JOIN ADDRESS ON ADDRESSaddressid = addressid WHERE CITYcityid = \'{}\'"
        .format(city_id))
        return self._mycursor.fetchall()

    def showShop(self, shop_id = None):
        if shop_id == None:
            self._mycursor.execute("SELECT * FROM SHOP;")
        else:
            self._mycursor.execute("SELECT * FROM SHOP WHERE shopid = \'{}\';"
            .format(shop_id))
        return self._mycursor.fetchall()

    def showFoodsOfShop(self, shop_id):
        self._mycursor.execute("SELECT * FROM FOOD WHERE SHOPshopid = \'{}\';".format(shop_id))
        return self._mycursor.fetchall()

    def showCategoryOfShop(self, shop_id):
        self._mycursor.execute("SELECT CATEGORY.* FROM CATEGORY JOIN FOOD ON FOOD.CATEGORYcategoryid = CATEGORY.categoryid WHERE SHOPshopid = \'{}\';"
        .format(shop_id))
        return self._mycursor.fetchall()

    def addShopAndAdmin(self, user_name, password, city_id, x, y, shop_name = "", shop_about = "", shop_bill_value = "",
     street = "", alley = "", plaque = "", address = ""):
        address_id = self.addAddress(x, y, "", city_id, street=street, alley=alley, plaque=plaque, address_text=address)
        self._mycursor.execute("INSERT INTO SHOP(name, `about-text`, `minimum-bill-value`, ADDRESSaddressid) VALUES (\'{}\', \'{}\', \'{}\', \'{}\');"
        .format(shop_name, shop_about, shop_bill_value, address_id))
        shop_id = self._mycursor.lastrowid
        self._mycursor.execute("INSERT INTO ADMIN(username, password, SHOPshopid) VALUES (\'{}\', \'{}\', \'{}\');"
        .format(user_name, password, shop_id))
        self._mydb.commit()
        return self._mycursor.lastrowid

    def addFoodToCart(self, food_id, user_id):
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
                discount_id = 'NULL'
                discount_percent = 0
        self._mycursor.execute("SELECT statusid FROM STATUS WHERE name = \'Prepration\';")
        status_id = int(self._mycursor.fetchall()[0][0])
        self._mycursor.execute("SELECT WALLETwalletid FROM USER WHERE userid = \'{}\';".format(user_id))
        wallet_id = self._mycursor.fetchall()[0][0]
        self._mycursor.execute("""INSERT INTO INVOIC(DISCOUNTdiscountid, COMMENTcommentid, STATUSstatusid, ADDRESSaddressid, WALLETwalletid, `total-price`)
         VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', 0);""".format(discount_id, "NULL", status_id, address_id, wallet_id))
        invoic_id = self._mycursor.lastrowid
        total_price = 0
        for food in foods:
            self._mycursor.execute("INSERT INTO FOOD_INVOIC (FOODfoodid, INVOICinvoiceid) VALUES (\'{}\', \'{}\');"
            .format(food[0], invoic_id))
            self._mycursor.execute("DELETE FROM CART WHERE USERuserid = \'{}\' AND FOODfoodid = \'{}\';".format(user_id,food[0]))
            self._mycursor.execute("SELECT `minimum-bill-value`, price FROM SHOP JOIN FOOD ON shopid = SHOPshopid AND foodid = \'{}\'"
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
        self._mycursor.execute("UPDATE INVOIC SET `total-price` = \'{}\' WHERE invoiceid = \'{}\';".format(total_price, invoic_id))
        self._mydb.commit()
        return invoic_id

    def showBuyHistory(self, user_id):
        """
            invoiceid, total-price, ADDRESSaddressid, FOODfoodid, STATUS.name
        """
        sql = """SELECT invoiceid, `total-price`, ADDRESSaddressid, FOODfoodid, STATUS.name FROM
        ((((INVOIC JOIN (FOOD_INVOIC JOIN FOOD ON FOODfoodid = foodid) ON INVOICinvoiceid = invoiceid) 
        JOIN STATUS ON STATUSstatusid = statusid)
        JOIN ADDRESS ON ADDRESSaddressid = addressid)
        JOIN WALLET ON WALLETwalletid = walletid)
        JOIN USER ON WALLET.walletid = USER.WALLETwalletid WHERE USER.userid = \'{}\' AND STATUS.name = \'Completed\';""".format(user_id)
        sql2 = """SELECT * FROM INVOIC JOIN DISCOUNT ON DISCOUNTdiscountid = discountid JOIN COMMENT ON COMMENTcommentid = commentid"""
        self._mycursor.execute(sql)
        return self._mycursor.fetchall()

    def addComment(self, invoic_id, rate, text = None): #NOT CHECKED
        self._mycursor.execute("INSERT INTO COMMENT(rate, text) VALUES (\'{}\', \'{}\');".format(rate, text))
        comment_id = self._mycursor.lastrowid
        self._mycursor.execute("UPDATE INVOIC SET COMMENTcommentid = \'{}\' WHERE invoiceid = \'{}\';""".format(comment_id,invoic_id))
        self._mydb.commit()
        return comment_id

    def setStateToComplete(self, invoic_id):
        self._mycursor.execute("UPDATE INVOIC SET STATUSstatusid = \'10\' WHERE invoiceid = \'{}\';".format(invoic_id))
        self._mydb.commit()

    def setStateToSending(self, invoic_id):
        self._mycursor.execute("UPDATE INVOIC SET STATUSstatusid = \'11\' WHERE invoiceid = \'{}\';".format(invoic_id))
        self._mydb.commit()

    def showFoods(self, food_ids):  #NOT CHECKED
        """
            food_ids is a list
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

    def searchShop(self, city_id = None, name = None, min_bill_val = -1):
        sql = "SELECT SHOP.* FROM SHOP JOIN ADDRESS ON ADDRESSaddressid = addressid"
        if city_id != None or name != None or min_bill_val != -1 :
            sql += " WHERE "
        need_and = 0
        if city_id != None :
            sql += ("ADDRESS.CITYcityid = \'{}\'".format(city_id))
            need_and = 1
        if name != None :
            if need_and == 1 :
                sql += " AND "
            sql += ("SHOP.name LIKE (\'{}%\')".format(name))
            need_and = 1
        if min_bill_val != -1:
            if need_and == 1 :
                sql += " AND "
            sql += ("SHOP.minimum-bill-value > \'{}\'".format(min_bill_val))
        sql += ";"
        self._mycursor.execute(sql)
        return self._mycursor.fetchall()

    def searchCategory(self, name = None):
        sql = "SELECT * FROM CATEGORY "
        if name != None:
            sql += ("WHERE name LIKE (\'{}%\')".format(name))
        sql += ";"
        self._mycursor.execute(sql)
        return self._mycursor.fetchall()

    def searchFood(self, price_l = None, price_h = None, about = None, name = None, discount = None, category = None): 
        sql = """SELECT FOOD.foodid, FOOD.name, FOOD.price, FOOD.about, FOOD.discount, CATEGORY.name, SHOP.name, SHOP.shopid FROM 
        (FOOD JOIN CATEGORY ON FOOD.CATEGORYcategoryid = CATEGORY.categoryid) JOIN SHOP ON FOOD.SHOPshopid = SHOP.shopid """
        need_and = 0
        if price_l != None or price_h != None or about != None or name != None or discount != None or category != None:
            sql += "WHERE "
        if price_l != None:
            sql += ("FOOD.price >= \'{}\'".format(price_l))
            need_and = 1
        if price_h != None:
            if need_and == 1:
                sql += " AND "
            sql += ("FOOD.price <= \'{}\'".format(price_h))
            need_and = 1
        if about != None:
            if need_and == 1:
                sql += " AND "
            sql += ("FOOD.about LIKE (\'%{}%\')".format(about))
            need_and = 1
        if name != None:
            if need_and ==1:
                sql += " AND "
            sql += ("FOOD.name LIKE (\'{}%\')".format(name))
            need_and = 1
        if discount != None:
            if need_and == 1:
                sql += " AND "
            sql += ("FOOD.discount = \'{}\'".format(discount))
            need_and = 1
        if category != None:
            if need_and == 1:
                sql += " AND "
            sql += ("CATEGORY.name = \'{}\'".format(category))
        sql += ";"
        self._mycursor.execute(sql)
        return self._mycursor.fetchall()


    def addFood(self, price, about, name, discount, category_id, shop_id, image = ""):
        self._mycursor.execute("""INSERT INTO FOOD(price, about, name, discount, image, CATEGORYcategoryid, SHOPshopid) 
        VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\');"""
        .format(price, about, name, discount, image, category_id, shop_id))
        self._mydb.commit()
        return self._mycursor.lastrowid

    def addCategory(self, name):
        self._mycursor.execute("INSERT INTO CATEGORY(name) VALUES (\'{}\');".format(name))
        self._mydb.commit()
        return self._mycursor.lastrowid 

    def shopOfCategory(self, catrgory_id):
        self._mycursor.execute("SELECT SHOP.* FROM SHOP JOIN FOOD ON FOOD.SHOPshopid = SHOP.shopid WHERE FOOD.CATEGORYcategoryid = \'{}\'"
        .format(catrgory_id))
        return self._mycursor.fetchall()

    def showCategoryName(self, category_id):
        self._mycursor.execute("SELECT name FROM CATEGORY WHERE categoryid = \'{}\';".format(category_id))
        return self._mycursor.fetchall()

    def addDiscountCodeForUser(self, user_id, code, percent=50):
        self._mycursor.execute("INSERT INTO DISCOUNT(`percent`, text) VALUES (\'{}\', \'{}\');".format(percent, code))
        discount_id = self._mycursor.lastrowid
        self._mycursor.execute("INSERT INTO DISCOUNT_USER(DISCOUNTdiscountid, USERuserid) VALUES (\'{}\', \'{}\');".format(discount_id, user_id))
        self._mydb.commit()
        return discount_id

    def temp(self):
        #self._mycursor.execute("ALTER TABLE `FOOD_INVOIC` ADD `food-invoicid` int(11)")
        #self._mycursor.execute("ALTER TABLE `FOOD_INVOIC` DROP PRIMARY KEY, ADD PRIMARY KEY (`food-invoicid`);")
        #self._mycursor.execute("ALTER TABLE `FOOD_INVOIC` MODIFY `food-invoicid` int(11) NOT NULL AUTO_INCREMENT;")
        #self._mycursor.execute("ALTER TABLE FOOD_INVOIC ADD CONSTRAINT `is in` FOREIGN KEY (FOODfoodid) REFERENCES FOOD (foodid);")
        #self._mycursor.execute("ALTER TABLE FOOD_INVOIC ADD CONSTRAINT `is in` FOREIGN KEY (INVOICinvoiceid) REFERENCES INVOIC (invoiceid);")
        self._mydb.commit()

    def close(self):
        self._mydb.close()

db = SnapFoodDB()
db.temp()
db.close()