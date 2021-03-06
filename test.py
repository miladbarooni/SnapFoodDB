from tkinter import Tk, Label, Button, Toplevel, StringVar, Entry, messagebox, Frame, END, Scrollbar, Y, RIGHT

from functools import partial
import tkinter as tk
from tkinter.ttk import Separator, Style, Combobox
from time import sleep
from snapFood import *

mydb = SnapFoodDB()




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
        

    def loadingPage(self):
        loader = Tk()
        loader.title("loading")
        # root.attributes('-alpha', 1.0)

    def makeMainWindow(self):
        
        self.master.geometry("300x250")

        self.master.title("Account Login")
        
        Label(text="Select Your Choice", bg="blue", width="300", height="2", font=("Calibri", 13)).pack()
        Label(text="").pack()
        Button(text="Login", height="2", width="30", command = self.loginPage).pack()
        Label(text="").pack()
        Button(text="Register", height="2", width="30", command=self.registerPage).pack()
        
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

        # print (username_entry.get())
        # print (password_entry.get())
        # print (firstname_entry.get())
    


    def dashboardPage(self):
        self.master.destroy
        self.login_screen.destroy
        self.dashboard = Tk()
        self.dashboard.title("User Dashboard")
        self.dashboard.geometry("300x250")

        Label(self.dashboard, text="Select Your Choice", bg="blue", width="300", height="2", font=("Calibri", 13)).pack()
        Label(text="").pack()
        Button(self.dashboard,text="Profile", height="2", width="30", command = self.profilePage).pack()
        Label(text="").pack()
        Button(self.dashboard,text="Restaurants", height="2", width="30", command=self.restaurantsPage).pack()
        Label(text="").pack()
        Button(self.dashboard,text="Order", height="2", width="30", command=self.orderPage).pack()
        
        closeButton = Button(self.dashboard, text="Exit", command=self.dashboard.destroy, width="200", height="2")
        closeButton.pack()

    def profilePage(self):
        def showAddress():
            self.current_address_screen = Tk()
            addresses = mydb.showAddress(self.user_id)
            print (addresses)
            for i in range(len(addresses)):
                Label(self.current_address_screen, text="Address #"+str(i+1)+":").pack()
                address_str = ""
                for j in range(1,5):
                    address_str+= addresses[i][j] + " "
                Label(self.current_address_screen, text=address_str).pack()
        # self.dashboard.destroy()
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
        """
        ########################################################## 
        """
        
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
    

    def restaurantsPage(self):
        self.address_selection_screen = Tk()
        self.address_selection_screen.title("Your addresses")
        
        
    
    def orderPage(self):
        def showHistoryOfOrders():
            print ("show history")
        self.order_screen = Tk()
        self.order_screen.title("Orders Page")
        Button(self.order_screen,text="history of orders", height="2", width="30", command=showHistoryOfOrders).pack()
    





root = Tk()
my_gui = Application(root)
root.mainloop()
