import sqlite3
from datetime import datetime
from getpass import getpass




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
    