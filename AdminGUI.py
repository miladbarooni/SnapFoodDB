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
        def loginVarify():
            admin_details = mydb.adminLogin(username_login_entry.get())
            self.shop_id = admin_details[0][2]
            if (password_login_entry.get() == admin_details[0][1]):
                self.dashboardPage()
            else:
                messagebox.showinfo('Username/Password incorrect', 'your username of password is incorrect')
        self.login_screen = Tk()
        self.login_screen.title("Login")
        self.login_screen.geometry("300x250")
        Label(self.login_screen, text="Please enter details below to login").pack()
        Label(self.login_screen, text="").pack()


        username_verify = StringVar()
        password_verify = StringVar()


        Label(self.login_screen, text="Username * ").pack()
        username_login_entry = Entry(self.login_screen, textvariable=username_verify)
        username_login_entry.pack()
        Label(self.login_screen, text="").pack()
        Label(self.login_screen, text="Password * ").pack()
        password_login_entry = Entry(self.login_screen, textvariable=password_verify, show= '*')
        password_login_entry.pack()
        Label(self.login_screen, text="").pack()
        Button(self.login_screen, text="Login", width=10, height=1, command=loginVarify).pack()
    def registerPage(self):
        
        def registerAdminAndShop():
            mydb.addShopAndAdmin(username_entry.get(), password_entry.get(), int(city_combo.get()[0]), int(x_entry.get()),int(y_entry.get()),
            shop_name_entry.get(), about_entry.get(), int(min_bill_value_entry.get()), street_entry.get(), alley_entry.get(), plaque_entry.get(), address_entry.get())


        self.register_screen = Tk()
        self.register_screen.title("Register")
        self.register_screen.geometry("300x700")

        

        Label(self.register_screen, text="Please enter details below", bg="blue").pack()
        Label(self.register_screen, text="").pack()
        
        #Username
        Label(self.register_screen, text="Username * ").pack()
        username_entry = Entry(self.register_screen)
        username_entry.pack()
        #password
        Label(self.register_screen, text="Password * ").pack()
        password_entry = Entry(self.register_screen,show='*')
        password_entry.pack()
        #repeat password
        Label(self.register_screen, text="Repeat Password * ").pack()
        repeat_password_entry = Entry(self.register_screen,show='*')
        repeat_password_entry.pack()
        #chose the city
        Label(self.register_screen, text="Choose a city *").pack()
        city_combo = Combobox(self.register_screen)
        cities = mydb.showAllCity()
        print (cities)
        self.number_of_cities = len(cities)
        cities_list = []
        
        for i in cities:
            cities_list.append(str(i[0]) +" " +i[1])
        city_combo['values']= cities_list
        city_combo.pack()
        #x 
        Label(self.register_screen, text="X *").pack()
        x_entry = Entry(self.register_screen)
        x_entry.pack()
        #y
        Label(self.register_screen, text="Y * ").pack()
        y_entry = Entry(self.register_screen)
        y_entry.pack() 
        #shop name
        Label(self.register_screen, text="Shop name *").pack()
        shop_name_entry = Entry(self.register_screen)
        shop_name_entry.pack() 
        #shop about
        Label(self.register_screen, text="About your shop *").pack()
        about_entry = Entry(self.register_screen)
        about_entry.pack()
        #min bill value
        Label(self.register_screen, text="Type your min bill value *").pack()
        min_bill_value_entry = Entry(self.register_screen)
        min_bill_value_entry.pack()
        #Street
        Label(self.register_screen, text="Enter your Street *").pack()
        street_entry = Entry(self.register_screen)
        street_entry.pack()
        #Alley
        Label(self.register_screen, text="Enter your Alley *").pack()
        alley_entry = Entry(self.register_screen)
        alley_entry.pack()
        #Plaque
        Label(self.register_screen, text="Enter your Plaque *").pack()
        plaque_entry = Entry(self.register_screen)
        plaque_entry.pack()
        
        #Other address
        Label(self.register_screen, text="Enter you other Address info * ").pack()
        address_entry = Entry(self.register_screen)
        address_entry.pack()

        Label(self.register_screen, text="").pack()
        Button(self.register_screen, text="Register", width=10, height=1, bg="blue", command =registerAdminAndShop).pack()


    def dashboardPage(self):
        self.dashboard_screen = Tk()
        self.dashboard_screen.title("Dashboard")
        Label(self.dashboard_screen, text="Select Your Choice", bg="blue", width="300", height="2", font=("Calibri", 13)).pack()
        Label(text="").pack()

        Button(self.dashboard_screen,text="Show all Foods", height="2", width="30", command=self.showFoods).pack()
        Label(text="").pack()
        Button(self.dashboard_screen,text="Edit Current Foods", height="2", width="30", command=self.editFood).pack()
        Button(self.dashboard_screen,text="Add food", height="2", width="30", command=self.addFood).pack()
        Button(self.dashboard_screen,text="Preparing orders", height="2", width="30", command=self.preparingOrders).pack()
        Button(self.dashboard_screen,text="All Compelete orders", height="2", width="30", command=self.allOrders).pack()
        Button(self.dashboard_screen,text="Show comments", height="2", width="30", command=self.showComment).pack()
        
        closeButton = Button(self.dashboard_screen, text="Exit", command=self.dashboard_screen.destroy, width="200", height="2")
        closeButton.pack()

    def editFood(self):
        def updateFood(food_id, price_entry, about_entry,city_combo, discount_entry, name_entry):
            if (city_combo.get() == ""):
                cat_id = ""
            else:
                cat_id = int(city_combo.get()[0])
            mydb.updateFood(food_id, price_entry.get(), about_entry.get(), name_entry.get(), discount_entry.get(),cat_id,"")
        foods = mydb.showFoodsOfShop(self.shop_id)
        print (foods)
        self.edit_food_screen = Tk()
        self.edit_food_screen.title("Edit Food")
        for i in range(len(foods)):
            Label(self.edit_food_screen, text="Food#"+str(i+1)).pack()
            # show price
            Label(self.edit_food_screen, text="Food Price:").pack()
            price_entry = Entry(self.edit_food_screen)
            price_entry.pack()
            # Show about
            Label(self.edit_food_screen, text="Food About:").pack()
            about_entry = Entry(self.edit_food_screen)
            about_entry.pack()
            # Show categori
            Label(self.edit_food_screen, text="Choose a Categori").pack()
            city_combo = Combobox(self.edit_food_screen)
            cities = mydb.showAllCategory()
            cities_list = []
            print(cities)
            for city in cities:
                cities_list.append(str(city[0]) + " " +city[1])
            
            city_combo['values']= cities_list
            city_combo.pack()
            # Show discount
            Label(self.edit_food_screen, text="Food Discount:").pack()
            discount_entry = Entry(self.edit_food_screen)
            discount_entry.pack()
            # Show food Name
            Label(self.edit_food_screen, text="Food Name:").pack()
            name_entry = Entry(self.edit_food_screen)
            name_entry.pack()

            # Change button
            Button(self.edit_food_screen,text="Change my information", height="2", width="30", command=
            partial(updateFood, foods[i][0], price_entry, about_entry,city_combo, discount_entry, name_entry)).pack()
            # print (email_address_entry.get())

    def registerUser(self ,phone_number_entry, password_entry, repeat_password_entry, firstname_entry, lastname_entry, email_entry):
        #insert into database 
        if (password_entry.get() == repeat_password_entry.get()):
            mydb.registerUser( phone_number_entry.get(), password_entry.get(),firstname_entry.get(), lastname_entry.get(), email_entry.get())
            Label(self.register_screen, text="Register was Seccesful").pack()
        else:
            messagebox.showinfo('Repeat password again', 'your repeated password doesn\'n match your entered password, Try Again')


    def showFoods(self):
        self.show_food_screen = Tk()
        self.show_food_screen.title("Foods")
        foods = mydb.showFoodsOfShop(self.shop_id)
        print (foods)
        Label(self.show_food_screen, text="All foods, double click to delete", bg="red", width="300", height="2", font=("Calibri", 13)).pack()
        Label(text="").pack()
        tree=Treeview(self.show_food_screen,style="mystyle.Treeview")
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
            tree.insert("", i+1, text=foods[i][3], values=(foods[i][1], foods[i][2], mydb.showCategoryName(foods[i][6]), foods[i][5], str(foods[i][4])))
        tree.bind("<Double-1>", partial(self.OnDoubleClickDeleteFood,tree,foods))

    def OnDoubleClickDeleteFood(self, tree,foods, event):
        item = tree.identify('item',event.x,event.y)
        food_name = tree.item(item,"text")
        for food in foods:
            if food[3] == food_name:
                food_id = food[0]
        mydb.deleteFood(food_id)


    def addFood(self):

        def addNewFood():
            mydb.addFood(price_entry.get(), about_entry.get(), name_entry.get(), discount_entry.get(), cat_combo.get()[0], self.shop_id)



        self.add_food_screen = Tk()
        self.add_food_screen.title("Add a new food")
        # mydb.addFood()
        #price
        Label(self.add_food_screen, text="Add A price for your food").pack()
        price_entry = Entry(self.add_food_screen)
        price_entry.pack()
        #about
        Label(self.add_food_screen, text="About your food").pack()
        about_entry = Entry(self.add_food_screen)
        about_entry.pack()
        #Name
        Label(self.add_food_screen, text="Choose a name").pack()
        name_entry = Entry(self.add_food_screen)
        name_entry.pack()
        #Discount
        Label(self.add_food_screen, text="Enter a discount").pack()
        discount_entry = Entry(self.add_food_screen)
        discount_entry.pack()
        #Categori
        Label(self.add_food_screen, text="choose a category").pack()
        cat_combo = Combobox(self.add_food_screen)
        catogries = mydb.showAllCategory()
        self.number_of_catogry = len(catogries)
        catogri_list = []
        print (catogries)
        for i in catogries:
            catogri_list.append(str(i[0])+ " "+ i[1])
        cat_combo['values']= catogri_list
        cat_combo.pack()
        Button(self.add_food_screen, text="add new food", command=addNewFood).pack()

    

    def preparingOrders(self):
        self.prepare_screen = Tk()
        self.prepare_screen.title("Preparing")
        all_history = mydb.showActiveOrder(self.shop_id)
        print (all_history)
        Label(self.prepare_screen, text="All your orders", bg="yellow", width="300", height="2", font=("Calibri", 13)).pack()
        Label(text="").pack()
        tree=Treeview(self.prepare_screen, style="mystyle.Treeview")
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
            order_number = list(invoic_dict.keys())[i][0]
            address_id = list(invoic_dict.keys())[i][2]
            foods_list = invoic_dict[list(invoic_dict.keys())[i]]
            print (foods_list)
            tree.insert("", i+1, text="Order#"+str(order_number), values=(list(invoic_dict.keys())[i][1], self.make_address_str(address_id),list(invoic_dict.keys())[i][3] ,self.make_foods_str(foods_list)))
        tree.bind("<Double-1>", partial(self.OnDoubleClickChangeStatus,tree))
    
    def OnDoubleClickChangeStatus(self, tree, event):
        item = tree.identify('item',event.x,event.y)
        status = tree.set(tree.identify_row(event.y))['three']
        order_name = tree.item(item,"text")
        order_number = int(order_name[order_name.index("#")+1:])
        if (status == "Prepration"):
            mydb.setStateToSending(order_number)
        elif (status=="Sending"):
            mydb.setStateToComplete(order_number)
    
    def allOrders(self):
        self.all_orders_screen = Tk()
        self.all_orders_screen.title("All Orders")
        all_history = mydb.showShopHistory(self.shop_id)
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
        # print (invoic_dict)

        tree.pack(side=tk.TOP,fill=tk.X)
        orders_list = []
        for key in invoic_dict.keys():
            orders_list.append(key[0])
        for i in range(len(list(invoic_dict.keys()))):
            order_number = list(invoic_dict.keys())[i][0]
            address_id = list(invoic_dict.keys())[i][2]
            foods_list = invoic_dict[list(invoic_dict.keys())[i]]
            print (foods_list)
            tree.insert("", i+1, text="Order#"+str(order_number), values=(list(invoic_dict.keys())[i][1], self.make_address_str(address_id),list(invoic_dict.keys())[i][3] ,self.make_foods_str(foods_list)))

    def showComment(self):
        self.show_comment_screen = Tk()
        self.show_comment_screen.title("comments")
        comments = mydb.showAllComments(self.shop_id)
        comments = list(dict.fromkeys(comments))
        Label(self.show_comment_screen, text="All your Comments", bg="yellow", width="300", height="2", font=("Calibri", 13)).pack()
        Label(text="").pack()
        tree=Treeview(self.show_comment_screen, style="mystyle.Treeview")
        tree["columns"]=("one")
        #set tree columns
        tree.column("#0", width=270, minwidth=270, stretch=tk.NO)
        tree.column("one", width=150, minwidth=150, stretch=tk.NO)
        
        #set tree's heading
        tree.heading("#0",text="Comment",anchor=tk.W)
        tree.heading("one", text="Rate",anchor=tk.W)


        for i in range(len(comments)):
            tree.insert("", 1, text=comments[i][4], values=(comments[i][5]))
        tree.pack(side=tk.TOP,fill=tk.X)


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

root = Tk()
my_gui = Application(root)
root.mainloop()