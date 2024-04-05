from tkinter import *
from tkinter import *
from PIL import ImageTk, Image
from product import ProductClass
from category_name import CategoryClass
from suppliers import SupplierClass
from tkinter import ttk, messagebox,simpledialog
import sqlite3
import datetime,json
import os,sys
now = datetime.datetime.now()
formatted_time = now.strftime("%d-%m-%Y\t\t\t\t\t\t\t Time:%H:%M:%S")
def resource_path(relative_path,base_path=None):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class BillingClass:

    def __init__(self, root):
        self.root = root
        now = datetime.datetime.now()
        self.formatted_time = now.strftime("%d-%m-%Y")
        self.root.title("INVENTORY MANAGEMENT SYSTEM | DEVELOPED BY ANKIT ")
        self.root.geometry("1366x768+0+0")
        self.root.configure(background="white")
        self.cart_list=[]
        self.discount=0


        #======================= VARIABLES ========================================
        self.search_var=StringVar()
        self.customer_name=StringVar()
        self.customer_contact=StringVar()
        self.p_id=StringVar()
        self.p_name=StringVar()
        self.p_quantity=StringVar()
        self.p_price=StringVar()
        self.p_status=StringVar()
        self.var_stock_quantity=StringVar()
        self.calc_screen=StringVar()

        # Load the image
        original_image = Image.open(resource_path("images/new1.png"))

        # Resize the image to fit the label
        original_image.thumbnail((1500, 85))

        # Convert the resized image to a format compatible with Tkinter
        self.icon_title = ImageTk.PhotoImage(original_image)

        # TITLE_LABEL
        self.title = Label(self.root, text="Aarush Trade and suppliers", image=self.icon_title, compound=LEFT,
                           font=("Times new Roman", 25, "bold"), bg='green', fg='white', anchor='w')
        self.title.image = self.icon_title
        self.title.place(x=0, y=0, height=70, relwidth=1)

        # LOGOUT_BUTTON
        btn_logout = Button(self.root, text="LOGOUT",font=('Times New Roman', 15, "bold"), bg='yellow', fg='black', cursor='hand2')
        btn_logout.place(x=1150, y=10, height=50, width=150)

        # CLOCK
        self.label_clock = Label(self.root, text="WELCOME TO INVENTORY MANAGEMENT\t\t Date:DD-MM-YYYY\t\t TIME:HH-MM-SS", font=("Times new Roman", 15), bg='#B3A398', fg='black', anchor=CENTER)
        self.label_clock.place(x=0, y=70, relwidth=1, height=30)

        #---FOOTER LABEL----=
        self.footer_label = Label(self.root,
                                  text="IMS-Developed by Ankit Devkota | Contact 9749466544 for any technical issue",
                                  font=("Times new Roman", 15), bg='#B3A398', fg='black', anchor=CENTER)
        self.footer_label.place(x=0, y=730, relwidth=1, height=30)

        ##-------------------- PRODUCT FRAME -------------------------------------+

        prod_frame1=Frame(self.root, bg='white', bd=4, relief=RIDGE)
        prod_frame1.place(x=15,y=110,width=410, height=550)

        p_title=Label(prod_frame1, text="All products", font=("goudy old style",20,'bold'), bg='#262626', fg='white').pack(side=TOP,fill=X)
        prod_frame2 = Frame(prod_frame1, bg='white', bd=2, relief=RIDGE)
        prod_frame2.place(x=2, y=42, width=398, height=90)

        lbl_search=Label(prod_frame2, text="Search products | By name", font=("Times new Roman",15,'bold'),bg='white', fg='green').place(x=2,y=5)

        prod_name_lbl=Label(prod_frame2, text="Product name", font=("Times new Roman",15,'bold'),bg='white', fg='black').place(x=2,y=40)
        prod_name_entry=Entry(prod_frame2,textvariable=self.search_var, font=("Times new Roman",15,'bold'),bg='lightyellow', fg='black',bd=2, relief=RIDGE).place(x=130,y=40,width=150,height=25)

        btn_search=Button(prod_frame2,command=self.search, text="Search", font=("Times new Roman",15,'bold'),bg='green',fg='white',cursor='hand2').place(x=290,y=40,width=80,height=25)
        btn_show_all=Button(prod_frame2, text="Show all",command=self.show_products, font=("Times new Roman",15,'bold'),bg='gray',fg='white',cursor='hand2').place(x=290,y=10, width=80,height=25)

        #------------------- PRODUCT TEE TREE VIEW NOW -----------------------+
        prod_frame3 = Frame(prod_frame1, bg="lightyellow", bd=2, relief=RIDGE)
        prod_frame3.place(x=2,y=140,width=405,height=385)

        scrolly = Scrollbar(prod_frame3, orient=VERTICAL)
        scrollx = Scrollbar(prod_frame3, orient=HORIZONTAL)
        #

        self.product_table = ttk.Treeview(prod_frame3, columns=(
        "Prod_id", "Name","Price","Quantity", "Status"),
                                          yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)

        scrolly.config(command=self.product_table.yview)
        scrollx.config(command=self.product_table.xview)

        self.product_table.heading("Prod_id", text='P ID')
        self.product_table.heading("Name", text='Product_Name')
        self.product_table.heading("Price", text='Price')
        self.product_table.heading("Quantity", text='Quantity')
        self.product_table.heading("Status", text='Status')
        self.product_table.bind('<<TreeviewSelect>>', self.get_data)
        self.product_table['show'] = 'headings'
        self.product_table.column('Prod_id', width=40)
        self.product_table.column('Name', width=150)
        self.product_table.column('Price', width=100)
        self.product_table.column('Quantity', width=100)
        self.product_table.column('Status', width=80)

        self.product_table.pack(fill=BOTH, expand=1)

        Lbl_note=Label(prod_frame1, text="Notes:Enter 0 quantity to remove from the cart", font=("Helvetica",10,),bg='white',fg='red').pack(side=BOTTOM, fill=X)


        customer_frame = Frame(self.root, bg='white', bd=4, relief=RIDGE)
        customer_frame.place(x=440, y=110, width=530, height=70)

        customer_title=Label(customer_frame, text="Customer Details", font=("Times new roman",16),bg='lightgray',fg='black').pack(side=TOP,fill=X)

        customer_name_lbl=Label(customer_frame,font=('Times new roman',14),bg='white',text="Customer name:").place(x=2,y=33)
        customer_name_entry = Entry(customer_frame, textvariable=self.customer_name, font=("Times new Roman", 15, 'bold'),
                                bg='lightyellow', fg='black', bd=2, relief=RIDGE).place(x=135,y=33,height=25,width=150)

        contact_lbl = Label(customer_frame, font=('Times new roman', 14), bg='white',
                                  text="Contact:").place(x=300, y=33,width=100)
        contact_no_entry = Entry(customer_frame, textvariable=self.customer_contact,
                                    font=("Times new Roman", 15, 'bold'),
                                    bg='lightyellow', fg='black', bd=2, relief=RIDGE).place(x=385,y=33,width=120,height=25)

        #----------------------- CALCULATION FRAME --------------------------------=
        calculation_cart_frame=Frame(self.root,bd=2,relief=RIDGE)
        calculation_cart_frame.place(x=440,y=190,width=530,height=360)


        #---------------------- calculator frame --------------------------------+

        calculator_img_frame = Frame(calculation_cart_frame, bd=2, relief=RIDGE)
        calculator_img_frame.place(x=5, y=10, width=268, height=340)

        text_cal_input=Entry(calculator_img_frame,justify=RIGHT, textvariable=self.calc_screen,font=("arial", 17, 'bold'), bg='lightyellow',width=19).grid(row=0,columnspan=4,padx=10,pady=15)

        btn_7=Button(calculator_img_frame,text="7",width=4,bd=5,pady=10,font=('arial',15,'bold'),cursor='hand2',command=lambda:self.get_input(7)).grid(row=1,column=0)
        btn_8=Button(calculator_img_frame,text="8",width=4,bd=5,pady=10,font=('arial',15,'bold'),cursor='hand2',command=lambda:self.get_input(8)).grid(row=1,column=1)
        btn_9=Button(calculator_img_frame,text="9",width=4,bd=5,pady=10,font=('arial',15,'bold'),cursor='hand2',command=lambda:self.get_input(9)).grid(row=1,column=2)
        btn_sum=Button(calculator_img_frame,text="+",width=4,bd=5,pady=10,font=('arial',15,'bold'),cursor='hand2',command=lambda:self.get_input('+')).grid(row=1,column=3)

        btn_4=Button(calculator_img_frame,text="4",width=4,bd=5,pady=10,font=('arial',15,'bold'),cursor='hand2',command=lambda:self.get_input(4)).grid(row=2,column=0)
        btn_5=Button(calculator_img_frame,text="5",width=4,bd=5,pady=10,font=('arial',15,'bold'),cursor='hand2',command=lambda:self.get_input(5)).grid(row=2,column=1)
        btn_6=Button(calculator_img_frame,text="6",width=4,bd=5,pady=10,font=('arial',15,'bold'),cursor='hand2',command=lambda:self.get_input(6)).grid(row=2,column=2)
        btn_subtract=Button(calculator_img_frame,text="-",width=4,bd=5,pady=10,font=('arial',15,'bold'),cursor='hand2',command=lambda:self.get_input('-')).grid(row=2,column=3)

        btn_1=Button(calculator_img_frame,text="1",width=4,bd=5,pady=10,font=('arial',15,'bold'),cursor='hand2',command=lambda:self.get_input(1)).grid(row=3,column=0)
        btn_2=Button(calculator_img_frame,text="2",width=4,bd=5,pady=10,font=('arial',15,'bold'),cursor='hand2',command=lambda:self.get_input(2)).grid(row=3,column=1)
        btn_3=Button(calculator_img_frame,text="3",width=4,bd=5,pady=10,font=('arial',15,'bold'),cursor='hand2',command=lambda:self.get_input(3)).grid(row=3,column=2)
        btn_mult=Button(calculator_img_frame,text="*",width=4,bd=5,pady=10,font=('arial',15,'bold'),cursor='hand2',command=lambda:self.get_input('*')).grid(row=3,column=3)

        btn_0=Button(calculator_img_frame,text="0",width=4,bd=5,pady=10,font=('arial',15,'bold'),cursor='hand2',command=lambda:self.get_input(0)).grid(row=4,column=0)
        btn_C=Button(calculator_img_frame,text="C",width=4,bd=5,pady=10,font=('arial',15,'bold'),cursor='hand2',command=self.clear).grid(row=4,column=1)
        btn_equal=Button(calculator_img_frame,text="=",width=4,bd=5,pady=10,font=('arial',15,'bold'),cursor='hand2',command=self.perform_calc).grid(row=4,column=2)
        btn_div=Button(calculator_img_frame,text="/",width=4,bd=5,pady=10,font=('arial',15,'bold'),cursor='hand2',command=lambda:self.get_input('/')).grid(row=4,column=3)






        #---------------------- Cart frame---------------+
        cart_frame = Frame(self.root, bg="lightyellow", bd=4, relief=RIDGE)
        cart_frame.place(x=720,y=200,width=240,height=340)

        self.cart_lbl=Label(cart_frame, text=" Cart\t Total products:[0]", bg='lightgray',fg='black',font=('Times new Roman',15),width=240,anchor='e')
        self.cart_lbl.pack(side=TOP, fill=X)

        scrolly = Scrollbar(cart_frame, orient=VERTICAL)
        scrollx = Scrollbar(cart_frame, orient=HORIZONTAL)
        #

        self.cart_table = ttk.Treeview(cart_frame, columns=(
        "Prod_id", "Name","Price","Quantity", "Discounted"),
                                          yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)

        scrolly.config(command=self.cart_table.yview)
        scrollx.config(command=self.cart_table.xview)

        self.cart_table.heading("Prod_id", text='P ID')
        self.cart_table.heading("Name", text='Product_Name')
        self.cart_table.heading("Price", text='Price')
        self.cart_table.heading("Quantity", text='Quantity')
        self.cart_table.heading("Discounted", text='Discount_check')


        self.cart_table.bind('<ButtonRelease-1>', self.indv_discount)

        self.cart_table['show'] = 'headings'
        self.cart_table.column('Prod_id', width=20)
        self.cart_table.column('Name', width=150)
        self.cart_table.column('Price', width=80)
        self.cart_table.column('Quantity', width=60)
        self.cart_table.pack(fill=BOTH, expand=1)

        #--- buttons add cart frame ---+
        btns_frame = Frame(self.root, bg="white", bd=4, relief=RIDGE)
        btns_frame.place(x=440, y=550, width=530, height=150)

        label_p_name=Label(btns_frame, text="Product name",bg="white", fg="black", font=("Times new Roman",15,'bold')).place(x=10,y=10)
        product_entry = Entry(btns_frame, textvariable=self.p_name, bg="lightgray", fg="black", font=("Times new Roman",15,'bold')).place(x=10,y=40)

        price_per_quantity = Label(btns_frame, text="Price", bg="white", fg="black",
                             font=("Times new Roman", 15, 'bold')).place(x=250, y=10)
        price_per_quantity_entry = Entry(btns_frame, textvariable=self.p_price, bg="lightgray", fg="black",
                              font=("Times new Roman", 15, 'bold')).place(x=250, y=40,width=150)
        self.In_stock_lbl = Label(btns_frame, bg="white",
                             font=("Times new Roman", 15,),text='In stock [999]')
        self.In_stock_lbl.place(x=10, y=100)

        label_p_quantity = Label(btns_frame, text="Qty", bg="white", fg="black",
                             font=("Times new Roman", 15, 'bold')).place(x=420, y=10)
        quantity_entry = Entry(btns_frame, textvariable=self.p_quantity, bg="lightyellow", fg="black",
                              font=("Times new Roman", 15, 'bold')).place(x=420, y=40,width=40)



        self.add_btn = Button(btns_frame, text="Add | Update cart", font=("Times new Roman", 15, 'bold'),command=self.add_update_cart, bg='orange', fg='black',
                            cursor='hand2').place(x=190, y=100, width=160, height=27)
        self.btn_clear = Button(btns_frame, text="Clear", font=("Times new Roman", 15, 'bold'), bg='gray', fg='black',command=self.clear_cart,
                              cursor='hand2').place(x=360, y=100, width=80, height=27)


        #=========================== BILLING AREA =================================================================================
        customer_bill_frame = Frame(self.root, bg="white", bd=4, relief=RIDGE)
        customer_bill_frame.place(x=980, y=109, width=380, height=440)


        lbl_billing=Label(customer_bill_frame, text="Customer Bill",bg="darkorange",font=("Times new Roman",25,"bold"),bd=2,relief=RIDGE,fg='white',width=40).pack(side=TOP, fill=X)

        self.bill_text_area=Text(customer_bill_frame, bg="white", font=("Times new Roman",8),bd=2,relief=RIDGE)


        scrolly_bill = Scrollbar(customer_bill_frame, orient=VERTICAL)
        scrollx_bill = Scrollbar(customer_bill_frame, orient=HORIZONTAL)

        scrolly_bill.config(command=self.bill_text_area.yview)
        scrollx_bill.config(command=self.bill_text_area.xview)
        scrolly_bill.pack(side=RIGHT, fill=Y)
        scrollx_bill.pack(side=BOTTOM, fill=X)

        self.bill_text_area.pack(side=TOP, fill=BOTH)



        #---------------------PURCHASING BUTTONS --------------------------------------+

        pur_btns_frame=Frame(self.root,bg="white",bd=4,relief=RIDGE)
        pur_btns_frame.place(x=978,y=552,width=380,height=150)

        self.lbl_amt=Label(pur_btns_frame,text="Bill amount\n[0]",font=("goudy old style",15,"bold"),bg="lightblue",fg='black',pady=10,padx=15,bd=3,relief=RIDGE)
        self.lbl_amt.place(x=2,y=5,width=120,height=70)

        self.discount_lbl = Label(pur_btns_frame, text=f" Discounts\nRs.{self.discount}", font=("goudy old style",15, "bold"),
                             bg="yellow", fg='black', pady=10, padx=15, bd=3, relief=RIDGE,cursor='hand2')
        self.discount_lbl.place(x=125, y=5, width=120, height=70)

        self.Net_pay = Button(pur_btns_frame, text="Net pay\n[0]", font=("goudy old style", 15, "bold"),
                             bg="lightblue", fg='black', pady=10, padx=15, bd=3, relief=RIDGE)
        self.Net_pay.place(x=250, y=5, width=120, height=70)

        self.btn_print = Button(pur_btns_frame, text="Print", font=("goudy old style", 15, "bold"),
                                bg="lightblue", fg='black', pady=10, padx=15, bd=3, relief=RIDGE, cursor='hand2',command=self.printing)
        self.btn_print.place(x=2, y=80, width=120, height=50)

        self.lbl_clear_al_btn=Button(pur_btns_frame,text="Clear all",font=("goudy old style",15,"bold"),bg='lightgray',fg='black',cursor='hand2',command=self.clear_all)
        self.lbl_clear_al_btn.place(x=125, y=80, width=120, height=50)

        self.Generate_bill_btn = Button(pur_btns_frame, text="Generate bill", font=("goudy old style", 15, "bold"),
                                       bg='lightgreen', fg='black',cursor='hand2',command=self.calculation_products)
        self.Generate_bill_btn.place(x=250, y=80, width=120, height=50)



        self.show_products()





    def get_input(self,num):
        inp=self.calc_screen.get()+str(num)
        self.calc_screen.set(inp)
    def clear(self):
        self.calc_screen.set('')


    def clear_cart(self):
        self.cart_table.delete(*self.cart_table.get_children())
        self.lbl_amt.config(text="Bill amount\n [0]")
        self.discount_lbl.config(text="Discounts\n [0]")
        self.Net_pay.config(text="Net Pay\n [0]")
        self.p_name.set('')
        self.p_price.set('')
        self.p_quantity.set('')
        self.var_stock_quantity.set('')
        self.In_stock_lbl.config(text='In Stock[]')
        self.cart_list = []
    def clear_all(self):
        del self.cart_list[:]
        self.customer_name.set('')
        self.customer_contact.set('')
        self.clear_cart()
        self.show_products()
        self.show_cart()
        self.discount=0
        self.bill_text_area.delete('1.0', END)

    def perform_calc(self):
        inp=self.calc_screen.get()
        self.calc_screen.set(eval(inp))

    def show_products(self):
        try:
            conn=sqlite3.connect(resource_path('database/shop_database.db'))
            cur=conn.cursor()
            cur.execute('SELECT Prod_id, Name,Price,Quantity, Status from products')
            products=cur.fetchall()

            if len(products)!=0:
                self.product_table.delete(*self.product_table.get_children())
                for row in products:
                    self.product_table.insert('',END,values=row)
            else:
                messagebox.showerror('Error','No products found')
        except Exception as e:



            messagebox.showerror('Error',f'Error due to {e}',parent=self.root)

    def search(self):
            conn = sqlite3.connect(resource_path('database/shop_database.db'))
            cur = conn.cursor()

            if self.search_var.get()!= '':
                try:
                    search_term = '%' + self.search_var.get()+'%'
                    cur.execute('SElect * from products where Name LIKE ?', (search_term,))
                    data = cur.fetchall()
                    print(data)
                    if len(data)>0:

                        self.product_table.delete(*self.product_table.get_children())
                        for char in data:
                            self.product_table.insert('', END, values=char)
                    elif len(data)==0:
                        messagebox.showerror('Error','No data found')
                except Exception as e:
                    messagebox.showerror('Error', f'Error due to {e}')

    def get_data(self, ev):
        selected_item = self.product_table.focus()  # Get the selected item in the Treeview
        if selected_item:
            item_values = self.product_table.item(selected_item, 'values')  # Get the values of the selected item
            if item_values:
                self.p_name.set(item_values[1])
                self.p_price.set(item_values[2])
                # self.var_stock_quantity.set(item_values[4])
                self.In_stock_lbl.config(text=f'In Stock [{str(item_values[3])}]')
                self.var_stock_quantity.set(item_values[3])
                self.p_id.set(item_values[0])


    def add_update_cart(self):
            if self.p_id.get() == '':
                messagebox.showerror('Error', 'Please select a product from the list')
            elif self.p_quantity.get() == '':
                messagebox.showerror('Error', 'Please enter the quantity', parent=self.root)
            elif int(self.p_quantity.get())>int(self.var_stock_quantity.get()):
                messagebox.showerror('Error', 'The stock in not available', parent=self.root)
            else:
                self.prices = float(self.p_price.get()) * float(self.p_quantity.get())
                cart_data = [self.p_id.get(), self.p_name.get(), self.prices, self.p_quantity.get()]

                # Check if the product is already in the cart
                present = False
                index=0
                for item in self.cart_list:
                    if item[0] == self.p_id.get():
                        present = True
                        break
                    index+=1
                if present:
                    op=messagebox.askyesno('warning','You have already inserted product || Do you want to update it?',parent=self.root)
                    if op==True:

                        if self.p_quantity.get() == '0':
                            print(index)
                            print(self.cart_list)
                            self.cart_list.pop(index)  # Remove the item if quantity is 0
                        else:
                                self.cart_list[index][3] = self.p_quantity.get()
                                self.cart_list[index][2] = self.prices

                if not present:
                    self.cart_list.append(cart_data)  # Append new product if not found in the cart

            self.show_cart()

            self.bill_updates()




    def show_cart(self):
        try:
            self.cart_table.delete(*self.cart_table.get_children())
            for row in self.cart_list:

                    self.cart_table.insert('', END, values=row)

        except Exception as e:
            messagebox.showerror('Error',f'Error due to {e}',parent=self.root)

    def bill_updates(self):
        self.bill_price=0
        "Prod_id", "Name", "Price", "Quantity", "Status"
        for char in self.cart_list:
            self.bill_price=self.bill_price +(int(char[2]))


        self.lbl_amt.config(text=f"Bill amount\n [{self.bill_price}]")
        self.cart_lbl.config(text=f'Total products[{len(self.cart_list)}]')
        self.discount_lbl.config(text=f"Discounts\n Rs.{self.discount}")
    def Net_pays(self):
        try:
            net_price = self.bill_price
            self.Net_pay_amount = max(0, net_price)  # Ensure the net pay amount is not negative
        except Exception as e:
            print(f"Error calculating net pay amount: {e}")
            self.Net_pay_amount = 0

        self.Net_pay.config(text=f"Net pay\n[{self.Net_pay_amount}]")

    def calculation_products(self):
        self.products=[]
        self.listing_prices=[]
        self.quantities=[]
        for char in self.cart_list:

            self.products.append(char[1])
            self.listing_prices.append(int(char[2]))
            self.quantities.append(char[3])

        if self.customer_name.get()!='' and self.customer_contact.get()!='':
            # now creating invoice num
            current_date = datetime.datetime.now()
            self.invoice = current_date.strftime('%f%S')



            self.generate_bill()
        elif self.customer_name.get()=='':
            messagebox.showerror("ERROR",'Please enter CUSTOMER NAME',parent=self.root)
        elif self.customer_contact.get()=='':
            messagebox.showerror("ERROR",'Please enter CUSTOMER CONTACT Number',parent=self.root)

    def generate_bill(self):

        self.Net_pays()
        is_sure=messagebox.askokcancel("DOUBLE-CHECK",f'Is {self.customer_contact.get()} correct ? \n\n Note: You must use contact no used earlier if you have due amount to pay ',parent=self.root)

        if is_sure==True:
            self.paid_amount = simpledialog.askinteger("Amount paying", "Enter amount paid by customer", parent=self.root)
            self.due_amount = self.Net_pay_amount - self.paid_amount
            bill_template = f"""
                  ================================
                                 Aarush trade and Suppliers          
                                   Bansgadhi-05,Bardiya   
    
                  Contact:9848086820     Date:{self.formatted_time}                  
                  =================================
                                            Invoice:{self.invoice}           
                  ----------------------------------------------
                  Customer Name: {self.customer_name.get():<41}            
                  Contact No: {self.customer_contact.get():<15}                            
                   Address:             
                  -------------------------------------------------
                  Item                            Quantity       Price      
                  -------------------------------------------------
              """
            # Append each product's details to bill_template
            for i in range(len(self.cart_list)):
                bill_template += f"\t{self.products[i]:<30} {self.quantities[i]:<15} {int(self.listing_prices[i])}\n"

            bill_template += f"""
                  -------------------------------------------------
                  Total:                 \t                 Rs.{int(sum(self.listing_prices))}
                
                  Paid Amount:           \t                 Rs.{self.paid_amount}
                  Due Amount:            \t                 Rs.{self.due_amount}
                  =================================
              """

            # Clear previous bill content
            self.bill_text_area.delete('1.0', END)

            # Insert new bill content
            self.bill_text_area.insert(END, bill_template)
    def updating_database(self):
        try:
            # Connect to the database
            conn = sqlite3.connect(resource_path('database/shop_database.db'))
            cur = conn.cursor()

            # Iterate through each item in the shopping cart
            for item in self.cart_list:
                prod_id, quantity_sold = item[0], int(item[3])

                # Retrieve the current quantity of the product from the database
                cur.execute('SELECT Quantity FROM products WHERE Prod_id = ?', (prod_id,))
                result = cur.fetchone()

                if result:
                    current_quantity = result[0]

                    # Ensure there's enough quantity in stock to fulfill the sale
                    if current_quantity >= quantity_sold:
                        # Update the quantity in the database
                        new_quantity = current_quantity - quantity_sold
                        cur.execute('UPDATE products SET Quantity = ? WHERE Prod_id = ?', (new_quantity, prod_id))
                        conn.commit()
                    else:
                        messagebox.showerror('Error', f'Insufficient quantity in stock for product ID {prod_id}')
                else:
                    messagebox.showerror('Error', f'Product with ID {prod_id} not found in database')

            # Refresh the displayed products
            self.show_products()

        except sqlite3.Error as e:
            conn.rollback()  # Rollback changes if an error occurs
            print('SQLite error:', e)
            messagebox.showerror('Error', 'Database error occurred')
        except Exception as e:
            print('Error:', e)
            messagebox.showerror('Error', f'An unexpected error occurred: {e}')
        finally:
            conn.close()  # Close the database connection

    def printing(self):
        with open(resource_path(f'bills/{self.invoice}.txt',base_path='.'),'w') as file:
            print('a')
            print(self.bill_text_area.get('1.0',END))
            file.write(self.bill_text_area.get('1.0',END))
        product_list=[]

        for char in self.cart_list:
            item={
                "id":char[0],
                "Name":char[1],
                "price":char[2],
                "quantity":char[3]
            }
            product_list.append(item)
        my_list=json.dumps(product_list)


        conn = sqlite3.connect(resource_path('database/shop_database.db'))
        cur=conn.cursor()
        cur.execute('INSERT INTO sales(bill_invoice,Date,Customer_name,products_sold,Net_sales,Paid_amount,unpaid_amount,Contact_no) VALUES(?,?,?,?,?,?,?,?)',(self.invoice,formatted_time, self.customer_name.get(),my_list,self.Net_pay_amount,self.paid_amount,self.due_amount,self.customer_contact.get()))
        conn.commit()

        self.updating_database()
        messagebox.showinfo('Success','Sales recorded successfully',parent=self.root)

    def indv_discount(self,ev):
        data=self.cart_table.focus()
        item_values = self.cart_table.item(data, 'values')

        my_list=[]
        for char in item_values:
            my_list.append(char)

        if  len(my_list)>0:
          discount_percent=simpledialog.askinteger(" Individual discount Discount","Please enter the Discount Percentage",parent=self.root)

          if discount_percent>-1:
                conn = sqlite3.connect(resource_path('database/shop_database.db'))
                cur = conn.cursor()
                cur.execute('SELECT * FROM products where Prod_id=?',(my_list[0],))
                data=cur.fetchone()
                price_per_unit=data[4]

                if len(my_list) < 5:
                    my_list.append('discounted')
                else:
                    price_per_unit_after_earlier_discounting = float(my_list[2]) / int(my_list[3])
                    self.discount =self.discount-(price_per_unit -price_per_unit_after_earlier_discounting) *int(my_list[3])


                self.discount += ((discount_percent) / 100) * price_per_unit *int(my_list[3])


                discounted_price=price_per_unit-(discount_percent/100)*price_per_unit
                net_paying_for_this_product=discounted_price * int(my_list[3])
                my_list[2]=net_paying_for_this_product




                # Update values in self.cart_list
                for char in self.cart_list:
                    if char[0]==my_list[0]:
                        index_=self.cart_list.index(char)
                        self.cart_list[index_]=my_list


                print(self.discount)
                # print(self.Net_pay_amount)

                # Refresh cart_table

                self.show_cart()
                self.bill_updates()
                self.Net_pay.config(text=f"Net pay\n[{self.bill_price}]")




if __name__ == '__main__':
        root = Tk()
        BillingClass(root)
        root.mainloop()
