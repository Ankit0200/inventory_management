import os
import sqlite3
from tkinter import *
from tkinter import messagebox

from PIL import ImageTk, Image

class LoginClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Window")
        self.root.geometry("400x400")
        self.root.configure(background="white")

        self.username = StringVar()
        self.password = StringVar()

        loging_frame = Frame(self.root, bg="white", relief=RIDGE, bd=5)
        loging_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        login_label = Label(loging_frame, text="Login System", font=("Times New Roman", 25, "bold"), bg="white",)
        login_label.grid(row=0, columnspan=2, pady=20)

        user_name_lbl = Label(loging_frame, text="Username:", font=("Times New Roman", 14), bg='white')
        user_name_lbl.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        user_name_entry = Entry(loging_frame, font=("Times New", 14), bg='lightyellow', fg='black', textvariable=self.username,show="*")
        user_name_entry.grid(row=1, column=1, padx=10, pady=10)

        password_lbl = Label(loging_frame, text="Password:", font=("Times New Roman", 14), bg='white')
        password_lbl.grid(row=2, column=0, padx=10, pady=10, sticky="e")

        password_entry = Entry(loging_frame, font=("Times New", 14), bg='lightyellow', fg='black', textvariable=self.password, show='*')
        password_entry.grid(row=2, column=1, padx=10, pady=10)

        login_button = Button(loging_frame, text="Login", font=("Times New", 14, "bold"), bg='blue', fg='white', command=self.login_now)
        login_button.grid(row=3, columnspan=2, pady=20)

    def login_now(self):
        conn=sqlite3.connect('database/shop_database.db')
        cur=conn.cursor()
        cur.execute('SELECT * FROM admin')
        rows = cur.fetchone()

        if self.username.get() == "" or self.password.get() == "":
            messagebox.showerror("Error", "Please enter all fields", parent=self.root)
        else:
            if self.username.get() == rows[0] and self.password.get() == rows[1]:
                self.root.destroy()
                os.system('python shopp.py')
            else:
                messagebox.showerror("Error", "Invalid username or password", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    LoginClass(root)
    root.mainloop()
