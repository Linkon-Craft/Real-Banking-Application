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
              balance REAL NOT NULL DEFAULT 0.00,
              account_number INTEGER NOT NULL UNIQUE CHECK(account_number <> '')                      
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              user_id INTEGER NOT NULL,
              transaction_type TEXT NOT NULL CHECK(transaction_type IN ('Deposit', 'Withdrawal', 'Transfer Out',  'Transfer In')),
              amount REAL NOT NULL CHECK(amount >= 0),
              date TEXT NOT NULL,
              FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            );
        """)


def user_registration():
    try:
        while True:

            first_name = input("Enter your first name: ").strip().title()
            if len(first_name) < 3 or len(first_name) > 20:
                print("Error: First name must be between 3 and 20 letters")
                continue

            middle_name = input("Enter your middle name ('Press Enter to skip'): ").strip().title()
            last_name = input("Enter Your last name: ").strip().title()
            if len(last_name) < 3 or len(last_name) > 20:
                print("Error: First name must be between 3 and 20 letters")
                continue

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

            if  "[!@#$%^&*(),.?\":{}|<>]" in full_name:
                print("Error: full_name must not contain any special character")
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
                print("Error: Password must contain at least one special character")
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

            cursor.execute("Select initial_deposit FROM users WHERE username = ?", (username,)).fetchone()
            balance = 0.00
            balance = initial_deposit + balance
            break
        

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
                    INSERT INTO users (full_name, username, password, initial_deposit, balance, account_number)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (full_name, username, hashed_password, initial_deposit, balance, account_number))
                conn.commit()

                user_id = cursor.lastrowid

                cursor.execute("""
                 INSERT INTO transactions (user_id, transaction_type, amount, date)
                    VALUES (?, 'Deposit', ?, ?)
                """, (user_id, initial_deposit, datetime.now().strftime('%Y-%m-%d')))
                conn.commit()

                print("Signing up...")
                time.sleep(2)
                print(f"Congratulations!{first_name} Your Registration is successful, Welcome to Linkon Bank PLC 🎠")
                print(f"Your Username is: {username}")
                print(f"Current balance (#): {balance}")
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
                        SELECT id, full_name, username FROM users WHERE username = ? AND password = ?
                """, (username, hashed_password)).fetchone()
                if username is None:
                    print("Invalid Username or password")
                    return
                
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
    id, full_name,username = user
    print(f"Hello {full_name}, Let's deposit in your account.")

    while True:
        try:
            deposit_amount = float(input("Enter amount you want to deposit (#): ").strip())
            if deposit_amount <= 0: 
                print("Error: Deposit cannot be negative or Zero")
                continue

            with sqlite3.connect(BI_File) as conn:
                cursor = conn.cursor()

                cursor.execute("SELECT balance FROM users WHERE id = ?", (id,))
                current_balance = cursor.fetchone()[0]
                new_balace = current_balance + deposit_amount
                cursor.execute("UPDATE users SET balance = ? WHERE id = ?",(new_balace, id))

                cursor.execute("""
                    INSERT INTO transactions (user_id, transaction_type, amount, date)
                        VALUES (?, 'Deposit', ?, ?)
                    """, (id, deposit_amount, datetime.now().strftime('%Y-%m-%d')))
                conn.commit()
            print("Processing...")
            time.sleep(3)
            print(f"Hi {username}...  Deposit successful! Your new balance is #{new_balace:.2f}")
            break
        except ValueError:
            print("Error: Please enter a valid number.")
        except Exception as e:
            print(f"Something went wrong: {e}")
            break


def withdrawal(user):
    id, full_name, username = user
    print(f"Hello! {full_name}! Please wait!! Withdrawal Processing ")

    while True:
        try:
            withdrawal_amount = float(input("Enter the amount you want to withdraw(#): "))
            with sqlite3.connect(BI_File) as conn:
                cursor = conn.cursor()

                cursor.execute("SELECT balance FROM users WHERE id = ?", (id,))
                current_balance = cursor.fetchone()[0]
            
                if withdrawal_amount <= 0:
                    print("Error: Withdrawal amount can not less than 1")
                    continue
                if withdrawal_amount > current_balance:
                    print(f"Error: Amount greater than your current balance of {current_balance}")
                    continue
            
            with sqlite3.connect(BI_File) as conn:
                cursor = conn.cursor()
        
                new_balance = current_balance - withdrawal_amount

                cursor.execute("UPDATE users SET balance = ? WHERE id = ?", (new_balance, id))

                cursor.execute("""
                    INSERT INTO transactions (user_id, transaction_type, amount, date)
                    VALUES (?, 'Withdrawal', ?, ?)
                """, (id, withdrawal_amount, datetime.now().strftime('%Y-%m-%d')))
                conn.commit()
            print("Please wait!!! while your request is processing...")
            time.sleep(3)
            print(f"Hi {username}...  withdrawal of {withdrawal_amount:.2f} completed! Your new balance is #{new_balance:.2f}")
            break
        except ValueError:
             print("Error: Please enter a valid number.")
        except Exception as e:
            print(f"Something went wrong: {e}")
            break


