from tkinter import *
from tkinter import ttk, messagebox

from PIL import ImageTk, Image
import sqlite3,os,sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



class CategoryClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Product Manager")
        self.root.geometry("1100x580+260+130")
        self.root.title("Categories")
        self.root.config(bg="white")


        #+===============     Variables    =================
        self.category_name=StringVar()

        title=Label(self.root, text="Manage Product Category", font=("goudy old style",30), bg="#0D9276",bd=2,relief=RIDGE).pack(side=TOP, fill=X,padx=11,pady=20)

        title=Label(self.root, text="ENTER YOUR CATEGORY", font=("goudy old style",30), bg="white").place(x=40,y=100)


        self.category_entry=Entry(self.root, text="ENTER YOUR CATEGORY",textvariable=self.category_name, font=("goudy old style",18), bg="lightyellow").place(x=60,y=180,width=300)

        #+==========Button=========================
        btn_add=Button(self.root, text="Add",command=self.add, font=("goudy old style",14),bg='green').place(x=380,y=180,width=150,height=30)
        btn_delete=Button(self.root, text="Delete", font=("goudy old style",14),command=self.delete_data, bg='red').place(x=540,y=180,width=150,height=30)

        self.root.focus_force()

        #+++++  Adding Frame ##+++

        cat_frame=Frame(self.root, bg="lightyellow",bd=2,relief=RIDGE)
        cat_frame.place(x=700,y=100,width=400,height=100)

        scrolly=Scrollbar(cat_frame,orient=VERTICAL)
        scrollx=Scrollbar(cat_frame,orient=HORIZONTAL)


        self.category_table=ttk.Treeview(cat_frame,columns=("cid","names"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)

        scrolly.config(command=self.category_table.yview)
        scrollx.config(command=self.category_table.xview)
        self.category_table.heading("cid",text='Category ID')
        self.category_table.heading("names",text='Category Names')
        self.category_table.bind('<<TreeviewSelect>>',self.get_data)
        #
        # self.category_table.column("#0", stretch=NO, minwidth=0, width=0)  # Hide first default column or you can try code below

        self.category_table['show'] = 'headings'


        self.category_table.pack(fill=BOTH, expand=1)

        self.show()



        ##++++++++  Adding Images #+=========================

        cat_one_img=Image.open(resource_path("images/category_img.jpg"))
        cat_two_img=Image.open(resource_path("images/sec.jpg"))
        cat_one_img.thumbnail((400,400))
        cat_two_img.thumbnail((400,400))

        first_image=ImageTk.PhotoImage(cat_one_img)
        second_image=ImageTk.PhotoImage(cat_two_img)



        fir_img = Label(self.root,image=first_image,bd=2,relief=RIDGE)
        fir_img.image = first_image

        sec_img = Label(self.root,image=second_image,bd=2,relief=RIDGE)
        sec_img.image = second_image


        fir_img.place(x=50,y=250,width=400,height=290)
        sec_img.place(x=600,y=250,width=400,height=300)


    #==============database+====================
    def add(self):
        conn = sqlite3.connect(resource_path('database/shop_database.db'))
        cur=conn.cursor()
        # print(self.category_name)
        # print(self.category_name.get())
        # print(type(self.category_name.get()))
        try:
            if self.category_name.get() == "":
                messagebox.showerror("Error","Category name must be required",parent=self.root)
            else:
                cur.execute("Select * from category where names=? ",(self.category_name.get(),))
                row=cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error","The category already exists",parent=self.root)
                else:
                    cur.execute("INSERT INTO category(names) VALUES (?)", (self.category_name.get(),))

                    conn.commit()
                    messagebox.showinfo("Done",f"{self.category_name.get()} added succesfully",parent=self.root)
                    self.show()





        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {ex}")


#+++++ showing data in treeview #++++++++++++++++++++

    def show(self):
        conn = sqlite3.connect(resource_path('database/shop_database.db'))
        cur=conn.cursor()
        try:
            self.category_table.delete(*self.category_table.get_children())
            cur.execute("select * from category")
            rows=cur.fetchall()
            for row in rows:
                self.category_table.insert('',END,values=row)
        except Exception as ex:

            messagebox.showerror("Error",f"Error due to {ex}",parent=self.root)


    ################# SELECTING THE REQUIRED DATA ################################
    def get_data(self, ev):
        selected_item = self.category_table.focus()  # Get the selected item in the Treeview
        if selected_item:  # Ensure an item is selected
            item_values = self.category_table.item(selected_item, 'values')  # Get the values of the selected item
            if item_values:  # Ensure values exist
                self.category_name.set(item_values[1])  # Assuming category name is the second column (index 1)

    def delete_data(self):
        if self.category_name.get() == "":
            messagebox.showerror("Error","Please select a category to delete",parent=self.root)
        else:
            try:
                conn = sqlite3.connect(resource_path('database/shop_database.db'))
                cur=conn.cursor()
                cur.execute('SELECT * FROM category WHERE names=?',(self.category_name.get(),))
                row=cur.fetchone()
                if row==NONE:
                    messagebox.showerror("Error","No such category",parent=self.root)
                else:

                    ask_ok_cancel=messagebox.askokcancel("Warning",f"Do you really want to delete {self.category_name.get()} category ?",parent=self.root)
                    if ask_ok_cancel:
                        cur.execute('DELETE FROM category WHERE names=?',(self.category_name.get(),))
                        conn.commit()
                        messagebox.showinfo("Done",f"{self.category_name.get()} Category deleted successfully from database",parent=self.root)
                        self.show()
            except Exception as ex:
                messagebox.showerror("Error",f"Error due to {ex}",parent=self.root)






###===Getting data in  form upon clicking +++++++++++++++++++



if __name__ == "__main__":
    root=Tk()
    CategoryClass(root)
    root.mainloop()