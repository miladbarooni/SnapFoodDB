import mysql.connector

class SnapFoodDB:

    def __init__(self):
        self._mydb = mysql.connector.connect(
            host = "host",
            user = "user",
            passwd = "pass",
            database = "database"
        )
        self._mycursor = self._mydb.cursor()

    def registerUser(self, user_id, password, f_name = "", l_name = "", phone_number = "", email = "", wallet_id = ""):
        self._mycursor.execute("INSERT INTO USER VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')"
        .format(user_id, f_name, l_name, phone_number, email, password, wallet_id))
        self._mydb.commit()

    def close(self):
        self._mydb.close()

