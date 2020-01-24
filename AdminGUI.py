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
        Button(self.dashboard_screen,text="Profile", height="2", width="30", command = self.profilePage).pack()
        Label(text="").pack()
        Button(self.dashboard_screen,text="Foods (add, delete)", height="2", width="30", command=self.foodsPage).pack()
        Label(text="").pack()
        Button(self.dashboard_screen,text="Order", height="2", width="30", command=self.orderPage).pack()
        Button(self.dashboard_screen,text="Search", height="2", width="30", command=self.searchFoodOrShop).pack()
        Button(self.dashboard_screen,text="Charge your wallet", height="2", width="30", command=self.chargeWallet).pack()
        
        closeButton = Button(self.dashboard_screen, text="Exit", command=self.dashboard_screen.destroy, width="200", height="2")
        closeButton.pack()


    def registerUser(self ,phone_number_entry, password_entry, repeat_password_entry, firstname_entry, lastname_entry, email_entry):
        #insert into database 
        if (password_entry.get() == repeat_password_entry.get()):
            mydb.registerUser( phone_number_entry.get(), password_entry.get(),firstname_entry.get(), lastname_entry.get(), email_entry.get())
            Label(self.register_screen, text="Register was Seccesful").pack()
        else:
            messagebox.showinfo('Repeat password again', 'your repeated password doesn\'n match your entered password, Try Again')

    def addFood(self):
        print ("add food")

    def profilePage(self):
        print ("Profile page")

    
root = Tk()
my_gui = Application(root)
root.mainloop()