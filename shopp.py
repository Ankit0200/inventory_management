import os
from tkinter import *
from PIL import ImageTk, Image
from product import ProductClass
from category_name import CategoryClass
from suppliers import SupplierClass
from sales import SalesClass
from billing import BillingClass
import sqlite3
import datetime
import sales

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
    print("Database path:", database_path)  # Debugging statement

    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(database_path)
        print("Database connected successfully!")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to the database: {e}")
        return None


class ATS:
    def __init__(self, root):
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)
        self.current_window = None
        self.root.title("INVENTORY MANAGEMENT SYSTEM | DEVELOPED BY ANKIT ")
        self.root.geometry("1366x768+0+0")
        self.root.configure(background="white")
        self.child_windows = []

        # Load the image
        original_image = Image.open(resource_path("images/new1.png"))

        # Resize the image to fit the label
        original_image.thumbnail((1500, 85))

        # Convert the resized image to a format compatible with Tkinter
        self.icon_title = ImageTk.PhotoImage(original_image)

        # TITLE_LABEL
        self.title = Label(self.root, text="Aarus Trade and Suppliers", image=self.icon_title, compound=LEFT,
                           font=("Times new Roman", 25, "bold"), bg='green', fg='yellow', anchor='w')
        self.title.image = self.icon_title
        self.title.place(x=0, y=0, height=70, relwidth=1)

        # LOGOUT_BUTTON
        btn_logout = Button(self.root, command=self.logout_func, text="LOGOUT", font=('Times New Roman', 15, "bold"),
                            bg='yellow', fg='black', cursor='hand2')
        btn_logout.place(x=1150, y=10, height=50, width=150)

        # CLOCK
        self.label_clock = Label(self.root, text="", font=("Times new Roman", 15), bg='#B3A398', fg='black',
                                 anchor=CENTER)
        self.label_clock.place(x=0, y=70, relwidth=1, height=30)
        self.update_clock()

        # LEFT MENU

        LeftMenu = Frame(self.root, bd=2, relief=RIDGE, bg='white')
        LeftMenu.place(x=10, y=105, width=250, height=650)

        # LEFT MENU LOGO

        self.Left_menu_logo = Image.open(resource_path("images/left_logo.jpg"))
        self.Left_menu_logo.thumbnail((200, 200))
        self.Left_menu_logo = ImageTk.PhotoImage(self.Left_menu_logo)
        lbl_menulogo = Label(LeftMenu, image=self.Left_menu_logo)
        lbl_menulogo.image = self.Left_menu_logo
        lbl_menulogo.pack(side=TOP, fill=X)

        # ICONS AND MENU

        self.icon_btn = Image.open(resource_path("images/menu.png"))
        self.icon_btn.thumbnail((15, 15))
        self.icon_btn = ImageTk.PhotoImage(self.icon_btn)
        Menu = Label(LeftMenu, text="Menu", fg='white', font=("Times New Roman", 20, "bold"), bg='green', relief=RIDGE,
                     bd=2)
        btn_Suppliers = Button(LeftMenu, command=self.supplier, text="Suppliers", fg='black',
                               font=("Times New Roman", 20, "bold"), cursor='hand2', image=self.icon_btn, compound=LEFT,
                               bg='white', relief=RIDGE, bd=2)
        btn_product = Button(LeftMenu, text="Products", fg='black', command=self.products,
                             font=("Times New Roman", 20, "bold"), image=self.icon_btn, cursor='hand2', compound=LEFT,
                             bg='white', relief=RIDGE, bd=2)
        btn_category = Button(LeftMenu, text="Category", fg='black', command=self.category,
                              font=("Times New Roman", 20, "bold"), image=self.icon_btn, cursor='hand2', compound=LEFT,
                              bg='white', relief=RIDGE, bd=2)
        btn_sales = Button(LeftMenu, text="Sales", fg='black', font=("Times New Roman", 20, "bold"),
                           image=self.icon_btn, compound=LEFT, bg='white', cursor='hand2', relief=RIDGE, bd=2,
                           command=self.Sales)
        btn_billing = Button(LeftMenu, text="Billing", fg='black', font=("Times New Roman", 20, "bold"),
                             image=self.icon_btn, compound=LEFT, bg='white', cursor='hand2', relief=RIDGE, bd=2,
                             command=self.Billing)

        btn_Suppliers.image = self.icon_btn

        btn_product.image = self.icon_btn
        btn_sales.image = self.icon_btn
        btn_billing.image = self.icon_btn
        btn_category.image = self.icon_btn

        Menu.pack(side=TOP, fill=X)
        btn_Suppliers.pack(side=TOP, fill=X)
        btn_product.pack(side=TOP, fill=X)
        btn_category.pack(side=TOP, fill=X)
        btn_sales.pack(side=TOP, fill=X)
        btn_billing.pack(side=TOP, fill=X)

        # Content
        self.Supplier_label = Label(self.root, text=f"TOTAL SUPPLIERS\n {self.fetch_suppliers()}",
                                    font=("Helvetica", 14, "bold"), bg='lightblue', fg='navy'
                                    , bd=2, relief='groove').place(x=380, y=200, height=150)
        self.category_label = Label(self.root, text=f"TOTAL CATEGORY\n {self.fetch_categories()}",
                                    font=("Helvetica", 14, "bold"), bg='lightgreen', fg='darkgreen'
                                    , bd=2, relief='groove').place(x=700, y=200, height=150)
        self.production_label = Label(self.root, text=f"TOTAL PRODUCTS\n {self.fetch_products()}",
                                      font=("Helvetica", 14, "bold"), bg='lavender', fg='indigo'
                                      , bd=2, relief='groove').place(x=1000, y=200, height=150)
        self.sales_label = Label(self.root, text=f"TOTAL SALES\n {self.fetch_sales()}", font=("Helvetica", 14, "bold"),
                                 bg='lightcoral', fg='darkred'
                                 , bd=2, relief='groove').place(x=380, y=360, height=150, width=180)


        self.footer_label = Label(self.root,
                                 text="IMS-Developed by Ankit Devkota | Contact 9749466544 for any technical issue",
                                 font=("Times new Roman", 15), bg='#B3A398', fg='black', anchor=CENTER)
        self.footer_label.place(x=0, y=730, relwidth=1, height=30)

    # +==========================================================================================================
    # new windows below

    def products(self):
        self.destroy_current_window()
        self.new_win = Toplevel(self.root)
        self.child_windows.append(self.new_win)
        self.new_obj = ProductClass(self.new_win)

    def category(self):
        self.destroy_current_window()
        self.new_win = Toplevel(self.root)
        self.child_windows.append(self.new_win)
        self.new_obj = CategoryClass(self.new_win)

    def supplier(self):
        self.destroy_current_window()
        self.new_win = Toplevel(self.root)
        self.child_windows.append(self.new_win)
        self.new_obj = SupplierClass(self.new_win)

    def Sales(self):
        self.destroy_current_window()
        self.new_win = Toplevel(self.root)
        self.child_windows.append(self.new_win)
        self.new_obj = SalesClass(self.new_win)

    def Billing(self):
        self.destroy_current_window()
        self.new_win = Toplevel(self.root)
        self.child_windows.append(self.new_win)
        self.new_obj = BillingClass(self.new_win)

    def destroy_current_window(self):
        if self.current_window:
            self.current_window.destroy()
            self.current_window = None

    def fetch_suppliers(self):
        conn = sqlite3.connect(resource_path('database/shop_database.db'))
        cur = conn.cursor()
        cur.execute('SELECT * FROM suppliers')
        suppliers = cur.fetchall()
        return len(suppliers)

    def fetch_sales(self):
        conn = sqlite3.connect(resource_path('database/shop_database.db'))
        cur = conn.cursor()
        cur.execute('SELECT * FROM sales')
        sales = cur.fetchall()
        return len(sales)

    def fetch_categories(self):
        conn = sqlite3.connect(resource_path('database/shop_database.db'))
        cur = conn.cursor()
        cur.execute('SELECT * FROM category')
        categories = cur.fetchall()
        return len(categories)

    def fetch_products(self):
        conn = sqlite3.connect(resource_path('database/shop_database.db'))
        cur = conn.cursor()
        cur.execute('SELECT * FROM products')
        products = cur.fetchall()
        return len(products)

    def update_clock(self):
        now = datetime.datetime.now()
        formatted_time = now.strftime("%d-%m-%Y\t\t\t\t\t\t\t Time:%H:%M:%S")
        self.label_clock.config(text=f"WELCOME TO INVENTORY MANAGEMENT\t\t Date: {formatted_time}")
        self.label_clock.after(1000, self.update_clock)

    def logout_func(self):
        self.root.destroy()
        for child in self.child_windows:
            child.destroy()

    def close_window(self):
        self.logout_func()
        sys.exit()


if __name__ == '__main__':
    connect_to_database()
    root = Tk()
    ATS(root)
    root.mainloop()
