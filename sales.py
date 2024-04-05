import os
import tkinter as tk
from tkinter import messagebox, Text, Scrollbar, Entry, Button, Label, Frame, Listbox, END
from PIL import ImageTk, Image
import os, sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class SalesClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("1100x580+260+130")
        self.root.configure(bg="white")
        self.root.focus_force()

        # VARIABLES
        self.invoice_no = tk.StringVar()
        self.invoice_no_for_search = tk.StringVar()

        # LEFT LABELS
        sales_title = Label(self.root, text="VIEW CUSTOMER BILLS", font=("Times New Roman", 23, 'bold'),
                            bg="#836FFF", fg="lightyellow", bd=2, relief=tk.RIDGE)
        sales_title.place(x=15, y=15, width=1070, height=60)

        invoice_label = Label(self.root, text="Invoice No.", font=("Times New Roman", 15, 'bold'), bg='white')
        invoice_label.place(x=50, y=100)

        self.invoice_entry = Entry(self.root, textvariable=self.invoice_no_for_search, bg="lightyellow",
                                   font=("Times New Roman", 15, 'bold'), bd=2, relief=tk.RIDGE)
        self.invoice_entry.place(x=165, y=100, height=30)

        search_button = Button(self.root, text="Search", font=("Times New Roman", 15, 'bold'), bg='#2196f3',
                               command=self.search)
        search_button.place(x=400, y=100, height=30, width=150)

        clear_btn = Button(self.root, text="Clear", font=("Times New Roman", 15, 'bold'), bg='gray', bd=2,
                           relief=tk.RIDGE, command=self.clear)
        clear_btn.place(x=570, y=100, height=30, width=100)

        # TEETREE VIEW SALE BILLS INFO
        Bill_frame = Frame(self.root, bg='lightyellow', relief=tk.RIDGE, bd=3)
        Bill_frame.place(x=55, y=150, height=380, width=230)

        self.sales_list = Listbox(Bill_frame, font=("Times New Roman", 15,), bg='#FADA5E', bd=2, relief=tk.RIDGE)
        self.sales_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        scrolly = Scrollbar(Bill_frame, orient=tk.VERTICAL, command=self.sales_list.yview)
        scrolly.pack(side=tk.RIGHT, fill=tk.Y)
        self.sales_list.config(yscrollcommand=scrolly.set)

        # BILL TEXT AREA
        text_bill_frame = Frame(self.root, bg='lightyellow', relief=tk.RIDGE, bd=3)
        text_bill_frame.place(x=330, y=150, height=380, width=400)

        self.actual_bill = Text(text_bill_frame, font=("Times New Roman", 10), bg='lightyellow', bd=2, relief=tk.RIDGE)
        self.actual_bill.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        scrolly2 = Scrollbar(text_bill_frame, orient=tk.VERTICAL, command=self.actual_bill.yview)
        scrolly2.pack(side=tk.RIGHT, fill=tk.Y)
        self.actual_bill.config(yscrollcommand=scrolly2.set)

        self.bill_img = Image.open(resource_path("images/billing.jpg"))
        self.bill_img.thumbnail((300, 300))
        self.bill_img = ImageTk.PhotoImage(self.bill_img)

        bill_img_label = Label(self.root, image=self.bill_img, bg='white', bd=0)
        bill_img_label.image = self.bill_img
        bill_img_label.place(x=750, y=200)

        self.show_bill()
        self.sales_list.bind('<ButtonRelease-1>', self.get_bill_details)

    def show_bill(self):
        self.sales_list.delete(0, END)

        # Add debug print statement to see if the directory is being accessed correctly


        for char in os.listdir(resource_path("bills")):

            if char.endswith(".txt"):
                self.sales_list.insert(END, char)

    def get_bill_details(self, ev):
        self.actual_bill.delete(1.0, END)
        index_ = self.sales_list.curselection()
        file_name = self.sales_list.get(index_)
        with open(resource_path(f"bills/{file_name}"), 'r') as f:
            content = f.read()
            self.actual_bill.insert(END, content)

    def search(self):
        if self.invoice_no_for_search.get() == '':
            messagebox.showerror('Error', 'Please enter invoice number')
        else:
            found = False
            for item in self.sales_list.get(0, END):
                if self.invoice_no_for_search.get() in item:
                    found = True
                    break

            if found:
                self.actual_bill.delete(1.0, END)
                file_name = self.invoice_no_for_search.get()
                with open(resource_path(os.path.join(os.path.dirname(__file__), "bills", f'{file_name}.txt')),
                          'r') as f:
                    content = f.read()
                    self.actual_bill.insert(END, content)
            else:
                messagebox.showerror('Error', f'Invoice number {self.invoice_no_for_search.get()} not found')

    def clear(self):
        # Clear the invoice entry
        self.invoice_entry.delete(0, 'end')

        # Clear the current list of bills
        self.sales_list.delete(0, END)
        self.show_bill()

if __name__ == "__main__":
    root = tk.Tk()
    SalesClass(root)
    root.mainloop()
