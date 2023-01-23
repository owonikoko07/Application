import sys
import string
import random
import json
import os


import re
import shutil
import time

import getpass as gp

import util
import encrypt


#Variables used in the applications i.e global variables
option = ""
email = "a@g.com"
passwd = "123"
USER_FOLDER = ""
ACCOUNTS = ""
KEYS = ""
DUMP = "dump.json"
SLEEP_DURATION = 2


#This function allowa user to login
def login_account():
    global email
    global passwd
    
    util.cls()
    print("Login account\n")
    email = input("Enter your email:")
    passwd = gp.getpass("Enter your password:")
    arr = util.get_account()
    user = None

    for i in arr:
        if i.get("email") == email and i.get("passwd") == passwd:
            user = i
            break

    if user == None:
        print("Invalid email or passwd was supplied")
        print("Try again... Redirecting in 2 sec...\n")

        time.sleep(SLEEP_DURATION)
        login_account()
    else:
        print("Credential Correct, Redirecting in 2 sec...")
        time.sleep(SLEEP_DURATION)
        encrypt_options()



#This function create the encryted, decryted folder, keys and dump
def make_folder():
    """
            Create folder to store all encrypted files in 
    """
    global USER_FOLDER
    global ACCOUNTS
    global DUMP

    USER_FOLDER = os.path.join(os.getcwd(), "users")
    ACCOUNTS = os.path.join(os.getcwd(), "accounts.json")

    if not os.path.exists(USER_FOLDER):
        os.mkdir(USER_FOLDER)

    if not os.path.exists(ACCOUNTS):
        with open(ACCOUNTS, 'w') as f:
            content = json.dumps([], indent=2)
            f.write(content)
            
    if not os.path.exists(DUMP):
        with open(DUMP, 'w') as f:
            content = json.dumps([], indent=2)
            f.write(content)

#This function display the account options
def account():
    util.cls()
    global option

    print("1. To go Back")
    print("2. Create account")
    print("3. Login account")

    option = input("select option:")

    if option == "1":
        util.cls()
        select_options()

    if option == "2":
        create_account()

    if option == "3":
        login_account()

#This function create new user account
def create_account(n=False):
    global email
    global passwd
    
    util.cls()
    if n:
        text = "Re-enter your email:"
    else:
        text = "Enter your email:"

    email = input(text)
    passwd = gp.getpass("Enter your password:")

    if util.is_email_exist(email):
        print(f"Email:${email} already exist. Redirecting in 2 sec...")
        time.sleep(SLEEP_DURATION)
        create_account(True)
    else:
        util.save_account(email, passwd)
        print("Account Created. Redirecting in 2 sec...")
        time.sleep(SLEEP_DURATION)
        account()


#This function allow a user to login
def login_account():
    global email
    global passwd
    
    util.cls()
    print("Login account\n")
    email = input("Enter your email:")
    passwd = gp.getpass("Enter your password:")
    arr = util.get_account()
    user = None

    for i in arr:
        if i.get("email") == email and i.get("passwd") == passwd:
            user = i
            break

    if user == None:
        print("Invalid email or passwd was supplied")
        print("Try again... Redirecting in 2 sec...\n")

        time.sleep(SLEEP_DURATION)
        login_account()
    else:
        print("Credential Correct, Redirecting in 2 sec...")
        time.sleep(SLEEP_DURATION)
        encrypt_options()

   
#This function display the option keys we see on the page
def select_options():
    global option

    print("Welcome to Jokotade Encryption App")
    print("Select the appropriate option to begin\n")
    print("1. To Exit")
    print("2. Account")

    option = input("select option:")

    if (option == "1"):
        sys.exit("\n\nExiting application")

    if option == "2":
        account()

#This function dispaly options in the application
def encrypt_options():
    global option
    global email
    global passwd

    util.cls()

    print(f"Logged in as:{email}")
    print("Select the appropriate option\n")
    print("1. To encrypt file")
    print("2. To encrypt folder")
    print("3. To decrypt file or folder")
    print("4. Logout")

    option = input("select option:")

    if option == "1":
        encrypt.encrypt_file(email,passwd)
        print("File Encrypted")
        time.sleep(1)
        encrypt_options()
        
    if option == "2":
        encrypt.encrypt_folder(email,passwd)
        print("Folder Encrypted")
        time.sleep(1)
        encrypt_options()
        
    if option == "3":
        encrypt.decrypt(email,passwd)
        print("File Decrypted")
        time.sleep(1)
        encrypt_options()
        
    if option == "4":
        util.cls()
        select_options()

        
#This function create the folder and calls all functions
def main():
    make_folder()
    select_options()

#This function start the program.
if __name__ == "__main__":
    main()
