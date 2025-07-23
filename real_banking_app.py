import sqlite3
from datetime import datetime
import time
import re
from getpass import getpass
import hashlib
import random
BI_File = "linkon_bank_lib.db"
def set_up():
    with sqlite3.connect(BI_File) as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              full_name TEXT NOT NULL CHECK(full_name <> ''),
              username TEXT NOT NULL UNIQUE CHECK(username <> ''),
              password TEXT NOT NULL CHECK(password <> ''),
              initial_deposit INTEGER NOT NULL CHECK(initial_deposit <> ''),
              account_number INTEGER NOT NULL UNIQUE CHECK(account_number <> '')                      
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS account_balances(
              user_id INTEGER PRIMARY KEY,
              balance REAL NOT NULL CHECK(balance >= 0),
              FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            );
        
        """)
def user_registration():
    try:
        while True:

            first_name = input("Enter your first name: ").strip().title()
            middle_name = input("Enter your middle name ('Press Enter to skip'): ").strip().title()
            last_name = input("Enter Your last name: ").strip().title()

            if middle_name:
                full_name = " ".join([first_name, middle_name, last_name])
            else:
                full_name = " ".join([first_name, last_name])

            if not full_name.replace(" ", "").isalpha():
                print("Error: Full name must only contain alphabetic characters.")
                continue
            if len(full_name) < 4 or len(full_name) > 255:
                print("Error: Full name must be between 4 and 255 characters.")
                continue
            break

        while True: 

            username = input("Enter your username: ").strip().lower()

            if len(username) < 3 or len(username) > 28:
                print("Error: username must be between 3 and 28 characters.")
                continue
            if not re.fullmatch(r"[a-z0-9_]+", username):
                print("Error: Username must contain only alphanumeric characters and underscores.")
                continue

            with sqlite3.connect(BI_File) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT username FROM users WHERE username = ?", (username,))

                if cursor.fetchone():
                    print("Error: Username already exists. Please choose a different username.")
                    continue
            print("Username accepted!")
            break

        while True:

            password = getpass("Enter your password: ").strip()
            if len(password) < 8 or len(password) > 30:
                print("Error password must be between 8 and 30 characters")
                continue
            if not re.search(r"[A-Z]", password):
                print("Error: Password must contain at least one uppercase")
                continue
            if not re.search(r"[a-z]", password): 
                print("Error: Password must contain at least one lowercase")
                continue
            if not re.search(r"[0-9]", password):
                print("Error: Password must contain at least one number")
                continue
            if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
                print("Error: Password must contain at least on special character")
                continue
            
            confirm_password = getpass("Confirm your password: ").strip()
            if len(password) < 8 or len(password) > 30:
                print("Error password must be between 8 and 30 characters")
                continue
            if not re.search(r"[A-Z]", password):
                print("Error: Password must contain at least one uppercase")
                continue
            if not re.search(r"[a-z]", password): 
                print("Error: Password must contain at least one lowercase")
                continue
            if not re.search(r"[0-9]", password):
                print("Error: Password must contain at least one number")
                continue
            if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
                print("Error: Password must contain at least on special character")
                continue
            
            if password != confirm_password:
                print("Passords don't match")
                continue
            print("Password accepted!")
            break
        
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
            

        while True:
            try:
                initial_deposit = int(input("Enter your initial deposit (#): "))

                if initial_deposit < 2000 :
                    print("Error: Initial deposit is less than minimum balance of (#2,000)")
                    continue
                if initial_deposit < 0 :
                    print("Error: Negative input")
                    continue

                print("Deposit accepted")
                break
            except ValueError:
                print("Error: Please enter a valid number")

        while True:
            with sqlite3.connect(BI_File) as conn:
                cursor = conn.cursor()
                while True:
                    account_number = "911" + str(random.randrange(1000000, 9999999))
                    cursor.execute("SELECT account_number FROM users WHERE account_number = ?", (account_number,))
                    if not cursor.fetchone():
                        break

            print(f"Your Account number is: {account_number}")
            break

        with sqlite3.connect(BI_File) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO users (full_name, username, password, initial_deposit, account_number)
                    VALUES (?, ?, ?, ?, ?)
                """, (full_name, username, hashed_password, initial_deposit, account_number))
                conn.commit()

                user_id = cursor.lastrowid

                cursor.execute("""
                    INSERT INTO account_balances (user_id, balance)
                    VALUES (?, ?)
                """, (user_id, initial_deposit))
                conn.commit()

                print("Signing up...")
                time.sleep(2)
                print(f"Congratulations!{first_name} Your Registration is successful, Welcome to Linkon Bank PLC 🎠")
                print(f"Your Username is: {username}...")
            except sqlite3.IntegrityError as e:
                print(f"Intergrity Error : {e}")
            except Exception as e:
                print(f"Something Went Wrong: {e}")
    
    except Exception as e:
        print(f"Something Went Wrong: {e}")
    finally:
        conn.close()