def balance(user):
    id, full_name, username = user
    print(f"Hi {username}! lets check your balance...")
    time.sleep(3)
    
    while True:
        try: 
            balance_enquiry = float(input("To check your balance press 1: "))
            if balance_enquiry != 1:
                print("Invalid input")
                continue
            
            with sqlite3.connect(BI_File) as conn:
                cursor = conn.cursor()

                cursor.execute("SELECT balance FROM users WHERE id = ?", (id,))
                current_balance = cursor.fetchone()[0]
            print("Please wait while your request is processing...")
            time.sleep(3)
            print(f"Hi {full_name}")
            print(f"current balance") 
            print("-" * 50)
            print(f"#{current_balance:.2f}")
            break
        except ValueError:
            print("Error: Please enter a valid number.")
        except Exception as e:
            print(f"Something went wrong: {e}")
            
        
        
def transaction_history(user):
    id, full_name, username = user
    print(f"Hi {username} Please wait... While your transaction history is being processed")
    time.sleep(2)

    try:
        with sqlite3.connect(BI_File) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT transaction_type, amount, date FROM transactions WHERE user_id = ? ORDER BY date DESC
            """, (id,))
            transactions = cursor.fetchall()

            if not transactions:
                print("No transaction history found.")
                return

            print(f"Transaction History for {full_name}:")
            print("-" * 50)
            print(f"{'Type'}               {'Amount(#)'}              {'Date'}")
            print("-" * 50)

            for transaction in transactions:
                transaction_type, amount, date = transaction
                print(f"{transaction_type}               {amount:.2f}             {date}")
            print("-" * 50)
    except ValueError:
            print("Error: Please enter a valid number.")
    except Exception as e:
        print(f"Something went wrong: {e}")
        

def transfer(user):
    id, full_name, username = user
    print(f"Good morning {full_name}!, Please wait... Transfer processing")
    time.sleep(2)

    while True:
        try:
            account_number = int(input("Enter recipient account number: "))

            with sqlite3.connect(BI_File) as conn:
                cursor = conn.cursor()

                cursor.execute("SELECT id, full_name, account_number FROM users WHERE account_number = ?", (account_number,))
                account = cursor.fetchone()
                
                if account: 
                    recipient_id, recipient_name, account_number = account
                    print("Customer found")
                    time.sleep(2)
                    print(f" Recipient Name: {recipient_name}")
                    print(f"Recipient Account Number: {account_number}")
                else:
                    print("invalid account")
                    continue
                
                cursor.execute("SELECT account_number FROM users WHERE id = ?", (id,))
                self_account = cursor.fetchone()[0]

                if self_account == account_number:
                    print("Error!!! You cannot transfer to your account number")
                    continue

                transfer_amount = float(input("Enter amount you want to transfer: "))
                if transfer_amount < 1:
                    print("Invalid transaction... Can not transfer zero(0) amount")
                    continue
             

                cursor.execute("SELECT balance FROM users WHERE id = ?", (id,))
                current_balance = cursor.fetchone()[0]
                
                if transfer_amount > current_balance:
                    print("Transfer Error: Insufficient Balance")
                    continue
                
                new_balance =  current_balance - transfer_amount
                cursor.execute("UPDATE users SET balance = ? WHERE id = ?", (new_balance, id))


                cursor.execute("SELECT balance FROM users WHERE id = ?", (recipient_id,))
                recipient_balance = cursor.fetchone()[0]
                
                new_balance = transfer_amount + recipient_balance

                cursor.execute("UPDATE users SET balance = ? WHERE id = ?", (new_balance, recipient_id))

                
                cursor.execute("""
                    INSERT INTO transactions (user_id, transaction_type, amount, date)
                    VALUES (?, 'Transfer Out', ?, ?)
                """, (id, transfer_amount, datetime.now().strftime('%Y-%m-%d')))
                
                
                cursor.execute("""
                    INSERT INTO transactions (user_id, transaction_type, amount, date)
                    VALUES (?, 'Transfer In', ?, ?)
                """, (recipient_id, transfer_amount, datetime.now().strftime('%Y-%m-%d')))
                conn.commit()
            print("Transfer Processing...")
            time.sleep(2)
            print(f"Transfer of #{transfer_amount} to {recipient_name} completed.")
            break
        except ValueError:
            print("Error: Please enter a valid number.")
        except Exception as e:
            print(f"Something went wrong: {e}")
            
            


def my_dashboard(user):
    id, full_name, username = user
    print(f" Good morning {full_name}!, Welcome to your dashboard")
    time.sleep(3)
    
    dashboard = """"
    Welcome to Linkon Bank PLC! ⛱ 🎡 🎠 
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

