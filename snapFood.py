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
        self._mycursor.execute("INSERT INTO USER (`first-name`, `last-name`, `phone-number`, email, password, WALLETwalletid) VALUES (%s, %s, %s, %s, %s, %s);"
        , (str(f_name), str(l_name), str(phone_number), str(email), str(password), str(wallet_id),))
        self._mydb.commit()
        return self._mycursor.lastrowid


    def login(self, phone_number):
        self._mycursor.execute("SELECT `phone-number`, password, userid FROM USER WHERE `phone-number` = %s", (str(phone_number),))
        return self._mycursor.fetchall()

    def showUser(self, user_id):
        self._mycursor.execute("SELECT * FROM USER WHERE `userid`=%s", (str(user_id),))
        return self._mycursor.fetchall()

    def updateUserProfile(self, user_id, f_name = "", l_name = "", phone_number = "", email = "", passwd = ""):
        self._mycursor.execute("SELECT * FROM USER WHERE userid=%s", (str(user_id),))
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
        self._mycursor.execute("UPDATE USER SET `first-name` = %s, `last-name` = %s, `phone-number` = %s, `email` = %s, `password` = %s WHERE userid = %s;"
        , (str(f_name), str(l_name), str(phone_number), str(email), str(passwd), str(user_id),))
        self._mydb.commit()
        return "DONE"

    def showUserAddress(self, user_id) :
        self._mycursor.execute("SELECT CITY.name, ADDRESS.* FROM ADDRESS JOIN CITY ON ADDRESS.CITYcityid = CITY.cityid WHERE ADDRESS.USERuserid = %s", (str(user_id),))
        return self._mycursor.fetchall()

    def showAddress(self, address_id):
        self._mycursor.execute("SELECT CITY.name, ADDRESS.* FROM ADDRESS JOIN CITY ON ADDRESS.CITYcityid = CITY.cityid WHERE addressid = %s", (str(address_id),))
        return self._mycursor.fetchall()

    def showAllCity(self):
        self._mycursor.execute("SELECT * FROM CITY")
        return self._mycursor.fetchall()

    def addCity(self, city_name):
        data = self.showAllCity()
        for city in data :
            if city_name == city[1]:
                return city[0]
        self._mycursor.execute("INSERT INTO CITY (name) VALUES (%s);", (str(city_name),))
        self._mydb.commit()
        return self._mycursor.lastrowid

    def addAddress(self, x, y, user_id, city_id, street = "", alley = "", plaque = "", address_text = ""):
        self._mycursor.execute("INSERT INTO ADDRESS(street, alley, plaque, `address-text`, USERuserid, CITYcityid) VALUES (%s, %s, %s, %s, %s, %s);"
        , (str(street), str(alley), str(plaque), str(address_text), str(user_id), str(city_id),))
        address_id = self._mycursor.lastrowid
        self._mycursor.execute("INSERT INTO LOCATION(x, y, ADDRESSaddressid) VALUES (%s, %s, %s);"
        , (str(x), str(y), str(address_id),))
        self._mydb.commit()
        return address_id

    def deletAddress(self, address_id):
        self._mycursor.execute("DELETE FROM ADDRESS WHERE addressid = %s;", (str(address_id),))
        self._mydb.commit()

    def updateAddress(self, address_id, x = None, y = None, city_id = None, street = None, alley = None, plaque = None, address_text = None):
        self._mycursor.execute("SELECT x, y, cityid, street, alley, plaque, address_text, locationid  FROM ADDRESS JOIN CITY ON ADDRESS.CITYcityid = CITY.cityid JOIN LOCATION ON ADDRESSaddressid = addressid WHERE ADDRESS.USERuserid = %s", (user_id))
        data = self._mycursor.fetchall()[0]
        location_id = data[7]
        if x == None:
            x = data[0]
        if y == None:
            y = data[1]
        if city_id == None:
            city_id = data[2]
        if street == None:
            street = data[3]
        if alley == None:
            alley = data[4]
        if plaque == None:
            plaque = data[5]
        if address_text == None:
            address_text = data[6]
        self._mycursor.execute("UPDATE ADDRESS SET street = %s, alley = %s, plaque = %s, `address-text` = %s, CITYcityid = %s WHERE addressid = %s;"
        , (str(street), str(alley), str(plaque), str(address_text), str(city_id), str(address_id),))
        self._mycursor.execute("UPDATE LOCATION SET x = %s, y = %s WHERE locationid = %s;", (str(x), str(y), str(location_id),))
        self._mydb.commit()

    def searchShopByLocation(self, address_id, radius):
        self._mycursor.execute("SELECT * FROM LOCATION WHERE ADDRESSaddressid = %s;", (str(address_id),))
        data = self._mycursor.fetchall()
        x = int(data[0][1])
        y = int(data[0][2])
        self._mycursor.execute("SELECT * FROM LOCATION;")
        data = self._mycursor.fetchall()
        sql = "SELECT * FROM SHOP WHERE ADDRESSaddressid IN ("
        lst = ""
        val = []
        for location in data:
            l_x = int(location[1])
            l_y = int(location[2])
            if (l_x - x)^2 + (l_y - y)^2 <= radius^2:
                if len(lst) == 0 :
                    lst += "%s"
                    val.append(str(location[3]))
                else:
                    lst += ", %s"
                    val.append(str(location[3]))
        sql += (lst + ");")
        self._mycursor.execute(sql, val)
        return self._mycursor.fetchall()

    def searchShopByCity(self, city_id):
        self._mycursor.execute("SELECT SHOP.* FROM SHOP JOIN ADDRESS ON ADDRESSaddressid = addressid WHERE CITYcityid = %s", (str(city_id),))
        return self._mycursor.fetchall()

    def showShop(self, shop_id = None):
        if shop_id == None:
            self._mycursor.execute("SELECT * FROM SHOP;")
        else:
            self._mycursor.execute("SELECT * FROM SHOP WHERE shopid = %s;", (str(shop_id),))
        return self._mycursor.fetchall()

    def showFoodsOfShop(self, shop_id):
        self._mycursor.execute("SELECT * FROM FOOD WHERE SHOPshopid = %s;", (str(shop_id),))
        return self._mycursor.fetchall()

    def showCategoryOfShop(self, shop_id):
        self._mycursor.execute("SELECT CATEGORY.* FROM CATEGORY JOIN FOOD ON FOOD.CATEGORYcategoryid = CATEGORY.categoryid WHERE SHOPshopid = %s;"
        , (str(shop_id),))
        return self._mycursor.fetchall()

    def addShopAndAdmin(self, user_name, password, city_id, x, y, shop_name = "", shop_about = "", shop_bill_value = "",
     street = "", alley = "", plaque = "", address = ""):
        address_id = self.addAddress(x, y, "", city_id, street=street, alley=alley, plaque=plaque, address_text=address)
        self._mycursor.execute("INSERT INTO SHOP(name, `about-text`, `minimum-bill-value`, ADDRESSaddressid) VALUES (%s, %s, %s, %s);"
        , (str(shop_name), str(shop_about), str(shop_bill_value), str(address_id),))
        shop_id = self._mycursor.lastrowid
        self._mycursor.execute("INSERT INTO ADMIN(username, password, SHOPshopid) VALUES (%s, %s, %s);"
        , (str(user_name), str(password), str(shop_id),))
        self._mydb.commit()
        return self._mycursor.lastrowid

    def addFoodToCart(self, food_id, user_id):
        self._mycursor.execute("INSERT INTO CART(USERuserid, FOODfoodid) VALUES (%s, %s);"
        , (str(user_id), str(food_id),))
        self._mydb.commit()
        return self._mycursor.lastrowid

    def finalizeCart(self, user_id, address_id, discount_code = None):
        self._mycursor.execute("SELECT FOODfoodid FROM CART WHERE USERuserid = %s;", (str(user_id),))
        foods = self._mycursor.fetchall()
        if discount_code != None :
            self._mycursor.execute("""SELECT discountid, percent FROM DISCOUNT_USER JOIN DISCOUNT ON discountid = DISCOUNTdiscountid
             WHERE Useruserid = %s AND text = %s;""", (str(user_id), str(discount_code),))
            data = self._mycursor.fetchall()
            if len(data) != 0:
                discount_id = data[0][0]
                discount_percent = int(data[0][1])
            else:
                discount_id = 'NULL'
                discount_percent = 0
        self._mycursor.execute("SELECT statusid FROM STATUS WHERE name = \'Prepration\';")
        status_id = int(self._mycursor.fetchall()[0][0])
        self._mycursor.execute("SELECT WALLETwalletid FROM USER WHERE userid = %s;", (str(user_id),))
        wallet_id = self._mycursor.fetchall()[0][0]
        self._mycursor.execute("""INSERT INTO INVOIC(DISCOUNTdiscountid, COMMENTcommentid, STATUSstatusid, ADDRESSaddressid, WALLETwalletid, `total-price`)
         VALUES (%s, %s, %s, %s, %s, 0);""", (str(discount_id), "NULL", str(status_id), str(address_id), str(wallet_id),))
        invoic_id = self._mycursor.lastrowid
        total_price = 0
        for food in foods:
            self._mycursor.execute("INSERT INTO FOOD_INVOIC (FOODfoodid, INVOICinvoiceid) VALUES (%s, %s);"
            , (str(food[0]), str(invoic_id),))
            self._mycursor.execute("DELETE FROM CART WHERE USERuserid = %s AND FOODfoodid = %s;", (str(user_id),str(food[0]),))
            self._mycursor.execute("SELECT `minimum-bill-value`, price FROM SHOP JOIN FOOD ON shopid = SHOPshopid AND foodid = %s"
            , (str(food[0]),))
            data = self._mycursor.fetchall()
            price = int(data[0][1])
            shop_bill_value = int(data[0][0])
            if shop_bill_value > price - (price * discount_percent):
                total_price += shop_bill_value
            else:
                total_price += price - (price * discount_percent)
        self._mycursor.execute("SELECT balance FROM WALLET WHERE walletid = %s", (str(wallet_id),))
        balance = int(self._mycursor.fetchall()[0][0])
        self._mycursor.execute("UPDATE WALLET SET balance = %s WHERE walletid = %s;", (str(balance - total_price), str(wallet_id),))
        self._mycursor.execute("UPDATE INVOIC SET `total-price` = %s WHERE invoiceid = %s;", (str(total_price), str(invoic_id),))
        self._mydb.commit()
        return invoic_id

    def showBuyHistory(self, user_id):
        """
            invoiceid, total-price, ADDRESSaddressid, FOODfoodid, STATUS.name
        """
        self._mycursor.execute("""SELECT invoiceid, `total-price`, ADDRESSaddressid, FOODfoodid, STATUS.name FROM
        ((((INVOIC JOIN (FOOD_INVOIC JOIN FOOD ON FOODfoodid = foodid) ON INVOICinvoiceid = invoiceid) 
        JOIN STATUS ON STATUSstatusid = statusid)
        JOIN ADDRESS ON ADDRESSaddressid = addressid)
        JOIN WALLET ON WALLETwalletid = walletid)
        JOIN USER ON WALLET.walletid = USER.WALLETwalletid WHERE USER.userid = %s AND STATUS.name = \'Completed\';""", (str(user_id),))
        return self._mycursor.fetchall()

    def showAllHistory(self, user_id):
        """
            invoiceid, total-price, ADDRESSaddressid, FOODfoodid, STATUS.name
        """
        self._mycursor.execute("""SELECT invoiceid, `total-price`, ADDRESSaddressid, FOODfoodid, STATUS.name FROM
        ((((INVOIC JOIN (FOOD_INVOIC JOIN FOOD ON FOODfoodid = foodid) ON INVOICinvoiceid = invoiceid) 
        JOIN STATUS ON STATUSstatusid = statusid)
        JOIN ADDRESS ON ADDRESSaddressid = addressid)
        JOIN WALLET ON WALLETwalletid = walletid)
        JOIN USER ON WALLET.walletid = USER.WALLETwalletid WHERE USER.userid = %s;""", (str(user_id),))
        return self._mycursor.fetchall()

    def addComment(self, invoic_id, rate, text = None):
        self._mycursor.execute("INSERT INTO COMMENT(rate, text) VALUES (%s, %s);", (str(rate), str(text),))
        comment_id = self._mycursor.lastrowid
        #self._mycursor.execute("SELECT COMMENTcommentid FROM INVOIC WHERE invoiceid = %s;", (str(invoic_id),))
        #last_comment_id = int(self._mycursor.fetchall()[0][0])
        #self._mycursor.execute("DELETE FROM COMMENT WHERE commentid = %s;", (str(last_comment_id),))
        self._mycursor.execute("UPDATE INVOIC SET COMMENTcommentid = %s WHERE invoiceid = %s;""", (str(comment_id), str(invoic_id),))
        self._mydb.commit()
        return comment_id

    def setStateToComplete(self, invoic_id):
        self._mycursor.execute("UPDATE INVOIC SET STATUSstatusid = \'10\' WHERE invoiceid = %s;", (str(invoic_id),))
        self._mydb.commit()

    def setStateToSending(self, invoic_id):
        self._mycursor.execute("UPDATE INVOIC SET STATUSstatusid = \'11\' WHERE invoiceid = %s;", (str(invoic_id),))
        self._mydb.commit()

    def showFoods(self, food_ids):
        """
            food_ids is a list
        """
        sql = "SELECT * FROM FOOD WHERE foodid IN ("
        lst = ""
        vals = []
        for food_id in food_ids:
            if len(lst) == 0:
                lst += "%s"
                vals.append(str(food_id))
            else:
                lst += ", %s"
                vals.append(str(food_id))
        sql += (lst + ");")
        self._mycursor.execute(sql, vals)
        return self._mycursor.fetchall()

    def ShowStatus(self, invoic_id):
        self._mycursor.execute("SELECT STATUS.name FROM STATUS JOIN INVOICE ON statusid = STATUSstatusid WHERE invoiceid = %s"
        , (str(invoic_id),))
        return self._mycursor.fetchall()

    def showOrderByShop(self, user_id, shop_id):
        self._mycursor.execute("""SELECT FOOD.* FROM 
        ((FOOD JOIN `FOOD_INVOIC` ON FOODfoodid = foodid)
        JOIN INVOIC ON INVOICinvoiceid = invoiceid)
        JOIN USER ON USER.WALLETwalletid = INVOIC.WALLETwalletid
        WHERE USER.userid = %s AND FOOD.SHOPshopid = %s""", (str(user_id), str(shop_id),))
        return self._mycursor.fetchall()

    def searchShop(self, city_id = None, name = None, min_bill_val = -1):
        sql = "SELECT SHOP.* FROM SHOP JOIN ADDRESS ON ADDRESSaddressid = addressid"
        vals = []
        if city_id != None or name != None or min_bill_val != -1 :
            sql += " WHERE "
        need_and = 0
        if city_id != None :
            sql += "ADDRESS.CITYcityid = %s"
            vals.append(str(city_id))
            need_and = 1
        if name != None :
            if need_and == 1 :
                sql += " AND "
            sql += "SHOP.name LIKE (%s)"
            vals.append(str(name) + "%")
            need_and = 1
        if min_bill_val != -1:
            if need_and == 1 :
                sql += " AND "
            sql += "SHOP.`minimum-bill-value` > %s"
            vals.append(str(min_bill_val))
        sql += ";"
        self._mycursor.execute(sql, vals)
        return self._mycursor.fetchall()

    def searchCategory(self, name = None):
        sql = "SELECT * FROM CATEGORY "
        vals = []
        if name != None:
            sql += "WHERE name LIKE (%s)"
            vals.append(str(name) + "%")
        sql += ";"
        self._mycursor.execute(sql, vals)
        return self._mycursor.fetchall()

    def searchFood(self, price_l = None, price_h = None, name = None, discount = None, category_id = None):
        sql = """SELECT FOOD.foodid, FOOD.name, FOOD.price, FOOD.about, FOOD.discount, CATEGORY.name, SHOP.name, SHOP.shopid FROM 
        (FOOD JOIN CATEGORY ON FOOD.CATEGORYcategoryid = CATEGORY.categoryid) JOIN SHOP ON FOOD.SHOPshopid = SHOP.shopid """
        need_and = 0
        vals = []
        if price_l != None or price_h != None or name != None or discount != None or category != None:
            sql += "WHERE "
        if price_l != None:
            sql += "FOOD.price >= %s"
            vals.append(str(price_l))
            need_and = 1
        if price_h != None:
            if need_and == 1:
                sql += " AND "
            sql += "FOOD.price <= %s"
            vals.append(str(price_h))
            need_and = 1
        if name != None:
            if need_and ==1:
                sql += " AND "
            sql += "FOOD.name LIKE (%s)"
            vals.append(str(name) + "%")
            need_and = 1
        if discount != None:
            if need_and == 1:
                sql += " AND "
            sql += "FOOD.discount = %s"
            vals.append(str(discount))
            need_and = 1
        if category_id != None:
            if need_and == 1:
                sql += " AND "
            sql += "CATEGORY.categoryid = %s"
            vals.append(str(category_id))
        sql += ";"
        self._mycursor.execute(sql, vals)
        return self._mycursor.fetchall()


    def addFood(self, price, about, name, discount, category_id, shop_id, image = ""):
        self._mycursor.execute("""INSERT INTO FOOD(price, about, name, discount, image, CATEGORYcategoryid, SHOPshopid) 
        VALUES (%s, %s, %s, %s, %s, %s, %s);"""
        , (str(price), str(about), str(name), str(discount), str(image), str(category_id), str(shop_id),))
        self._mydb.commit()
        return self._mycursor.lastrowid

    def addCategory(self, name):
        self._mycursor.execute("INSERT INTO CATEGORY(name) VALUES (%s);", (str(name),))
        self._mydb.commit()
        return self._mycursor.lastrowid 

    def shopOfCategory(self, catrgory_id):
        self._mycursor.execute("SELECT SHOP.* FROM SHOP JOIN FOOD ON FOOD.SHOPshopid = SHOP.shopid WHERE FOOD.CATEGORYcategoryid = %s"
        , (str(catrgory_id),))
        return self._mycursor.fetchall()

    def showCategoryName(self, category_id):
        self._mycursor.execute("SELECT name FROM CATEGORY WHERE categoryid = %s;", (str(category_id),))
        return self._mycursor.fetchall()

    def showAllCategory(self):
        self._mycursor.execute("SELECT * FROM CATEGORY;")
        return self._mycursor.fetchall()

    def addDiscountCodeForUser(self, user_id, code, percent=50):
        self._mycursor.execute("INSERT INTO DISCOUNT(`percent`, text) VALUES (%s, %s);", (str(percent), str(code),))
        discount_id = self._mycursor.lastrowid
        self._mycursor.execute("INSERT INTO DISCOUNT_USER(DISCOUNTdiscountid, USERuserid) VALUES (%s, %s);", (str(discount_id), str(user_id),))
        self._mydb.commit()
        return discount_id

    def charging(self, user_id, amount):  #NOT CHECKED
        self._mycursor.execute("SELECT balance, walletid FROM WALLET JOIN USER ON WALLETwalletid = walletid WHERE userid = %s;",(str(user_id),))
        data = self._mycursor.fetchall()[0]
        balance = int(data[0])
        wallet_id = data[1]
        self._mycursor.execute("UPDATE WALLET SET balance = %s WHERE walletid = %s;", (str(balance + amount), str(wallet_id),))
        self._mydb.commit()

    def adminLogin(self, username):  #NOT CHECKED
        self._mycursor.execute("SELECT * FROM ADMIN WHERE username = %s", (str(username),))
        return self._mycursor.fetchall()

    def deleteFood(self, food_id):  #NOT CHECKED
        self._mycursor.execute("DELETE FROM FOOD WHERE foodid = %s;", (str(food_id),))
        self._mydb.commit() 

    def updateFood(self, food_id, price = "", about = "", name = "", discount = "", category_id = "", image = ""):   #NOT CHECKED
        self._mycursor.execute("SELECT * FROM FOOD WHERE foodid = %s;", (str(food_id),))
        data = self._mycursor.fetchall()[0]
        if price == "":
            price = data[1]
        if about == "":
            about = data[2]
        if name == "":
            name = data[3]
        if discount == "":
            discount = data[4]
        if category_id == "":
            category_id = data[6]
        if image == "":
            image = data[5]
        self._mycursor.execute("UPDATE FOOD SET price = %s, about = %s, name = %s, discount = %s, image = %s, CATEGORYcategoryid = %s WHERE foodid = %s;"
        .format(str(price), str(about), str(name), str(discount), str(image), str(category_id), str(food_id),))
        self._mydb.commit()

    def showActiveOrder(self, shop_id):  #NOT CHECKED
        """
            invoiceid, total-price, ADDRESSaddressid, FOODfoodid, STATUS.name
        """
        self._mycursor.execute("""SELECT invoiceid, `total-price`, ADDESSaddressid, FOODfoodid, STATUS.name FROM
        (((SHOP JOIN FOOD ON SHOPshopid = shopid)
        JOIN `FOOD_INVOIC ON FOODfoodid = foodid)
        JOIN INVOIC ON INVOICinvoiceid = invoiceid)
        JOIN STATUS ON STATUSstatusid = statusid WHERE shopid = %s AND STATUS.name <> \'Completed\';""", (str(shop_id),))
        return self._mycursor.fetchall()

    def showShopHistory(self, shop_id):  #NOT CHECKED
        """
            invoiceid, total-price, ADDRESSaddressid, FOODfoodid, STATUS.name
        """
        self._mycursor.execute("""SELECT invoiceid, `total-price`, ADDESSaddressid, FOODfoodid, STATUS.name FROM
        (((SHOP JOIN FOOD ON SHOPshopid = shopid)
        JOIN `FOOD_INVOIC ON FOODfoodid = foodid)
        JOIN INVOIC ON INVOICinvoiceid = invoiceid)
        JOIN STATUS ON STATUSstatusid = statusid WHERE shopid = %s AND STATUS.name = \'Completed\';""", (str(shop_id),))
        return self._mycursor.fetchall()

    def showAllComments(self, shop_id):  #NOT CHECKED
        self._mycursor.execute("""SELECT invoiceid, `total-price`, ADDESSaddressid, FOODfoodid, COMMENT.text, COMMENT.rate FROM
        (((SHOP JOIN FOOD ON SHOPshopid = shopid)
        JOIN `FOOD_INVOIC ON FOODfoodid = foodid)
        JOIN INVOIC ON INVOICinvoiceid = invoiceid)
        JOIN COMMENT ON COMMENTcommetnid = commentid WHERE shopid = %s;""", (str(shop_id),))
        return self._mycursor.fetchall()

    def temp(self):
        #self._mycursor.execute("UPDATE STATUS SET name = \'Prepration\' WHERE statusid = 7;")
        self._mydb.commit()

    def close(self):
        self._mydb.close()

db = SnapFoodDB()
print(db.temp())
db.close()