#!/usr/bin/python

my_dict = dict()
username = "0"
while not username == "-1":
    print("If you do not want to continue, enter -1")
    username = str(raw_input("Enter your username : "))
    if(username == "-1"):
        break
    password = str(raw_input("Enter password: "))

    my_dict[username] = password

up_username = str(raw_input("Username: "))
up_password = str(raw_input("Password: "))

login = 0
check = "-1"
for key in my_dict:
    if(key == up_username):
        login = 1
        check = my_dict.get(key)

if(login == 0):
    print("Try again")
if(login == 1):
    if(check == up_password):
        print("Login successful")
    else:
        print("Try again")



        