def user_login():
    while True:
        username = input("Enter your username: ")
        if len(username) < 3 or len(username) > 28:
            print("Error: username must be between 3 and 28 characters.")
            continue
        if not re.fullmatch(r"[a-z0-9_]+", username):
            print("Error: Username must contain only alphanumeric characters and underscores.")
            continue
        break
        
    while True:

            password = getpass("Enter your password: ").strip()
            if len(password) < 8 or len(password) > 30:
                print("Error password must be between 8 and 30 characters")
                continue
            if not re.search(r"[A-Z]", password):
                print("Error: Password must contain at least one uppercase")
                continue
            if not re.search(r"[a-z]", password): 
                print("Error: Password must contain at least one lowercase")
                continue
            if not re.search(r"[0-9]", password):
                print("Error: Password must contain at least one number")
                continue
            if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
                print("Error: Password must contain at least on special character")
                continue
        
            print("Password accepted!")
            break
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    with sqlite3.connect(BI_File) as conn:
            cursor = conn.cursor()
            try:
                user = cursor.execute("""
                        SELECT id, full_name, username, FROM users WHERE username = ? AND password = ?
                """, (username, hashed_password)).fetchone()
                if user is None:
                    print("Invalid Username or password")
                else:
                    print("Loggin in...")
                    time.sleep(2)
                    print("Get ready to experience convenient and secure banking at your fingertips.")
                    time.sleep(2)
                    print("Welcome to Linkon Bank PLC ⛱🎡🎠")
                    my_dashboard(user)
            except sqlite3.IntegrityError as e:
                print(f"Intergrity Error : {e}")
            except Exception as e:
                print(f"Something Went Wrong: {e}")


def deposit(user):
    id, full_name = user
    print(f"Hello {full_name}, Let's deposit in your account.")

    while True:
        try:
            deposit_amount - float(input("Enter amount you want to deposit: ").strip())
            if deposit_amount <= 0: 
                print("Error: Deposit cannot be negative or Zero")
                continue

            with 

def my_dashboard(user):
    id, full_name = user
    print(f" Good morning {full_name}!, Welcome to your dashboard")
    time.sleep(3)
    
    dashboard = """"
    Welcome to Linkon Bank PLC! ⛱🎡🎠 
   1. Deposit
   2. Withdrawal
   3. Balance Enquiry
   4. Transaction History
   5. Transfer
   6. Logout
    """
    while True:
        print(dashboard)
        choice = input("Enter an option from above: ").strip()
        if choice == "1":
            print("loading...")
            time.sleep(2)
            deposit(user)
        elif choice == "2":
            print("loading...")
            time.sleep(2)
            withdrawal(user)
        elif choice == "3":
            print("loading...")
            time.sleep(2)
            balance(user)
        elif choice == "4":
            print("loading...")
            time.sleep(2)
            transaction_history(user)
        elif choice == "5":
            print("loading")
            time.sleep(2)
            transfer(user)
        elif choice == "6":
            print("loading...")
            time.sleep(2)
            print("Logged out successful.Thank you.")
            break
        else:
            print("invalid Choice")
            continue



set_up()

menu = """
Welcome to Linkon Bank PLC
1. User Registration
2. User Login
3. Exist
"""

while True:
    print(menu)
    choice = input("Enter an option from above: ").strip()

    if choice == "1":
        user_registration()
    elif choice == "2":
        user_login()
    elif choice == "3":
        print("Goodbye 🧑‍💼")
        break
    else:
        print("Invalid Choice")
        continue

