from tkinter import *
import pymongo
from pymongo import MongoClient
from werkzeug.security import generate_password_hash ,check_password_hash
from os import path


##database init
cluster= MongoClient("mongodb+srv://dvirbens:<password>@dvirbens.d7gwq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db=cluster["spreadApp"]
collection=db["Users"]


## login area
def Login():
    global login_screen

    login_screen=Tk()
    login_screen.geometry('260x250')
    login_screen.title("Account Manager")
    login_screen.iconbitmap('accman.ico')

    #user enter
    username_label=Label(login_screen,text="User name:").grid(row=0,column=0,padx=10,pady=5)
    e_username=Entry(login_screen,width=25)
    e_username.grid(row=0,column=1,padx=10,pady=5)
    
    #password enter
    password_label=Label(login_screen,text="Password:").grid(row=1,column=0,padx=10,pady=5)
    e_password=Entry(login_screen,show='*',width=25)
    e_password.grid(row=1,column=1,padx=10,pady=5)

    #sumbit button
    sumbit_button=Button(login_screen,text="Login",width=10,command= lambda: login_func(e_username.get(),e_password.get()))
    sumbit_button.grid(row=2,column=0,columnspan=2,padx=10,pady=5,ipadx=30)


    #exit button
    Label(login_screen,text="").grid(row=3,column=1,pady=5)
    exit_button=Button(login_screen,width=10,text="Exit",command= lambda:login_screen.destroy()).grid(row=4,column=0,columnspan=2,padx=10,pady=5,ipadx=30)


#login function - function that let only admin user to loging the system.
def login_func(username,password):
  
    res=collection.find_one({"user_name":username})

    if res:
        if res["adminAccess"]==True:
            if check_password_hash(res["password"], password):
                label_mass=Label(login_screen,text="Login success",width=20,fg="green").grid(row=3,column=0,columnspan=2,padx=10,pady=5)
                manu_manager()
            else: 
                label_mass=Label(login_screen,text="Worng password ",width=20,fg="red").grid(row=3,column=0,columnspan=2,padx=10,pady=5)
        else:
            label_mass=Label(login_screen,text="User has no accsees",width=20,fg="red").grid(row=3,column=0,columnspan=2,padx=10,pady=5)

    else: 
        label_mass=Label(login_screen,text="User not found",width=20,fg="red").grid(row=3,column=0,columnspan=2,padx=10,pady=5)


##  Manager manu
def manu_manager():
    menu_screen=Toplevel()
    menu_screen.title=("Account Manager")
    menu_screen.iconbitmap('accman.ico')
    menu_screen.geometry('300x300')

    menu_label=Label(menu_screen,text="Select an option:",font = "Helvetica 10 bold ").pack()
    newAccount_button=Button(menu_screen,width=20,text="Create new account",command=lambda:create_account()).pack(pady=10)
    deleteAccount_button=Button(menu_screen,width=20,text="Delete account",command=lambda: delete_account()).pack(pady=10)
    updateAccount_button=Button(menu_screen,width=20,text="Change account",command=lambda:change_user()).pack(pady=10)
    getusers_button=Button(menu_screen,text="Get accounts report",width=20,command=lambda:get_users()).pack(pady=10)
    
    exit_button=Button(menu_screen,text="Exit",command=menu_screen.destroy,width=20).pack(side=BOTTOM,pady=10)


### Delete account Scene ####

#Delete account screen
def delete_account():
    global delete_screen
    delete_screen=Toplevel()
    delete_screen.title=("Account Manager")
    delete_screen.iconbitmap('accman.ico')
    delete_screen.geometry('300x200')
    Label(delete_screen,text="Enter User-name to delete").pack()
    e=Entry(delete_screen) 
    e.pack()
    delete_button=Button(delete_screen,width=15,text="Delete",command= lambda: delete_func(e.get())).pack()


#Delete account function - delete an existing account from database.
def delete_func(user):
    res= collection.find_one({"user_name":user})
    if res:
        collection.delete_one(res)
        Label(delete_screen,text="User deleted",width=20,fg="green").pack()

    else:
        Label(delete_screen,text="User not found",width=20,fg="red").pack()



### Create account Scene ####

#Create account screen
def create_account():
    global create_screen
    create_screen=Toplevel()
    create_screen.title=("Account Manager")
    create_screen.iconbitmap('accman.ico')
    create_screen.geometry('300x200')
    createuser_laber=Label(create_screen,text="Create Account",font = "Helvetica 10 bold ").grid(row=0,column=0,columnspan=2)

    #user enter
    username_label=Label(create_screen,text="User name:").grid(row=1,column=0)
    e_createUsername=Entry(create_screen)
    e_createUsername.grid(row=1,column=1)
    
    #password enter
    password_label=Label(create_screen,text="Password:").grid(row=2,column=0)
    e_createPassword=Entry(create_screen,show='*')
    e_createPassword.grid(row=2,column=1)


    #check box to ask if the new user will have admin accses or not.
    var=IntVar()
    checkbox_useraccses=Checkbutton(create_screen,text="Let Administrator privileges",variable=var)
    checkbox_useraccses.grid(row=3,column=0,columnspan=2,padx=10,pady=5)
    
    #sumbit button
    sumbit_button=Button(create_screen,width=15,text="Create",command=lambda:create_func(e_createUsername.get(),e_createPassword.get(), var.get()))
    sumbit_button.grid(row=4,column=0,columnspan=2,padx=10,pady=5)


#Create account function - adding the new account to the database.
def create_func(username,password,accses):
    res=collection.find_one({"user_name":username})
    if res:
        Label(create_screen,text="User already exist",width=40,fg="red").grid(row=5,column=0,columnspan=2,padx=10,pady=5)

    elif (len(password)<7):
        Label(create_screen,text="Password must be atleat 7 characters ",width=40,fg="red").grid(row=5,column=0,columnspan=2,padx=10,pady=5)
    elif accses==1:
        collection.insert_one({"user_name":username,"password":generate_password_hash(password,method='sha256'),"adminAccess":True})
        Label(create_screen,text="User created",width=40,fg="green").grid(row=5,column=0,columnspan=2,padx=10,pady=5)
    else:
        collection.insert_one({"user_name":username,"password":generate_password_hash(password,method='sha256'),"adminAccess":False})
        Label(create_screen,text="User created",width=40,fg="green").grid(row=5,column=0,columnspan=2,padx=10,pady=5)



def change_user():
    changeUser_screen=Toplevel()
    changeUser_screen.title=("Account Manger")
    changeUser_screen.iconbitmap('accman.ico')
    changeUser_screen.geometry('300x400')
    Label(changeUser_screen,text="Enter User-name to update:").grid(row=0,column=0)
    user_e=Entry(changeUser_screen,width=20)
    user_e.grid(row=0,column=1)
    res=collection.find_one({"user_name":user_e.get()})
    if res:
        #update_menu()
        return
    else:
        Label(changeUser_screen,text="User not found",fg="red").grid(row=1,column=0,columnspan=2)    


# get users function- prints all the users and thir info to the system.
def get_users():
    usersinfo_screen=Toplevel()
    usersinfo_screen.title=("Account Manager")
    usersinfo_screen.iconbitmap('accman.ico')
    usersinfo_screen.geometry('300x400')

    res=collection.find({})
    Label(usersinfo_screen,text="User Name",font = "Helvetica 10 bold ").grid(row=0,column=0,padx=15)
    Label(usersinfo_screen,text="Admin accses",font = "Helvetica 10 bold ").grid(row=0,column=1)
    i=0
    for user in res:
        i+=1
        Label(usersinfo_screen,text=user["user_name"]).grid(row=i,column=0,padx=15)
        if user["adminAccess"]==True:
            Label(usersinfo_screen,text="On",fg="green").grid(row=i,column=1)
        else:    
            Label(usersinfo_screen,text="Off",fg="red").grid(row=i,column=1)

Login()

mainloop()







