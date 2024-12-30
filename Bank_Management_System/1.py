import mysql.connector
import random
import re
from getpass import getpass

# Database setup
def initialize_database():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysql",
        database="banking_system"
    )
    cursor = conn.cursor()

    # Create database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS banking_system")
    cursor.execute("USE banking_system")

    # Users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        account_number VARCHAR(10) UNIQUE NOT NULL,
                        dob DATE NOT NULL,
                        city VARCHAR(255) NOT NULL,
                        password VARCHAR(255) NOT NULL,
                        balance DECIMAL(10, 2) NOT NULL CHECK(balance >= 2000),
                        contact_number VARCHAR(10) NOT NULL,
                        email VARCHAR(255) NOT NULL,
                        address TEXT NOT NULL,
                        is_active BOOLEAN DEFAULT TRUE
                      )''')

    # Transactions table
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        account_number VARCHAR(10) NOT NULL,
                        transaction_type VARCHAR(50) NOT NULL,
                        amount DECIMAL(10, 2) NOT NULL,
                        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                      )''')

    conn.commit()
    conn.close()

# Utility functions
def generate_account_number():
    return str(random.randint(1000000000, 9999999999))

def validate_email(email):
    return re.match(r'^[\w.-]+@[\w.-]+\.[a-zA-Z]{2,}$', email)

def validate_contact_number(contact):
    return re.match(r'^\d{10}$', contact)

def validate_password(password):
    return len(password) >= 8 and any(ch.isdigit() for ch in password) and any(ch.isupper() for ch in password)

def get_user(account_number):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="banking_system"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE account_number = %s", (account_number,))
    user = cursor.fetchone()
    conn.close()
    return user

def create_user():
    print("\n--- Add User ---")
    name = input("Enter Name: ")
    dob = input("Enter Date of Birth (YYYY-MM-DD): ")
    city = input("Enter City: ")
    address = input("Enter Address: ")
    contact_number = input("Enter Contact Number (10 digits): ")
    if not validate_contact_number(contact_number):
        print("Invalid contact number. Must be 10 digits.")
        return

    email = input("Enter Email ID: ")
    if not validate_email(email):
        print("Invalid email format.")
        return

    password = getpass("Enter Password (at least 8 characters, including a digit and an uppercase letter): ")
    if not validate_password(password):
        print("Invalid password.")
        return

    initial_balance = float(input("Enter Initial Balance (minimum 2000): "))
    if initial_balance < 2000:
        print("Initial balance must be at least 2000.")
        return

    account_number = generate_account_number()

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="banking_system"
    )
    cursor = conn.cursor()
    try:
        cursor.execute('''INSERT INTO users (name, account_number, dob, city, password, balance, contact_number, email, address)
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                       (name, account_number, dob, city, password, initial_balance, contact_number, email, address))
        conn.commit()
        print(f"User added successfully! Account Number: {account_number}")
    except mysql.connector.IntegrityError:
        print("Error: Account could not be created.")
    finally:
        conn.close()

def show_users():
    print("\n--- User List ---")
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysql",
        database="banking_system"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT name, account_number, dob, city, balance, contact_number, email, address, is_active FROM users")
    users = cursor.fetchall()
    conn.close()

    if users:
        for user in users:
            status = "Active" if user[8] else "Inactive"
            print(f"Name: {user[0]}, Account Number: {user[1]}, DOB: {user[2]}, City: {user[3]}, Balance: {user[4]}, Contact: {user[5]}, Email: {user[6]}, Address: {user[7]}, Status: {status}")
    else:
        print("No users found.")

def login():
    print("\n--- Login ---")
    account_number = input("Enter Account Number: ")
    password = getpass("Enter Password: ")

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="banking_system"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE account_number = %s AND password = %s", (account_number, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        if not user[9]:
            print("Account is deactivated. Contact the bank.")
            return
        print(f"Welcome, {user[1]}!")
        user_menu(user)
    else:
        print("Invalid account number or password.")

def user_menu(user):
    while True:
        print("\n--- User Menu ---")
        print("1. Show Balance")
        print("2. Show Transactions")
        print("3. Credit Amount")
        print("4. Debit Amount")
        print("5. Transfer Amount")
        print("6. Activate/Deactivate Account")
        print("7. Change Password")
        print("8. Update Profile")
        print("9. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            print(f"Your balance is: {user[5]}")

        elif choice == "9":
            print("Logged out successfully.")
            break

        else:
            print("Feature not implemented yet.")

# Main menu
def main():
    initialize_database()

    while True:
        print("\n--- Banking System ---")
        print("1. Add User")
        print("2. Show Users")
        print("3. Login")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_user()
        elif choice == "2":
            show_users()
        elif choice == "3":
            login()
        elif choice == "4":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
