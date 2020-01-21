from tkinter import Tk, Label, Button, Toplevel, StringVar, Entry, messagebox, Frame, END
from functools import partial
import tkinter as tk
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
        print("Width",windowWidth,"Height",windowHeight)
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
        print (username_verify.get())
        Button(self.login_screen, text="Login", width=10, height=1, command = partial(self.loginVerify, username_login_entry, password_login_entry)).pack()
        

    def loginVerify(self, username_login_entry, password_login_entry):
        # self.db_cursor.execute("SELECT userid, password FROM USER WHERE userid=\'{}\'".format(username_login_entry.get()))
       
        user_id = mydb.login(username_login_entry.get())
        self.phone_number = username_login_entry.get()
        #check whether user_id exists or not
        if (len(user_id) != 0 and user_id[0][1] == password_login_entry.get()):
            
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
        # self.dashboard.destroy()
        self.profile = Tk()
        self.profile.title("User Profile")
        self.profile.geometry("700x500")
        # Show yoru Username
        Label(self.profile, text="You Username").pack()
        username_entry = Entry(self.profile)
        username_entry.pack()
        username = "hello"
        username_entry.insert(END, username)

    def restaurantsPage(self):
        print ("resturantsPage")
    
    def orderPage(self):
        print ("orderPage")
    





root = Tk()
my_gui = Application(root)
root.mainloop()