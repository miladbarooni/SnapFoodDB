from tkinter import Tk, Label, Button, Toplevel, StringVar, Entry, messagebox, Frame, END, Scrollbar, Y, RIGHT
from tkinter import Checkbutton, IntVar, BooleanVar, Text, INSERT

from functools import partial
import tkinter as tk
from tkinter.ttk import Separator, Style, Combobox, Treeview
from time import sleep
from snapFood import *

mydb = SnapFoodDB()


style = Style()
style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11)) # Modify the font of the body
style.configure("mystyle.Treeview.Heading", font=('Calibri', 13,'bold')) # Modify the font of the headings
style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders
        

class Application:
    def __init__(self, master):
        self.username = ""
        self.password = ""
        # self.db_cursor = mydb.cursor()
        self.master = master
        master.title("Snapp Food")

        #Bring the window to the center of screen
        windowWidth = master.winfo_reqwidth()
        windowHeight = master.winfo_reqheight()
        # print("Width",windowWidth,"Height",windowHeight)
        positionRight = int(master.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(master.winfo_screenheight()/2 - windowHeight/2)
        # Positions the window in the center of the page.
        master.geometry("+{}+{}".format(positionRight, positionDown))

        #Set Number of rows and columns
        self.master.rowconfigure(5)
        self.master.columnconfigure(5)

        self.makeMainWindow()
        

    # def loadingPage(self):
    #     # loader = Tk()
    #     # loader.title("loading")
    #     # root.attributes('-alpha', 1.0)

    def makeMainWindow(self):
        
        self.master.geometry("300x200")

        self.master.title("Account Login")
        
        Label(self.master,text="Select Your Choice", bg="blue", width="300", height="2", font=("Calibri", 13)).pack()
        Label(text="").pack()
        Button(self.master,text="Login", height="2", width="30", command = self.loginPage).pack()
        Label(text="").pack()
        Button(self.master, text="Register", height="2", width="30", command=self.registerPage).pack()
        
        closeButton = Button(self.master, text="Exit", command=self.master.quit, width="200", height="2")
        closeButton.pack()
    
    def loginPage(self):
        self.login_screen = Tk()
        self.login_screen.title("Login")
        self.login_screen.geometry("300x250")
        Label(self.login_screen, text="Please enter details below to login").pack()
        Label(self.login_screen, text="").pack()


        username_verify = StringVar()
        password_verify = StringVar()


        Label(self.login_screen, text="Phone Numbers * ").pack()
        username_login_entry = Entry(self.login_screen, textvariable=username_verify)
        username_login_entry.pack()
        Label(self.login_screen, text="").pack()
        Label(self.login_screen, text="Password * ").pack()
        password_login_entry = Entry(self.login_screen, textvariable=password_verify, show= '*')
        password_login_entry.pack()
        Label(self.login_screen, text="").pack()
        Button(self.login_screen, text="Login", width=10, height=1, command = partial(self.loginVerify, username_login_entry, password_login_entry)).pack()
        

    def loginVerify(self, username_login_entry, password_login_entry):
        # self.db_cursor.execute("SELECT userid, password FROM USER WHERE userid=\'{}\'".format(username_login_entry.get()))
       
        data = mydb.login(username_login_entry.get())
        self.user_id = data[0][2]
        self.phone_number = username_login_entry.get()
        #check whether user_id exists or not
        if (len(data) != 0 and data[0][1] == password_login_entry.get()):
            
            self.dashboardPage()
        else:
            messagebox.showinfo('Username/Password incorrect', 'your username of password is incorrect')


    def registerPage(self):
        self.register_screen = Toplevel(self.master)
        self.register_screen.title("Register")
        self.register_screen.geometry("300x450")

        

        Label(self.register_screen, text="Please enter details below", bg="blue").pack()
        Label(self.register_screen, text="").pack()

        #phonenumber
        Label(self.register_screen, text="Phone Number * ").pack()
        phone_number_entry = Entry(self.register_screen)
        phone_number_entry.pack()
        #password
        Label(self.register_screen, text="Password * ").pack()
        password_entry = Entry(self.register_screen,show='*')
        password_entry.pack()
        #repeat password
        Label(self.register_screen, text="Password * ").pack()
        repeat_password_entry = Entry(self.register_screen,show='*')
        repeat_password_entry.pack()
        #firstname
        Label(self.register_screen, text="First Name * ").pack()
        firstname_entry = Entry(self.register_screen)
        firstname_entry.pack()
        #lastname
        Label(self.register_screen, text="Last Name * ").pack()
        lastname_entry = Entry(self.register_screen)
        lastname_entry.pack()  
        #email address
        Label(self.register_screen, text="Email Address * ").pack()
        email_entry = Entry(self.register_screen)
        email_entry.pack()

        Label(self.register_screen, text="").pack()
        Button(self.register_screen, text="Register", width=10, height=1, bg="blue", command = partial(self.registerUser,
                                    phone_number_entry ,password_entry, repeat_password_entry, firstname_entry, lastname_entry, email_entry)).pack()



    def registerUser(self ,phone_number_entry, password_entry, repeat_password_entry, firstname_entry, lastname_entry, email_entry):
        #insert into database 
        if (password_entry.get() == repeat_password_entry.get()):
            mydb.registerUser( phone_number_entry.get(), password_entry.get(),firstname_entry.get(), lastname_entry.get(), email_entry.get())
            Label(self.register_screen, text="Register was Seccesful").pack()
        else:
            messagebox.showinfo('Repeat password again', 'your repeated password doesn\'n match your entered password, Try Again')



    def dashboardPage(self):
        self.master.destroy
        self.login_screen.destroy
        self.dashboard = Tk()
        self.dashboard.title("User Dashboard")
        self.dashboard.geometry("300x350")

        Label(self.dashboard, text="Select Your Choice", bg="blue", width="300", height="2", font=("Calibri", 13)).pack()
        Label(text="").pack()
        Button(self.dashboard,text="Profile", height="2", width="30", command = self.profilePage).pack()
        Label(text="").pack()
        Button(self.dashboard,text="Restaurants", height="2", width="30", command=self.restaurantsPage).pack()
        Label(text="").pack()
        Button(self.dashboard,text="Order", height="2", width="30", command=self.orderPage).pack()
        Button(self.dashboard,text="Search", height="2", width="30", command=self.searchFoodOrShop).pack()
        Button(self.dashboard,text="Charge your wallet", height="2", width="30", command=self.chargeWallet).pack()
        
        closeButton = Button(self.dashboard, text="Exit", command=self.dashboard.destroy, width="200", height="2")
        closeButton.pack()

    def chargeWallet(self):
        def charging(charge_wallet_entry):
            mydb.charging(self.user_id, int(charge_wallet_entry.get()))
        self.charge_wallet_screen = Tk()
        self.charge_wallet_screen.title("charging")
        Label(self.charge_wallet_screen, text="Enter A number to charge your wallet", bg="blue", width="300", height="2", font=("Calibri", 13)).pack()
        Label(text="").pack()
        Label(self.charge_wallet_screen, text="Just Numbers")
        charge_wallet_entry = Entry(self.charge_wallet_screen)
        charge_wallet_entry.pack()
        Button(self.charge_wallet_screen, text="Charge My Wallet", command=partial(charging, charge_wallet_entry)).pack()

        

    def searchFoodOrShop(self):
        self.search_screen = Tk()
        self.search_screen.title("Search page")
        Label(self.search_screen, text="Search By Shops", bg="Green", width="300", height="2", font=("Calibri", 13)).pack()
        Label(text="").pack()
        Label(self.search_screen, text="Search part of a name").pack()
        shop_name_entry = Entry(self.search_screen)
        shop_name_entry.pack()
        Label(self.search_screen, text="Choose a city to find shops at that city").pack()
        city_combo = Combobox(self.search_screen)
        cities = mydb.showAllCity()
        self.number_of_cities = len(cities)
        cities_list = []
        
        for i in cities:
            cities_list.append(i[1])
        cities_list.append("None")
        city_combo['values']= cities_list
        city_combo.pack()
        city_combo.current(len(cities))
        # city_id = mydb.addCity(city_combo.get())
        Label(self.search_screen, text="Enter Min Bill Value:").pack()
        min_bill_entry = Entry(self.search_screen)
        min_bill_entry.pack()
        Button(self.search_screen, text="Search", command=partial(self.showRestaurantsBySearch, city_combo, shop_name_entry, min_bill_entry)).pack()
        Label(self.search_screen, text="Search By Foods", bg="Green", width="300", height="2", font=("Calibri", 13)).pack()
        Label(text="").pack()
        Label(self.search_screen, text="Enter a Low Boundery for price").pack()
        price_l_entry = Entry(self.search_screen)
        price_l_entry.pack()
        Label(self.search_screen, text="Enter a High Boundery for price").pack()
        price_h_entry = Entry(self.search_screen)
        price_h_entry.pack()
        
        Label(self.search_screen, text="Search part of a food name").pack()
        food_name_entry = Entry(self.search_screen)
        food_name_entry.pack()
        Label(self.search_screen, text="Enter your desire discount").pack()
        discount_entry = Entry(self.search_screen)
        discount_entry.pack()
        Label(self.search_screen, text="Choose a catogory for you desire food").pack()
        cat_combo = Combobox(self.search_screen)
        catogries = mydb.showAllCategory()
        self.number_of_catogry = len(catogries)
        catogri_list = []
        print (catogries)
        for i in catogries:
            catogri_list.append(str(i[0])+ " "+ i[1])
        catogri_list.append("None")
        cat_combo['values']= catogri_list
        cat_combo.pack()
        cat_combo.current(len(catogries))  
        Button(self.search_screen, text="Search", command=partial(self.showFoods, cat_combo, price_l_entry, price_h_entry, food_name_entry, discount_entry)).pack()

    def showFoods(self, cat_cambo, price_l_entry, price_h_entry, food_name_entry, discount_entry):
        self.search_food_screen = Tk()
        self.search_food_screen.title("Foods")
        price_l = price_l_entry.get()
        if (price_l_entry.get() == ""):
            price_l = None
        price_h = price_h_entry.get()
        if (price_h_entry.get() == ""):
            price_h = None
        food_name = food_name_entry.get()
        if (food_name_entry.get() == ""):
            food_name = None
        discount = discount_entry.get()
        if (discount_entry.get() == ""):
            discount = None
        cat_id = -1
        if (cat_cambo.get()=="None"):
            cat_id = None
        else:
            cat_id = cat_cambo.get()[0]
        print (price_l)
        print (price_h)
        print (food_name)
        print (discount)
        print (cat_id)
        foods = mydb.searchFood(price_l, price_h, food_name, discount, cat_id)
        if (len(foods) != 0):
            Label(self.search_food_screen, text="Result for your search", bg="red", width="300", height="2", font=("Calibri", 13)).pack()
            Label(text="").pack()
            tree=Treeview(self.search_food_screen,style="mystyle.Treeview")
            tree["columns"]=("one","two","three", "four", "five", "six")
            #set tree columns
            tree.column("#0", width=150, minwidth=150, stretch=tk.NO)
            tree.column("one", width=400, minwidth=200)
            tree.column("two", width=80, minwidth=50, stretch=tk.YES)
            tree.column("three", width=80, minwidth=50, stretch=tk.YES)
            tree.column("four", width=80, minwidth=50, stretch=tk.YES)
            tree.column("five", width=80, minwidth=50, stretch=tk.YES)
            tree.column("six", width=80, minwidth=50, stretch=tk.YES)
            #set tree's heading
            tree.heading("#0", text="Name",anchor=tk.W)
            tree.heading("one", text="Price",anchor=tk.W)
            tree.heading("two", text="About",anchor=tk.W)
            tree.heading("three", text="Category",anchor=tk.W)
            tree.heading("four", text="Image",anchor=tk.W)
            tree.heading("five", text="Discount",anchor=tk.W)
            tree.heading("six", text="Resturant",anchor=tk.W)
            tree.pack()
            for i in range(len(foods)):
                tree.insert("", i+1, text=foods[i][1], values=(foods[i][2], foods[i][3], foods[i][5],0, foods[i][4], foods[i][6]))
            tree.bind("<Double-1>", partial(self.OnDoubleClickOnFood,tree, foods))



    def showRestaurantsBySearch(self, city_combo, shop_name_entry, min_bill_entry):
        city_id = -1
        if (city_combo.get() == "None"):
            city_id = None
        else:
            city_id = mydb.addCity(city_combo.get())
        min_bill = min_bill_entry.get()
        if (min_bill_entry.get() == ""):
            min_bill = None
        shop_name = shop_name_entry.get()
        if (shop_name_entry.get() == ""):
            shop_name = None

        resturants = mydb.searchShop(city_id, shop_name, min_bill)
        # print (resturants)
        self.searched_resturant_screen = Tk()
        self.searched_resturant_screen.title("Results")
        tree=Treeview(self.searched_resturant_screen,style="mystyle.Treeview")
        tree["columns"]=("one","two","three", "four")
        #set tree columns
        tree.column("#0", width=270, minwidth=270, stretch=tk.NO)
        tree.column("one", width=150, minwidth=150, stretch=tk.NO)
        tree.column("two", width=400, minwidth=200)
        tree.column("three", width=80, minwidth=50, stretch=tk.YES)
        tree.column("four", width=80, minwidth=50, stretch=tk.YES)
        #set tree's heading
        tree.heading("#0",text="Name",anchor=tk.W)
        tree.heading("one", text="About",anchor=tk.W)
        tree.heading("two", text="min bill value",anchor=tk.W)
        tree.heading("three", text="address",anchor=tk.W)
        tree.heading("four", text="Rate",anchor=tk.W)
        list_of_resturant_in_treeview = []
        for i in range(len(resturants)):
            rate = mydb.calculateRate(resturants[i][0])
            resturant_in_treeview = tree.insert("", i+1, text=resturants[i][1], values=(resturants[i][2], resturants[i][3], 
            self.make_address_str(resturants[i][4]), "--" if rate[0][0] == None else rate[0][0]))
            list_of_resturant_in_treeview.append(resturant_in_treeview)
        # for resturant in list_of_resturant_in_treeview:
        #     index = list_of_resturant_in_treeview.index(resturant)
        #     shop_id = resturants[index][0]
        #     shop_foods = mydb.showFoodsOfShop(shop_id)
            
        tree.pack(side=tk.TOP,fill=tk.X)
        tree.bind("<Double-1>", partial(self.OnDoubleClick,tree, resturants))
    
    def profilePage(self):
        def showAddress():
            self.current_address_screen = Tk()
            addresses = mydb.showUserAddress(self.user_id)
            # print (addresses)
            print (addresses)
            for i in range(len(addresses)):
                # print (addresses[i])
                Label(self.current_address_screen, text="Address #"+str(i+1)+":").pack()
                address_str = ""
                address_str+=addresses[i][0] + ", "
                for j in range(2,6):
                    address_str += addresses[i][j] + ", "
                Label(self.current_address_screen, text=address_str).pack()
                Button(self.current_address_screen, text="Delete this address",command=partial(self.deleteAddress, addresses[i][1])).pack()
        self.profile = Tk()
        self.profile.title("User Profile")
        self.profile.geometry("700x1000")
        
        
        """
        in this section we will show the user his/her information and he or she can change it 
        ##########################################################3
        """
        Label(self.profile, text="Your information", bg="red", width="300", height="2", font=("Calibri", 13)).pack()
        Label(text="").pack()
        user_information = mydb.showUser(self.user_id)
        print (user_information)
        # Show your firstname and edit
        Label(self.profile, text="You FirstName:").pack()
        firstname_entry = Entry(self.profile)
        firstname_entry.pack()
        firstname_entry.insert(END, user_information[0][1])
        # Show your lastname and edit
        Label(self.profile, text="You Lastname:").pack()
        lastname_entry = Entry(self.profile)
        lastname_entry.pack()
        lastname_entry.insert(END, user_information[0][2])
        # Show your phone number and edit
        Label(self.profile, text="You Phone Number:").pack()
        phone_number_entry = Entry(self.profile)
        phone_number_entry.pack()
        phone_number_entry.insert(END, user_information[0][3])
        # Show your email address and edit
        Label(self.profile, text="You email address:").pack()
        email_address_entry = Entry(self.profile)
        email_address_entry.pack()
        email_address_entry.insert(END, user_information[0][4])
        # Show your password and edit
        Label(self.profile, text="You Password:").pack()
        password_entry = Entry(self.profile)
        password_entry.pack()
        password_entry.insert(END, user_information[0][5])
        # Change button
        self.user_id = user_information[0][0]
        Button(self.profile,text="Change my information", height="2", width="30", command=partial(self.updateUserInformation, user_information[0][0],
                                    firstname_entry, lastname_entry, phone_number_entry, email_address_entry, password_entry)).pack()
        # print (email_address_entry.get())
        sep1= Separator(self.profile, orient=tk.HORIZONTAL)
        sep1.pack(anchor="nw", fill=tk.X, pady=4)
        """
        ########################################################## 
        """
        
        """
        in this section we will show the user address
        ##########################################################3
        """
        Label(self.profile, text="Address Management", bg="red", width="300", height="2", font=("Calibri", 13)).pack()
        Label(text="").pack()
        show_address_button = Button(self.profile, text="Show Current added address", command=showAddress)
        show_address_button.pack()
        
        add_address_button = Button(self.profile, text="Add Address", command=self.addAddress)
        add_address_button.pack()
        
        edit_address_button = Button(self.profile, text="Edit Exists Address", command=self.editAddresses)
        edit_address_button.pack()
        """
        ########################################################## 
        """
    
    def deleteAddress(self, address_id):
        # print (address_id)
        mydb.deletAddress(address_id)


    def editAddresses(self):
        def updateAddress(i, x_entry, y_entry,city_combo, street_entry, alley_entry, plaque_entry, address_text_entry):

            x = x_entry.get()
            if (x_entry.get() == ""):
                x = None
            y = y_entry.get()

            if (y_entry.get() == ""):
                y = None
  
            if (city_combo.get() == "None"):
                city_id = None
            else :
                city_id = int(city_combo.get()[0])

            street = street_entry.get()
            if (street_entry.get()==""):
                street = None
            
            alley = alley_entry.get()
            if (alley_entry.get()==""):
                alley = None

            plaque = plaque_entry.get()
            if (plaque_entry.get() == ""):
                plaque = None
            
            address_text = address_text_entry.get()
            if (address_text_entry==""):
                address_text = None
            mydb.updateAddress(i, x, y, city_id, street, alley, plaque, address_text)
        addresses = mydb.showUserAddress(self.user_id)
        print (addresses)
        self.edit_address_screen = Tk()
        self.edit_address_screen.title("Edit Address")
        for i in range(len(addresses)):
            # print (i)
            # print (type(i))
            Label(self.edit_address_screen, text="Address#"+str(i+1)).pack()
            # show x
            Label(self.edit_address_screen, text="Address x:").pack()
            x_entry = Entry(self.edit_address_screen)
            x_entry.pack()
            # Show y
            Label(self.edit_address_screen, text="Address y:").pack()
            y_entry = Entry(self.edit_address_screen)
            y_entry.pack()
            # Show city
            Label(self.edit_address_screen, text="Choose your city, if not please select None").pack()
            city_combo = Combobox(self.edit_address_screen)
            cities = mydb.showAllCity()
            cities_list = []
            cities_list.append("None")
            
            for city in cities:
                cities_list.append(str(city[0]) + " " +city[1])
            
            city_combo['values']= cities_list
            city_combo.pack()
            city_combo.current(0)
            # Show Street
            Label(self.edit_address_screen, text="Address Street:").pack()
            street_entry = Entry(self.edit_address_screen)
            street_entry.pack()
            # Show Alley
            Label(self.edit_address_screen, text="Address Alley:").pack()
            alley_entry = Entry(self.edit_address_screen)
            alley_entry.pack()
            # Show Plaque
            Label(self.edit_address_screen, text="Address plaque:").pack()
            plaque_entry = Entry(self.edit_address_screen)
            plaque_entry.pack()
            # Show Address text
            Label(self.edit_address_screen, text="Address Text:").pack()
            address_text_entry = Entry(self.edit_address_screen)
            address_text_entry.pack()
            # Change button
            Button(self.edit_address_screen,text="Change my information", height="2", width="30", command=
            partial(updateAddress, addresses[i][1], x_entry, y_entry,city_combo, street_entry, alley_entry, plaque_entry, address_text_entry)).pack()
            # print (email_address_entry.get())



    def addAddress(self):
        def addNewAddress():
            mydb.addAddress(x_entry.get(), y_entry.get(), self.user_id, mydb.addCity(city_combo.get()), street_entry.get()
                            ,alley_entry.get(), plaque_entry.get(), other_information_entry.get())
        self.add_address_screen = Tk()
        self.add_address_screen.title("Adding new address")
        self.add_address_screen.geometry("700x500")
        Label(self.add_address_screen, text="First select your city and then").pack()
        city_combo = Combobox(self.add_address_screen)
        cities = mydb.showAllCity()
        cities_list = []
        for i in cities:
            cities_list.append(i[1])
        city_combo['values']= cities_list
        city_combo.pack()
        Label(self.add_address_screen, text="X:").pack()
        x_entry = Entry(self.add_address_screen)
        x_entry.pack()
        Label(self.add_address_screen, text="Y:").pack()
        y_entry = Entry(self.add_address_screen)
        y_entry.pack()
        Label(self.add_address_screen, text="Street:").pack()
        street_entry = Entry(self.add_address_screen)
        street_entry.pack()
        Label(self.add_address_screen, text="Alley:").pack()
        alley_entry = Entry(self.add_address_screen)
        alley_entry.pack()
        Label(self.add_address_screen, text="Plaque:").pack()
        plaque_entry = Entry(self.add_address_screen)
        plaque_entry.pack()
        Label(self.add_address_screen, text="Other information:").pack()
        other_information_entry = Entry(self.add_address_screen)
        other_information_entry.pack()
        add_address_button = Button(self.add_address_screen, text="Add This New Address", command=addNewAddress)
        add_address_button.pack()
        


    def updateUserInformation(self, user_id,firstname_entry, lastname_entry, phone_number_entry, email_address_entry, password_entry):
        try:
            mydb.updateUserProfile(user_id, firstname_entry.get(),lastname_entry.get(), phone_number_entry.get(), email_address_entry.get(), password_entry.get()) 
        except:
            print ("can't change the information")
        Label(self.profile, text="Changed seccussful").pack()



    def OnDoubleClick(self, tree,resturants, event):
        item = tree.identify('item',event.x,event.y)
        resturant_name = tree.item(item,"text")
        resturant_id = -1 
        for res in resturants:
            if (res[1] == resturant_name):
                resturant_id = res[0]
        # print (resturant_id)
        foods = mydb.showFoodsOfShop(resturant_id)
        self.menu_screen = Tk()
        self.menu_screen.title(resturant_name+" Menu")
        if (len(foods) != 0):
            
            Label(self.menu_screen, text="Resturant Menu", bg="red", width="300", height="2", font=("Calibri", 13)).pack()
            Label(text="").pack()
            tree=Treeview(self.menu_screen,style="mystyle.Treeview")
            tree["columns"]=("one","two","three", "four", "five")
            #set tree columns
            tree.column("#0", width=150, minwidth=150, stretch=tk.NO)
            tree.column("one", width=400, minwidth=200)
            tree.column("two", width=80, minwidth=50, stretch=tk.YES)
            tree.column("three", width=80, minwidth=50, stretch=tk.YES)
            tree.column("four", width=80, minwidth=50, stretch=tk.YES)
            tree.column("five", width=80, minwidth=50, stretch=tk.YES)
            #set tree's heading
            tree.heading("#0", text="Name",anchor=tk.W)
            tree.heading("one", text="Price",anchor=tk.W)
            tree.heading("two", text="About",anchor=tk.W)
            tree.heading("three", text="Category",anchor=tk.W)
            tree.heading("four", text="Image",anchor=tk.W)
            tree.heading("five", text="Discount",anchor=tk.W)
            tree.pack()
            for i in range(len(foods)):
                tree.insert("", i+1, text=foods[i][3], values=(foods[i][1], foods[i][2], mydb.showCategoryName(foods[i][6])[0][0], foods[i][5], foods[i][4]))
            tree.bind("<Double-1>", partial(self.OnDoubleClickOnFood,tree, foods))

        ######################################
        ######################################
        ######################################
        #LAST FOOD FORM THIS RESTURANT
        ######################################
        ######################################
        ######################################
        last_foods = mydb.showOrderByShop(self.user_id, resturant_id)
        last_foods = list(dict.fromkeys(last_foods))
        # print (last_foods)
        Label(self.menu_screen, text="Last orders from this resturant", bg="red", width="300", height="2", font=("Calibri", 13)).pack()
        Label(text="").pack()
        tree=Treeview(self.menu_screen,style="mystyle.Treeview")
        tree["columns"]=("one","two","three", "four", "five")
        #set tree columns
        tree.column("#0", width=150, minwidth=150, stretch=tk.NO)
        tree.column("one", width=400, minwidth=200)
        tree.column("two", width=80, minwidth=50, stretch=tk.YES)
        tree.column("three", width=80, minwidth=50, stretch=tk.YES)
        tree.column("four", width=80, minwidth=50, stretch=tk.YES)
        tree.column("five", width=80, minwidth=50, stretch=tk.YES)
        #set tree's heading
        tree.heading("#0", text="Name",anchor=tk.W)
        tree.heading("one", text="Price",anchor=tk.W)
        tree.heading("two", text="About",anchor=tk.W)
        tree.heading("three", text="Category",anchor=tk.W)
        tree.heading("four", text="Image",anchor=tk.W)
        tree.heading("five", text="Discount",anchor=tk.W)
        tree.pack()
        for i in range(len(last_foods)):
            tree.insert("", i+1, text=last_foods[i][3], values=(last_foods[i][1], last_foods[i][2], mydb.showCategoryName(last_foods[i][6])[0][0], last_foods[i][5], last_foods[i][4]))
        tree.bind("<Double-1>", partial(self.OnDoubleClickOnFood,tree, last_foods))
    
    def OnDoubleClickOnFood(self, tree,foods, event):
        item = tree.identify('item',event.x,event.y)
        food_name = tree.item(item,"text")
        food_id = -1
        for food in foods:
            if (food[1] == food_name):
                food_id = food[0]
                break
        #Add the food to cart
        self.cart_id = mydb.addFoodToCart(food_id, self.user_id)

    

    def showRestaurants(self, all_variables, all_address):

        address_id = -1
        for variable in all_variables:
            if (variable.get()):
                index = all_variables.index(variable)
                address_id = all_address[index][1]
                self.address_id = address_id
        resturants = mydb.searchShopByLocation(int(address_id), 100)
        # print (resturants)
        self.searched_resturant_screen = Tk()
        self.searched_resturant_screen.title("Results")
        tree=Treeview(self.searched_resturant_screen,style="mystyle.Treeview")
        tree["columns"]=("one","two","three", "four")
        #set tree columns
        tree.column("#0", width=270, minwidth=270, stretch=tk.NO)
        tree.column("one", width=150, minwidth=150, stretch=tk.NO)
        tree.column("two", width=400, minwidth=200)
        tree.column("three", width=400, minwidth=200, stretch=tk.YES)
        tree.column("four", width=80, minwidth=50, stretch=tk.YES)

        #set tree's heading
        tree.heading("#0",text="Name",anchor=tk.W)
        tree.heading("one", text="About",anchor=tk.W)
        tree.heading("two", text="min bill value",anchor=tk.W)
        tree.heading("three", text="address",anchor=tk.W)
        tree.heading("four", text="rate",anchor=tk.W)
        list_of_resturant_in_treeview = []
        for i in range(len(resturants)):
            rate = mydb.calculateRate(resturants[i][0])[0][0]
            resturant_in_treeview = tree.insert("", i+1, text=resturants[i][1], values=(resturants[i][2], resturants[i][3], self.make_address_str(resturants[i][4]), "-" if rate== None else rate))
            list_of_resturant_in_treeview.append(resturant_in_treeview)
        tree.pack(side=tk.TOP,fill=tk.X)
        tree.bind("<Double-1>", partial(self.OnDoubleClick,tree, resturants))

        
    def restaurantsPage(self):      
        self.address_selection_screen = Tk()
        self.address_selection_screen.title("Your addresses")
        self.address_selection_screen.geometry("700x500")
        Label(self.address_selection_screen, text="Choose an address to find the nearest resturant to you", bg="yellow", width="300", height="2", font=("Calibri", 13)).pack()
        Label(text="").pack()
        all_address = mydb.showUserAddress(self.user_id)
        # print (all_address)
        all_variables = []

        list_of_address_str = []
        for address in all_address:
            address_str = ""
            for part in address[1:-2]:
                address_str += str(part) + ", "
                list_of_address_str.append(address_str)
            vari = IntVar(self.address_selection_screen)
            all_variables.append(vari)
            Checkbutton(self.address_selection_screen, text=address_str, variable=vari).pack()        
        Button(self.address_selection_screen, text="Submit", command=partial(self.showRestaurants, all_variables, all_address) ).pack()


    def make_address_str(self, address_id):
        address_info = mydb.showAddress(address_id)
        address_info = address_info[0]
        address_str = address_info[0] + ", "
        # print (address_info)
        for i in range(2,6):
            address_str += address_info[i] + ", "
        # print (address_str)
        return address_str

    def make_foods_str(self, foods_list):
        food_str_dict = {}
        for food in foods_list:
            food_str = mydb.showFoods([food])[0][3]
            if food_str in food_str_dict.keys():
                food_str_dict[food_str] += 1
            else:
                food_str_dict[food_str] = 1

        return_str = ""
        for food_name in list(food_str_dict.keys()):
            return_str += food_name + ": "
            return_str += str(food_str_dict[food_name]) + "  "
        return return_str

    def saveComment(self, order_id, comment_entry, rate_entry):
        mydb.addComment(order_id, rate_entry.get(), comment_entry.get())


    def orderPage(self):
        def OnDoubleClickOnOrder(tree, orders_list, event):
            item = tree.identify('item',event.x,event.y)
            order_number = tree.item(item,"text")
            
            order_id = orders_list [int(order_number[-1]) - 1]
            self.order_comment_page = Tk()
            self.order_comment_page.title("Comment")
            Label(self.order_comment_page, text="Comment on this order", bg="yellow", width="300", height="2", font=("Calibri", 13)).pack()
            Label(text="").pack()
            Label(self.order_comment_page, text="Your comment:").pack()
            comment_entry = Entry(self.order_comment_page)
            comment_entry.pack()
            Label(self.order_comment_page, text="Your rating to this order(from 0 to 100):").pack()
            rate_entry = Entry(self.order_comment_page)
            rate_entry.pack()
            Button(self.order_comment_page, text="comment this", command=partial(self.saveComment, order_id, comment_entry, rate_entry)).pack()


            

        def showHistoryOfOrders():
            self.history_of_orders_screen = Tk()
            self.history_of_orders_screen.title("Hisotry of orders")
            Label(self.history_of_orders_screen, text="History of orders, click on them to comment", bg="yellow", width="300", height="2", font=("Calibri", 13)).pack()
            Label(text="").pack()
            tree=Treeview(self.history_of_orders_screen, style="mystyle.Treeview")
            tree["columns"]=("one","two","three")
            #set tree columns
            tree.column("#0", width=270, minwidth=270, stretch=tk.NO)
            tree.column("one", width=150, minwidth=150, stretch=tk.NO)
            tree.column("two", width=400, minwidth=200)
            tree.column("three", width=80, minwidth=50, stretch=tk.YES)
            #set tree's heading
            tree.heading("#0",text="Order#",anchor=tk.W)
            tree.heading("one", text="Total Price",anchor=tk.W)
            tree.heading("two", text="Address",anchor=tk.W)
            tree.heading("three", text="Foods",anchor=tk.W)
            history_of_orders = mydb.showBuyHistory(self.user_id)
            invoic_dict = {}
            for history in history_of_orders:
                if ((history[0],history[1],history[2]) in invoic_dict.keys()):
                    invoic_dict[(history[0],history[1],history[2])].append(history[3])
                else:
                    invoic_dict[(history[0],history[1],history[2])] = []
                    invoic_dict[(history[0],history[1],history[2])].append(history[3])
            
            # print (type(list(invoic_dict.keys())))
            # print (invoic_dict)

            tree.pack(side=tk.TOP,fill=tk.X)
            orders_list = []
            for key in invoic_dict.keys():
                orders_list.append(key[0])
            for i in range(len(list(invoic_dict.keys()))):
                address_id = list(invoic_dict.keys())[i][2]
                foods_list = invoic_dict[list(invoic_dict.keys())[i]]
                print (foods_list)
                tree.insert("", i+1, text="Order#"+str(i+1), values=(list(invoic_dict.keys())[i][1], self.make_address_str(address_id), self.make_foods_str(foods_list)))
            # resturant_in_treeview = tree.insert("", i+1, text=resturants[i][1], values=(resturants[i][2], resturants[i][3], make_address_str(resturants[i][4])))
            # list_of_resturant_in_treeview.append(resturant_in_treeview)
            tree.bind("<Double-1>", partial(OnDoubleClickOnOrder,tree, orders_list))
        
        
        def finilizeCart(discount_code):
            # print (self.address_id)
            self.ivoice_id = mydb.finalizeCart(self.user_id, self.address_id, discount_code.get())

        def showAllOrders():
            self.all_orders_screen = Tk()
            self.all_orders_screen.title("All Orders")
            all_history = mydb.showAllHistory(self.user_id)
            print (all_history)
            Label(self.all_orders_screen, text="All your orders", bg="yellow", width="300", height="2", font=("Calibri", 13)).pack()
            Label(text="").pack()
            tree=Treeview(self.all_orders_screen, style="mystyle.Treeview")
            tree["columns"]=("one","two","three", "four")
            #set tree columns
            tree.column("#0", width=270, minwidth=270, stretch=tk.NO)
            tree.column("one", width=150, minwidth=150, stretch=tk.NO)
            tree.column("two", width=400, minwidth=200)
            tree.column("three", width=80, minwidth=50, stretch=tk.YES)
            tree.column("four", width=80, minwidth=50, stretch=tk.YES)
            #set tree's heading
            tree.heading("#0",text="Order#",anchor=tk.W)
            tree.heading("one", text="Total Price",anchor=tk.W)
            tree.heading("two", text="Address",anchor=tk.W)
            tree.heading("three", text="Status",anchor=tk.W)
            tree.heading("four", text="Foods",anchor=tk.W)
            invoic_dict = {}
            print(all_history)
            for history in all_history:
                if ((history[0],history[1],history[2], history[4]) in invoic_dict.keys()):
                    invoic_dict[(history[0],history[1],history[2], history[4])].append(history[3])
                else:
                    invoic_dict[(history[0],history[1],history[2], history[4])] = []
                    invoic_dict[(history[0],history[1],history[2], history[4])].append(history[3])
            
            # print (type(list(invoic_dict.keys())))
            print (invoic_dict)

            tree.pack(side=tk.TOP,fill=tk.X)
            orders_list = []
            for key in invoic_dict.keys():
                orders_list.append(key[0])
            for i in range(len(list(invoic_dict.keys()))):
                address_id = list(invoic_dict.keys())[i][2]
                foods_list = invoic_dict[list(invoic_dict.keys())[i]]
                print (foods_list)
                tree.insert("", i+1, text="Order#"+str(i+1), values=(list(invoic_dict.keys())[i][1], self.make_address_str(address_id),list(invoic_dict.keys())[i][3] ,self.make_foods_str(foods_list)))
            # resturant_in_treeview = tree.insert("", i+1, text=resturants[i][1], values=(resturants[i][2], resturants[i][3], make_address_str(resturants[i][4])))
            # list_of_resturant_in_treeview.append(resturant_in_treeview)


        self.order_screen = Tk()
        self.order_screen.title("Orders Page")
        Label(self.order_screen, text="Finilize your Cart", bg="red", width="300", height="2", font=("Calibri", 13)).pack()
        Label(text="").pack()
        Label(self.order_screen, text="enter your discount code if you have one").pack()
        discount_code = Entry(self.order_screen)
        discount_code.pack()
        Button(self.order_screen,text="Buy your Cart", height="2", width="30", command=partial(finilizeCart, discount_code)).pack()
        Label(self.order_screen, text="Your Orders History (Compeleted)", bg="red", width="300", height="2", font=("Calibri", 13)).pack()
        Label(text="").pack()
        Button(self.order_screen,text="history of orders", height="2", width="30", command=showHistoryOfOrders).pack()
        Label(self.order_screen, text="Your All Orders", bg="red", width="300", height="2", font=("Calibri", 13)).pack()
        Label(text="").pack()
        Button(self.order_screen,text="All Orders", height="2", width="30", command=showAllOrders).pack()

root = Tk()
my_gui = Application(root)
root.mainloop()