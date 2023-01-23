import util
import os
import shutil
from secrets import token_bytes
import time;
# For generating private-public key
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

import app

#This function prompt the user to input the file to be encrypt
def encrypt_file(email,secret):
    global option

    util.cls()
    file_path = input("Enter the file path to encrypt:")
    encryption(file_path,email,secret, None)


#This function prompt the user to input the folder to be encrypt and compress
def encrypt_folder(email,secret):
    global option

    util.cls()
    folder_path = input("Enter the folder path:")
    dump = util.read_dump()
    option = ""

    if os.path.isdir(folder_path):
        arv = input("Enter the archive folder name:")
        shutil.make_archive(arv, 'zip', root_dir=folder_path) #compression
        file_path = os.path.join(os.getcwd(), arv)        
        print("Compressing...")
        #time.sleep(1)
        encryption(file_path+".zip",email,secret, arv)

        

#This function create the public and privte keys file
def public_private_pem_file(secret,name, size=2048):
   
    KEY_FOLDER = os.path.join("users",name,"keys")
   
    key = RSA.generate(size)   
    private_key = key.export_key(passphrase=secret)
    
    public_key = key.publickey().export_key()

    if os.path.exists(os.path.join(KEY_FOLDER, "private.pem")):   
        return
    
    with open(os.path.join(KEY_FOLDER, "private.pem"), "wb") as f:
        f.write(private_key)

    with open(os.path.join(KEY_FOLDER, "public.pem"), "wb") as f:
        f.write(public_key)


#This function encrypt the file or folder using the keys
def encrypt_string(reader, encrypted_path, rsa_file,secret,f=None):

    if f == None:
        data = reader.read().encode('utf-16')
    else:
        data = reader.read()
  
    writer = open(encrypted_path, 'wb')
    
    """ 
            Passing the reader, writer object as arguments
            Passing the path to the rsa_file also as an arguments
    """
    aes_key = token_bytes(32)
   
    client = RSA.import_key(open(rsa_file).read(),passphrase=secret)
    cipher_rsa = PKCS1_OAEP.new(client)
    enc_session_key = cipher_rsa.encrypt(aes_key)
    
    aes_cipher = AES.new(aes_key, AES.MODE_GCM)
    (cipher, tag) = aes_cipher.encrypt_and_digest(data)  
    
    [writer.write(x) for x in (enc_session_key, aes_cipher.nonce, tag, cipher)]
   
    writer.close()
    reader.close()

#This function calls several other file or function to either encrypt file or folder
def encryption(file_path,email,secret, fname):
      
    read_mode = ""
    write_mode = ""
    
    dump = util.read_dump()

    if (os.path.isdir(file_path)):
        return "Error: Expected file but, directory was passed"

    filename = util.get_filename(file_path)
    

    try:
        # Create the public-private key
        public_private_pem_file(secret,email)
        read_mode = util.get_read_mode(util.get_type(file_path))
        write_mode = util.get_write_mode(util.get_type(file_path))

        ENCRYPTED_FOLDER = os.path.join("users",email,"encrypt")
        encrypted_path = os.path.join(ENCRYPTED_FOLDER, filename)
        rsa_file = os.path.join("users",email,"keys","private.pem")

        # Process is not efficient for large file, but can be optimized by
        # Streaming the data rather than buffering data in memory
        reader = open(file_path, read_mode)
        
        
        
        if fname is not None:
            encrypt_string(reader, encrypted_path, rsa_file,secret,"folder")
            
            print(file_path)
            util.remove_file(file_path)
            util.write_dump(dump, util.write_dump_content(file_path,email, secret, fname))
        else:
            encrypt_string(reader, encrypted_path, rsa_file,secret)
            util.write_dump(dump, util.write_dump_content(file_path,email, secret))


    except Exception as e:
        print(e)


#This function display the information for the User
def decrypt(email,secret):
    global option

    util.cls()
    print(f"Logged in as:{email}")
    print("The heading information contains")

    dump = util.read_dump()
    arr = [x for x in dump if x.get("email") == email]

    for i, v in enumerate(arr):
        index = i + 1
        print(f"{index}. {v['name']}\t{v['type']}".expandtabs(8))

    option = input(
        "Press 0 To go back or Select any file you want to decrypt:")

    if option == "0":
        util.cls()
        app.encrypt_options()

    for i, v in enumerate(dump):

        index = str(i + 1)

        if (index == option):

            if v['type'] == "folder":
                encrypted_path = os.path.join(os.getcwd(),"users",email,"encrypt", v['name']+".zip")
                decrypted_path = os.path.join(os.getcwd(),"users",email,"decrypt", v['name']+'.zip')

            else:
                encrypted_path = os.path.join(os.getcwd(),"users",email,"encrypt", v['name'])
                decrypted_path = os.path.join(os.getcwd(),"users",email,"decrypt", v['name'])

            read_mode = util.get_read_mode(util.get_type(encrypted_path))
                        
            rsa_file = os.path.join(os.getcwd(),"users",email,"keys", "private.pem")
          
            writer = open(decrypted_path, 'wb')

            decrypt_string(encrypted_path,writer, rsa_file,secret)

            # Delete the data at the selected index
            del dump[i]

            # Write the data back into the dump
            writer.close()
            
            util.save_dump(dump)           
            util.remove_file(encrypted_path)

            break

#This function decrypt the file or folder using the keys.
def decrypt_string(reader,writer, rsa_file,secret):
    #encrypted_file = input("Enter the encrypted file: ")
   
    cipher_file = open(reader, 'rb')
    
    private_key = RSA.import_key(open(rsa_file).read(),passphrase=secret)

    enc_session_key, nonce, tag, ciphertext = [ cipher_file.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1) ]
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)


    aes_cipher = AES.new(session_key, AES.MODE_GCM,nonce=nonce)
    decrypted = aes_cipher.decrypt_and_verify(ciphertext,tag)
    writer.write(decrypted)
    return

