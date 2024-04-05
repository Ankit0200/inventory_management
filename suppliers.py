from tkinter import *
from PIL import ImageTk, Image
import sqlite3,os,sys
from tkinter import messagebox,ttk

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class SupplierClass:
    def __init__(self,root):
        self.root =root
        self.root.title("Inventory Management System")
        self.root.geometry("1100x580+260+130")
        self.root.configure(bg="white")
        self.root.focus_force()

        ### VARIABLES ##############

        self.invoice_no=StringVar()
        self.supplier_name=StringVar()
        self.contact_no=StringVar()
        self.supplier_description=Text
        self.invoice_no_for_search=StringVar()



        ######   LEFT LABELS ###########################

        supplier_title=Label(self.root,text="Manage Supplier Details",font=("Times New Roman",23,'bold'),bg="#0288D1",fg="#FFFFFF",bd=2,relief=RIDGE).place(x=15,y=15,width=1070,height=60)

        invoice_label=Label(self.root,text="Invoice No.",font=("Times New Roman",15,'bold'),bg='white').place(x=15,y=100)
        Supplier_name_label=Label(self.root,text="Supplier Name",font=("Times New Roman",15,'bold'),bg='white').place(x=15,y=150)
        Contact_label=Label(self.root,text="Contact",font=("Times New Roman",15,'bold'),bg='white').place(x=15,y=200)
        Description_label=Label(self.root,text="Description",font=("Times New Roman",15,'bold'),bg='white').place(x=15,y=250)



        ######## ENTRIES ##########################
        invoice_entry = Entry(self.root, textvariable=self.invoice_no,bg="lightyellow",font=("Times New Roman",15,'bold'),bd=2,relief=RIDGE).place(x=150,y=100,height=30)
        supplier_entry = Entry(self.root, textvariable=self.supplier_name,bg="lightyellow",font=("Times New Roman",15,'bold'),bd=2,relief=RIDGE).place(x=150,y=150,height=30)
        contact_entry = Entry(self.root, textvariable=self.contact_no,bg="lightyellow",font=("Times New Roman",15,'bold'),bd=2,relief=RIDGE).place(x=150,y=200,height=30)
        self.supplier_description = Text(self.root, width=100, height=30, font=("Times New Roman", 15, 'bold'),
                                         bg="lightyellow", bd=2, relief=RIDGE)
        self.supplier_description.place(x=150,y=250,height=70,width=350)


        ## TREE VIEW NOW #####

        supplier_frame = Frame(self.root, bg="lightyellow", bd=2, relief=RIDGE)
        supplier_frame.place(x=530, y=140,width=550, height=300)

        scrolly = Scrollbar(supplier_frame, orient=VERTICAL)
        scrollx = Scrollbar(supplier_frame, orient=HORIZONTAL)
        #

        self.supplier_table = ttk.Treeview(supplier_frame, columns=("invoice_no", "Name", "Contact", "Description"),
                                           yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)

        scrolly.config(command=self.supplier_table.yview)
        scrollx.config(command=self.supplier_table.xview)

        self.supplier_table.heading("invoice_no", text='Sup_invoice')
        self.supplier_table.heading("Name", text='Sup_Names')
        self.supplier_table.heading("Contact", text='Contact')
        self.supplier_table.heading("Description", text='Description')
        # self.category_table.bind('<<TreeviewSelect>>', self.get_data)
        #
        # self.category_table.column("#0", stretch=NO, minwidth=0, width=0)  # Hide first default column or you can try code below

        self.supplier_table['show'] = 'headings'

        self.supplier_table.pack(fill=BOTH, expand=1)
        self.supplier_table.bind('<<TreeviewSelect>>', self.get_data)




        #### SEARCH LABEL BY INVOICE NUMBER ON THE TOP RIGHT ##############

        invoice_label = Label(self.root, text="Invoice No:", font=("Times New Roman", 15, 'bold'), bg='white').place(
            x=600, y=100)
        invoice_entry = Entry(self.root, textvariable=self.invoice_no_for_search, bg="lightyellow",
                              font=("Times New Roman", 15, 'bold'), bd=2, relief=RIDGE).place(x=710, y=100, height=30,width=150)

        search_button = Button(self.root, text="Search",command=self.search, font=("Times New Roman", 15, 'bold'), bg='green')
        search_button.place(x=880,y=100, height=30, width=150)



    ######### OTHER BUTTONS ##########################


        Save_btn = Button(self.root, text="SAVE",command=self.add, font=("Times New Roman", 15, 'bold'), bg='lightblue',bd=2, relief=RIDGE)
        Save_btn.place(x=60, y=500, height=30, width=100)

        Update_btn= Button(self.root, text="Update", command=self.Update, font=("Times New Roman", 15, 'bold'), bg='lightgreen',bd=2, relief=RIDGE)
        Update_btn.place(x=170, y=500, height=30, width=100)

        Delete_btn = Button(self.root, text="Delete", command=self.Delete, font=("Times New Roman", 15, 'bold'), bg='red',bd=2, relief=RIDGE)
        Delete_btn.place(x=280, y=500, height=30, width=100)

        clear_btn = Button(self.root, text="Clear", font=("Times New Roman", 15, 'bold'),command=self.clear, bg='gray',bd=2, relief=RIDGE)
        clear_btn.place(x=390, y=500, height=30, width=100)
        self.show()

    ##################### ADDING DATABASE ########################################

    def add(self):

        conn=sqlite3.connect(resource_path('database/shop_database.db'))
        cur=conn.cursor()

        try:
            if self.invoice_no.get()== "" or self.supplier_name.get() == "":
                messagebox.showerror("Error", "Invoice no and supplier name are required")
            else:
                cur.execute('SELECT * FROM suppliers WHERE invoice_no=?', (self.invoice_no.get(),))
                rows = cur.fetchone()
                print(rows)
                if rows is not None:
                    messagebox.showerror("Error", f"The supplier {self.supplier_name.get()} already exists")
                else:
                        cur.execute("INSERT INTO suppliers(invoice_no, Name, Contact, Description) VALUES (?, ?, ?, ?)", (
                            self.invoice_no.get(),
                            self.supplier_name.get(),
                            self.contact_no.get(),
                            self.supplier_description.get('1.0', 'end'),
                        ))
                        conn.commit()
                        self.show()
        except Exception as e:
            print(e)
            messagebox.showerror("Error",f"{e}")


     #---------------------------------------------------SHOW AND GET DATA FUNCTIONSSS------------------------------------

    def show(self):
        conn = sqlite3.connect(resource_path('database/shop_database.db'))
        cur = conn.cursor()
        try:
            self.supplier_table.delete(*self.supplier_table.get_children())
            cur.execute("select * from suppliers")
            rows = cur.fetchall()
            for row in rows:
                self.supplier_table.insert('', END, values=row)
        except Exception as ex:

            messagebox.showerror("Error", f"Error due to {ex}", parent=self.root)



   #--------------------------------  GET DATA ----------------------------------------------------------#
    def get_data(self, ev):
        selected_item = self.supplier_table.focus()  # Get the selected item in the Treeview
        if selected_item:  # Ensure an item is selected
            item_values = self.supplier_table.item(selected_item, 'values')  # Get the values of the selected item
            if item_values:  # Ensure values exist
                self.invoice_no.set(item_values[0])  # Set the value of invoice_no entry
                self.supplier_name.set(item_values[1])  # Set the value of supplier_name entry
                self.contact_no.set(item_values[2])  # Set the value of contact_no entry
                self.supplier_description.delete(1.0, END)  # Clear previous text in supplier_description Text widget
                self.supplier_description.insert(END,item_values[3])  # Insert the value of supplier_description Text widget


    #----- UPDATE FUNCTIONS ------------------

    def Update(self):
        conn = sqlite3.connect(resource_path('database/shop_database.db'))
        cur = conn.cursor()

        if self.invoice_no.get()!='' and self.supplier_name.get()!='':
            cur.execute('Select * from suppliers where invoice_no = ?', (self.invoice_no.get(),))
            rows = cur.fetchall()
            if rows is not None:
                try:
                    cur.execute("UPDATE suppliers SET Name=?, Contact=?, Description=? WHERE invoice_no=?", (
                        self.supplier_name.get(),
                        self.contact_no.get(),
                        self.supplier_description.get('1.0', 'end'),
                        self.invoice_no.get(),
                    ))
                    conn.commit()
                    messagebox.showinfo('Done', 'Updated suppliers',parent=self.root)
                    self.show()
                except Exception as e:
                    messagebox.showerror('Error',f'Error due to {e}',parent=self.root)
        else:
            messagebox.showerror('Error ', 'INVOICE NUMBER AND SUPPLIER NAME ARE REQUIRED', parent=self.root)

    def Delete(self):
        conn = sqlite3.connect(resource_path('database/shop_database.db'))
        cur = conn.cursor()
        if self.invoice_no.get() is None:
            messagebox.showerror('Error','No Invoice Number entered')
        else:
            try:
                cur.execute('Select * from suppliers where invoice_no = ?', (self.invoice_no.get(),))
                rows = cur.fetchall()
                if rows is not None:
                    askok_cancel = messagebox.askokcancel( 'Warning',f'Do you really want to delete this supplier\n {self.supplier_name.get()} ? ',parent=self.root)
                    if askok_cancel:
                        try:
                            cur.execute('DELETE FROM suppliers where invoice_no = ?', (self.invoice_no.get(),))
                            conn.commit()
                            messagebox.showinfo('Done','Deleted Successfully',parent=self.root)
                            self.show()
                            self.clear()
                        except Exception as e:
                            messagebox.showerror('Error',f'Error due to {e}',parent=self.root)
                else:
                    messagebox.showerror('Operation failed','No data found with the given invoice number',parent=self.root)
            except Exception as e:
                messagebox.showerror('Error',f'Error due to {e}',parent=self.root)


    def clear(self):
        self.supplier_name.set('')
        self.invoice_no.set('')
        self.contact_no.set('')
        self.supplier_description.delete(1.0,END)
        self.invoice_no_for_search.set('')
        self.show()

    def search(self):
        conn = sqlite3.connect(resource_path('database/shop_database.db'))
        cur=conn.cursor()
        if self.invoice_no_for_search.get()!='':
            try:
                cur.execute('SElect * from suppliers where invoice_no = ?',(self.invoice_no_for_search.get(),))
                data=cur.fetchall()
                if data is not None:
                    self.supplier_table.delete(*self.supplier_table.get_children())
                    for char in data:
                        self.supplier_table.insert('', END, values=char)


            except Exception as e:
                messagebox.showerror('Error',f'Error due to {e}')





if __name__ == "__main__":
    root=Tk()
    SupplierClass(root)
    root.mainloop()