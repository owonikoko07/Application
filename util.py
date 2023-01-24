""" Coursework for 637V0033 1CWK50
Student Name: Shuaib Olanrewaju Jokotade
Student ID: 22453753
This application was developed using code samples from:
38%: Self-writing
15%: https://www.pycryptodome.org/src/examples#encrypt-data-with-rsa
20%: https://www.pycryptodome.org/src/examples#generate-public-key-and-private-key
20%: https://www.pycryptodome.org/src/examples#encrypt-data-with-aes
5%: Lecturer provided enc.py
2%: https://stackoverflow.com/questions/1855095/how-to-create-a-zip-archive-of-a-directory
All comments are original..........
"""
import platform #Details of thhe operating system
import os #No of processor, CPUgiven by OS
import shutil
import json #Converts certain information into JSON object
import mimetypes #Converts a filename or URL

#This save user account information and create user folder such as keys, encrypt, etc.
def save_account(email, passwd):
    arr = get_account()
    arr.append({"email": email, "passwd": passwd})
    
    FOLDER_NAME = os.path.join(os.getcwd(), "users",email)
    KEYS = os.path.join(os.getcwd(), "users",email,"keys")
    ENCRYPT = os.path.join(os.getcwd(), "users",email,"encrypt")
    DECRYPT = os.path.join(os.getcwd(), "users",email,'decrypt')

    if not os.path.exists(FOLDER_NAME):
        os.mkdir(FOLDER_NAME)

    if not os.path.exists(KEYS):
        os.mkdir(KEYS)

    if not os.path.exists(ENCRYPT):
        os.mkdir(ENCRYPT)

    if not os.path.exists(DECRYPT):
        os.mkdir(DECRYPT)   

    with open("accounts.json", "w") as f:
        v = json.dumps(arr, indent=2)
        f.write(v)

#This function check if the account is register
def is_email_exist(email):
    arr = get_account()
    for i in arr:
        if i.get('email') == email:
            return True
    return False


#This function get account information
def get_account():
    try:
        content = None
        with open("accounts.json") as f:
            content = f.read()
        return json.loads(content)
    except Exception as e:
        with open("accounts.json", "w") as f:
            f.write(json.dumps([], indent=2))
        return []
    
#The function allows us to clear the screen base on the OS
def cls():
    if platform.system().lower() == "windows":
        os.system("cls")
    else:
        os.system("clear")

#This function is use for removing a file or folder
def remove_file(path):
    if os.path.exists(path):
        os.remove(path)
        #shutil.rmtree(path)


#It is use to save information of particular file into the dump.JSON
def save_dump(data):
    with open("dump.json", 'w') as f:
        f.write(json.dumps(data, indent=4))

#The function get the details of information we need to be saved into dump file such as email, filename.
def write_dump_content(path,email, key, value=None):
   
    file_type = None

    if (path.count(".zip") > 0):
        file_type = "folder"
        name = value
    else:
        file_type = "file"
        name = os.path.basename(path)

    key = len(read_dump()) + 1
    
    return {
        "id":key,
        "name": name,
        "email": email,
        "full_path": path,
        "type": file_type
    }

#The function will append the data to be save and pass to save_dump
def write_dump(data, record):
    data.append(record)
    save_dump(data)

#This function will read information store in the dump file
def read_dump():
    dump = "dump.json"
    content = None
    with open(dump) as f:
        content = f.read()
    return json.loads(content)

#This function will describe the type of file. 
def get_type(file):
    mime = mimetypes.guess_type(file)
    ext = mime[0]
    if ext:
        arr = ext.split('/')
        if (arr[0] == "text"):
            return "text"
    return "binary"

#This function get the file name from path.
def get_filename(file):
    return os.path.basename(file)

#This function provide the mode of a file either binary or text
def get_read_mode(type):
    if type == "text":
        return "r"
    return "rb"

#This function is use to write a file as binary or text
def get_write_mode(type):
    if type == "text":
        return "w"
    return "wb"
