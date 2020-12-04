
import sqlite3
from hashlib import sha256

masterUsername = "master"
masterPassword = "password"
masterLogin = masterUsername + masterPassword

accessed = 0
accessed = False

while accessed == False:
    masterUsername = input("Username: ")
    masterPassword = input("Password: ")
    
    if masterUsername == "master" and masterPassword == "password":
        print("Welcome.\n")
        accessed = True

    else:
        print("Username/Password is incorrect. Try again.")
        break

conn = sqlite3.connect('password_manager.db')
c = conn.cursor()

def create_credential(pass_key, service, admin_pass):
    return sha256(admin_pass.encode('utf-8') + service.lower().encode('utf-8') + pass_key.encode('utf-8')).hexdigest()[:15]

def retrieve_hex_key(admin_pass, service):
    return sha256(admin_pass.encode('utf-8') + service.lower().encode('utf-8')).hexdigest()

# Functional Story 1
def retrieve_credential(admin_pass, service):
    hidden_key = retrieve_hex_key(admin_pass, service)
    cursor = conn.execute("SELECT * from KEYS WHERE PASS_KEY=" + '"' + hidden_key + '"')

    file_string = ""
    for row in cursor:
        file_string = row[0]
    return create_credential(file_string, service, admin_pass)

# Functional Story 2
def add_credential(service, admin_pass):
    hidden_key = retrieve_hex_key(admin_pass, service)

    # Security Story 5
    command = 'INSERT INTO KEYS (PASS_KEY) VALUES (%s);' %('"' + hidden_key +'"')        
    conn.execute(command)
    conn.commit()
    return create_credential(hidden_key, service, admin_pass)

if accessed == True:
    try:
        conn.execute('''Create table key
            (pass_key text primary key not null) ;''')
        print("Safe is created. What would you like to store in it?")
    except:
        print("You already have one. What else would you like to store?")

    while True:
        print("\n")
        print("Enter 'a' to make a new credential")
        print("Enter 'b' to find a credential")
        print("Enter 'c' to exit")
        userInput = input()

        if userInput == "a":
            # Functional Story 3
            service = input("Which server do you want to store this credential?\n")
            print("\n" + service.capitalize() + "New Credential: " + add_credential(service, masterLogin))
        if userInput == "b":
            service = input('Which service do you want to retrieve credentials from?')
            print("\n" + service.capitalize() + "Credential: " + retrieve_credential(masterLogin, service))
        if userInput == "c":
            break