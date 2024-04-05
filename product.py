from tkinter import *
from PIL import ImageTk, Image
import sqlite3
from tkinter import messagebox,ttk
import os,sys
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class ProductClass:
    def __init__(self,root):
        self.root =root
        self.root.title("Inventory Management System")
        self.root.geometry("1100x580+260+130")
        self.root.configure(bg="white")


  ##==------------------------VARIABLES----------------------------------------------------------------------------------------
        self.category_val=StringVar()
        self.search_index_val=StringVar()
        self.supplier_val=StringVar()
        self.product_val=StringVar()
        self.quantity_val=StringVar()
        self.status_val=StringVar()
        self.price_val=StringVar()
        self.search_val=StringVar()
        self.prod_id=StringVar()

#========================================================================================================================

        product_detail_frame=Frame(self.root,bg="white",height=500,width=600,bd=3,relief=RIDGE)
        product_detail_frame.place(x=30,y=30,width=430,height=470)



        self.root.focus_force()
        managing_label = Label(product_detail_frame, text="Manage Prdouct details",font=('Times new roman',18,'bold'), bg="#E0F2F1", fg="#001F3F")
        managing_label.pack(side=TOP, fill=X)


        #++++  labels #+++++


        category_label=Label(product_detail_frame, font=('Times new roman',15),text="Category",bg='white',anchor='w')
        category_label.place(x=20,y=70,width=200,height=25)

        Supplier_label=Label(product_detail_frame, font=('Times new roman',15),text="Supplier",bg='white',anchor='w')
        Supplier_label.place(x=20, y=120, width=200, height=25)
        Prod_name_label=Label(product_detail_frame, font=('Times new roman',15),text="Prod Name",bg='white',anchor='w')
        Prod_name_label.place(x=20, y=170, width=200, height=25)
        Price_label=Label(product_detail_frame, font=('Times new roman',15),text="Price",bg='white',anchor='w')
        Price_label.place(x=20, y=220, width=200, height=25)
        Quantity_label=Label(product_detail_frame, font=('Times new roman',15),text="Quantity",bg='white',anchor='w')
        Quantity_label.place(x=20, y=270, width=200, height=25)
        Status_label=Label(product_detail_frame, font=('Times new roman',15),text="Status",bg='white',anchor='w')
        Status_label.place(x=20, y=320, width=200, height=25)

     #------------------------ENTRIES---------------------------------------------------------------------------


        category_entry = ttk.Combobox(product_detail_frame, values=list(self.fetch_categories()), textvariable=self.category_val,
                                      state='readonly', font=('Times new roman', 15))
        category_entry.place(x=110, y=70, width=200, height=25)
        category_entry.current(0)  # Set the current selection to the first item in the values list

        Supplier_entry=ttk.Combobox(product_detail_frame, values=list(self.fetch_suppliers()),textvariable=self.supplier_val, font=('Times new Roman',15))
        Supplier_entry.place(x=110,y=121,width=200,height=25)
        Supplier_entry.current(0)

        Prduct_entry = Entry(product_detail_frame, font=('Times new roman', 15),textvariable=self.product_val, bg='lightyellow')
        Prduct_entry.place(x=115, y=171, width=200, height=25)
        #
        Price_entry = Entry(product_detail_frame, font=('Times new roman', 15), bg='lightyellow',textvariable=self.price_val)
        Price_entry.place(x=110, y=221, width=200, height=25)

        Quantity_entry = Entry(product_detail_frame, font=('Times new roman', 15), bg='lightyellow',textvariable=self.quantity_val)
        Quantity_entry.place(x=110, y=271, width=200, height=25)

        status_entry = ttk.Combobox(product_detail_frame, font=('Times new roman', 12),values=("Active","Inactive"),textvariable=self.status_val,state='readonly',width=20)
        # status_entry = ttk.Combobox(product_detail_frame, font=('Times new roman', 12), values=["Active", "Inactive"],
        #                             textvariable=self.status_val, state='readonly', width=20)


        status_entry.place(x=110, y=321, width=200,height=25)
        status_entry.current(0)



        #--------------------------- BUTTONS ----------------------------------------------------------------------------------------------------#
        Save_btn = Button(product_detail_frame, text="Save", command=self.add, font=("Times New Roman", 15, 'bold'),
                          bg='lightblue', bd=2, relief=RIDGE)

        Save_btn.place(x=10, y=400, height=30, width=100)
        #
        Update_btn = Button(product_detail_frame, text="Update", command=self.Update, font=("Times New Roman", 15, 'bold'),
                            bg='lightgreen', bd=2, relief=RIDGE)
        Update_btn.place(x=120,y=400, height=30, width=100)
        #
        Delete_btn = Button(product_detail_frame, text="Delete", command=self.Delete, font=("Times New Roman", 15, 'bold'),
                            bg='red', bd=2, relief=RIDGE)
        Delete_btn.place(x=230,y=400 , height=30, width=100)
        #
        clear_btn = Button(product_detail_frame, text="Clear", font=("Times New Roman", 15, 'bold'), command=self.clear, bg='gray',
                           bd=2, relief=RIDGE)
        clear_btn.place(x=340, y=400, height=30, width=80)
        #


        ###+++++++++++++ Right screen =============================================

        Search_frame=LabelFrame(self.root, text="Search", font=('Times new roman',15),bg='white',relief=RIDGE,bd=2)
        Search_frame.place(x=530, y=30, width=550, height=80)

        search_entry=Entry(Search_frame, font=('Times new roman',15), bg='lightyellow', bd=2, relief=RIDGE, textvariable=self.search_val)
        search_entry.place(x=220, y=3, width=200, height=30)

        search_select=ttk.Combobox(Search_frame, font=('Times new roman',15),values=(("Supplier"),("Category"),("Product_Name")),state='readonly',textvariable=self.search_index_val)
        search_select.place(x=10, y=3, width=200, height=30)
        search_select.current(1)

        btn_search=Button(Search_frame, text="Search",bg='lightgreen',command=self.search)
        btn_search.place(x=430,y=3,width=100,height=30)

        #----------------------------------------- showing details -------------------------------------------------#

        product_frame = Frame(self.root, bg="lightyellow", bd=2, relief=RIDGE)
        product_frame.place(x=530, y=140,width=550, height=300)

        scrolly = Scrollbar(product_frame, orient=VERTICAL)
        scrollx = Scrollbar(product_frame, orient=HORIZONTAL)
        #

        self.product_table = ttk.Treeview(product_frame, columns=("Prod_id", "Name",'Category_name', "Supplier_name", "Price","Quantity","Status"),
                                          yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)

        scrolly.config(command=self.product_table.yview)
        scrollx.config(command=self.product_table.xview)

        self.product_table.heading("Prod_id", text='P ID')
        self.product_table.heading("Name", text='Product_Name')
        self.product_table.heading("Category_name", text='Category_name')
        self.product_table.heading("Supplier_name", text='Supplier_name')
        self.product_table.heading("Price", text='Price')
        self.product_table.heading("Quantity", text='Quantity')
        self.product_table.heading("Status", text='Status')
        self.product_table.bind('<<TreeviewSelect>>', self.get_data)
        self.product_table['show'] = 'headings'

        self.product_table.pack(fill=BOTH, expand=1)

        self.show()
    #---------------------------------- ADD THE DATABASE ------------------------------------------------------------------------------------------
    def add(self):

        conn = sqlite3.connect(resource_path('database/shop_database.db'))
        cur=conn.cursor()

        try:
            if self.price_val.get()== "" or self.product_val.get() == "":
                messagebox.showerror("Error", "Name and price must be entered",parent=self.root)
            else:
                cur.execute('SELECT * FROM products WHERE Name=?', (self.product_val.get(),))
                rows = cur.fetchone()
                if rows is not None:
                    messagebox.showerror("Error", f"The product {self.product_val.get()} already exists",parent=self.root)
                else:
                    cur.execute(
                        "INSERT INTO products(Name,Category_name, Supplier_name, Price, Quantity, Status) VALUES (?,?,?, ?, ?, ?)", (
                            self.product_val.get(),
                            self.category_val.get(),
                            self.supplier_val.get(),
                            self.price_val.get(),
                            self.quantity_val.get(),
                            self.status_val.get(),
                        ))
                    conn.commit()
                    self.show()
                    messagebox.showinfo("Success", "Added product successfully",parent=self.root)
                    self.clear()
        except Exception as e:
            print(e)
            messagebox.showerror("Error",f"{e}",parent=self.root)

    def show(self):
        conn = sqlite3.connect(resource_path('database/shop_database.db'))
        cur = conn.cursor()
        try:
            self.product_table.delete(*self.product_table.get_children())
            cur.execute("select * from products")
            rows = cur.fetchall()
            for row in rows:
                self.product_table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {ex}", parent=self.root)

    # --------------------------------  GET DATA ----------------------------------------------------------#

    def get_data(self, ev):
        selected_item = self.product_table.focus()  # Get the selected item in the Treeview
        if selected_item:  # Ensure an item is selected
             item_values = self.product_table.item(selected_item, 'values')  # Get the values of the selected item
             if item_values:
                print(item_values)# Ensure values exist
                self.product_val.set(item_values[1])
                self.category_val.set(item_values[2])  # Set the value of contact_no entry
                self.supplier_val.set(item_values[3])
                self.price_val.set (item_values[4])
                self.quantity_val.set(item_values[5])
                # Clear previous text in supplier_description Text widget
                self.status_val.set(item_values[6]) # Insert the value of supplier_description Text widget
                self.prod_id=item_values[0]
    #     # ----- UPDATE FUNCTIONS ------------------
    #
    def Update(self):
        conn = sqlite3.connect(resource_path('database/shop_database.db'))
        cur = conn.cursor()
        if self.product_val.get() != '' and self.supplier_val.get() != '':
            cur.execute('Select * from products where Prod_id=?', (self.prod_id,))
            rows = cur.fetchone()
            print(rows)
            if rows is not None:
                try:
                    # we need to modity this code a little bit more. The name of two paints can be same sometime so be aware.
                    cur.execute(
                        "UPDATE products SET Name=?, Category_name=?, Supplier_name=?, Price=?, Quantity=?, Status=? WHERE Prod_id = ?",
                        (
                            self.product_val.get(),  # New value for the Name column
                            self.category_val.get(),  # New value for the Category_name column
                            self.supplier_val.get(),  # New value for the Supplier_name column
                            self.price_val.get(),  # New value for the Price column
                            self.quantity_val.get(),  # New value for the Quantity column
                            self.status_val.get(),  # New value for the Status column
                            self.prod_id  # Condition: which row to update (based on the Name column)
                        ))

                    conn.commit()
                    messagebox.showinfo('Done', 'Updated product successfully!',parent=self.root)

                    self.show()
                    self.clear()
                except Exception as e:
                    print(e)
                    messagebox.showerror('Error', f'Error due to {e}')
        else:
            messagebox.showerror('Error ', 'Product Name and supplier Name are required', parent=self.root)

    def Delete(self):
        conn = sqlite3.connect(resource_path('database/shop_database.db'))
        cur = conn.cursor()
        if self.product_val.get()=='':
            messagebox.showerror('Error', 'No product name entered', parent=self.root)
        else:
            try:
                cur.execute('Select * from products where Name = ?', (self.product_val.get(),))
                rows = cur.fetchall()
                print(rows)
                if len(rows)>0:
                    askok_cancel = messagebox.askokcancel('Warning',
                                                          f'Do you really want to delete this product\n {self.product_val.get()} ? ',parent=self.root)
                    if askok_cancel:
                        try:
                            cur.execute('DELETE FROM products where Name = ?', (self.product_val.get(),))
                            conn.commit()
                            messagebox.showinfo('Done', 'Deleted Successfully',parent=self.root)
                            self.show()
                            self.clear()
                        except Exception as e:
                            messagebox.showerror('Error', f'Error due to {e}')
                elif len(rows)==0:
                    messagebox.showerror('Operation failed', 'No data found with the given  Product Name',parent=self.root)
            except Exception as e:
                messagebox.showerror('Error', f'Error due to {e}',parent=self.root)
    #
    def clear(self):
        self.category_val.set('')
        self.supplier_val.set('')
        self.price_val.set('')
        self.status_val.set('')
        self.product_val.set('')
        self.quantity_val.set('')
        self.show()

    def fetch_categories(self):
        conn = sqlite3.connect(resource_path('database/shop_database.db'))
        cur=conn.cursor()
        cur.execute('SELECT names from category')
        rows = cur.fetchall()
        data = [row[0] for row in rows]
        return data
    def fetch_suppliers(self):
        conn = sqlite3.connect(resource_path('database/shop_database.db'))
        cur = conn.cursor()
        cur.execute('SELECT Name from suppliers')
        rows=cur.fetchall()
        data=[row[0] for row in rows]
        return data

    def search(self):
            conn = sqlite3.connect(resource_path('database/shop_database.db'))
            cur = conn.cursor()
            if self.search_val !='':
                try:
                    search_term = '%' + self.search_val.get() + '%'
                    if self.search_index_val.get()== 'Supplier':
                        cur.execute('SElect * from products where Supplier_name LIKE ?', (search_term,))
                        data = cur.fetchall()
                        print(data)
                        if data is not None:
                            self.product_table.delete(*self.product_table.get_children())
                            for char in data:
                                self.product_table.insert('', END, values=char)
                    elif self.search_index_val.get()== 'Category':
                        cur.execute('Select * from products where Category_name LIKE ?', (search_term,))
                        data = cur.fetchall()
                        if data is not None:
                            self.product_table.delete(*self.product_table.get_children())
                            for char in data:
                                self.product_table.insert('', END, values=char)
                    elif self.search_index_val.get()== 'Product_Name':
                        cur.execute('Select * from products where Name LIKE ?', (search_term,))
                        data = cur.fetchall()
                        if data is not None:
                            self.product_table.delete(*self.product_table.get_children())
                            for char in data:
                               self.product_table.insert('', END, values=char)

                except Exception as e:
                    messagebox.showerror('Error', f'Error due to {e}',parent=self.root)


if __name__ == "__main__":
    root=Tk()
    ProductClass(root)
    root.mainloop()