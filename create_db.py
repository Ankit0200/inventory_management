import sqlite3
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def connect_to_database():
    # Construct the path to the database file
    database_path = resource_path('database/shop_database.db')

    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(database_path)
        print("Database connected successfully!")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

def create_databases(conn):
    if conn is not None:
        cur = conn.cursor()
        try:
            # Create tables if they do not exist
            cur.execute('CREATE TABLE IF NOT EXISTS category (cid INTEGER PRIMARY KEY,names StringVar)')
            cur.execute('CREATE TABLE IF NOT EXISTS suppliers (invoice_no StringVar PRIMARY KEY ,Name StringVar,Contact StringVar,Description Text)')
            cur.execute('CREATE TABLE IF NOT EXISTS products (Prod_id INTEGER PRIMARY KEY,Name StringVar, Category_name StringVar,Supplier_name StringVar, Price StringVar,Quantity StringVar,Status StringVar)')
            cur.execute('CREATE TABLE IF NOT EXISTS sales (bill_invoice INTEGER PRIMARY KEY,Date date,Customer_name StringVar,products_sold Text,Net_sales integer,Paid_amount integer,unpaid_amount integer,Contact_no integer)')
            conn.commit()
            print("Database tables created successfully!")
        except sqlite3.Error as e:
            print(f"Error creating database tables: {e}")

# Connect to the database
conn = connect_to_database()

# Create tables if the connection is successful
if conn is not None:
    create_databases(conn)
else:
    print("Failed to connect to the database.")
