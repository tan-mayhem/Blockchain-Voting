#!/usr/bin/python
import base64
import getpass
#from databaseauth import databaseinfo

def create():
    username = "0"
    file = open("userpass.txt","a")
    while not username == "-1":
        print("If you do not want to continue, enter -1")
        username = str(raw_input("Enter your username : ").strip())
        if(username == "-1"):
            break
        else:
            password = getpass.getpass().strip()
            cr = base64.encodestring(password)
            file.write(username+","+cr+'\n')
    file.close()

def enter(voterID, voterPassword):
    encodedPassword = base64.encodestring(voterPassword)
    with open("userpass.txt","r") as f:
        for line in f:
            if line.split(",")[0] == voterID and line.split(",")[1] == encodedPassword:
                return True
        return False
#choice = str(raw_input("Add new usernames/passwords or login --> Enter [1 or 2]"))
#if choice=="1":
    #create()
#else:
    #if enter():
        #print("Logged in!")
    #else:
        #print("Incorrect!")
