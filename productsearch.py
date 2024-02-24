from tkinter import *
from tkinter import ttk,messagebox
import sqlite3
from product import productClass

class proview:
    def __init__(self,root):
        ttk.Style().configure("Treeview",background="light blue",
                              foreground="black",fieldbackground="white",
                              font=("calibri",12))
        ttk.Style().configure("Treeview.Heading",
                              font=("calibri",13,'bold'))
        self.root=root
        self.root.geometry("1200x700+220+130")
        self,root.config(bg="white")
        self.root.title("Inventory Management system  >> Developed By Hanska Ravishan")
        self.root.focus_force()


        self.var_searchby=StringVar()
        self.var_search_txt=StringVar()

        #=====search Frame=========
        SearchFrame1=LabelFrame(self.root,text="Search Employee ", bg="white",relief=RIDGE)
        SearchFrame1.place(x=150 ,y= 20 , width=840 ,height=90)


        #=========Option=======
        cmb_search=ttk.Combobox(SearchFrame1,textvariable=self.var_searchby,values=("Select","pid","china_code","nop"),state='readonly',justify=CENTER)
        cmb_search.place(x=10,y=10,width=180,height=40)
        cmb_search.current(0)

        txt_search=Entry(SearchFrame1,textvariable=self.var_search_txt,font=("goudy old style",15),bg="lightyellow").place(x=200,y=10 , width=435 , height=40)
        btn_search=Button(SearchFrame1,command=self.search,text="Search",font=("goudy old style",15),cursor="hand2",bg="green",fg="white").place(x=650 , y=10,height=40)
        btn_showall=Button(SearchFrame1,command=self.show,text="Show All",font=("goudy old style",15),cursor="hand2",bg="green",fg="white").place(x=740 , y=10,height=40)


        btn_addproduct=Button(self.root,command=self.addproduct,text="Add Product",font=("goudy old style",15),cursor="hand2",bg="green",fg="white").place(x=1000 , y=50,height=40)

        pro_frame=Frame(self.root,bd=3,relief=RIDGE)
        pro_frame.place(x=0,y=120 , relwidth=1,height=550)


        scoily=Scrollbar(pro_frame,orient=VERTICAL)
        scoilx=Scrollbar(pro_frame,orient=HORIZONTAL)

        self.producttable=ttk.Treeview(pro_frame,columns=("pid","china_code","catogory","pdes","rprice","wprice","cost","nop","wstock","pstock","cstock","loose"),yscrollcommand=scoily.set)
        scoily.pack(side=RIGHT,fill=Y)
        scoily.config(command=self.producttable.yview)
        self.producttable.heading("pid",text="Product ID")
        self.producttable.heading("china_code",text="China Code")
        self.producttable.heading("catogory",text="Catogory")
        self.producttable.heading("pdes",text="Description")
        self.producttable.heading("rprice",text="Retail Price")
        self.producttable.heading("wprice",text="Wholesale Price")
        self.producttable.heading("cost",text="Cost")
        self.producttable.heading("nop",text="No of pices")
        self.producttable.heading("wstock",text="Warehouse")
        self.producttable.heading("pstock",text="Panadura")
        self.producttable.heading("cstock",text="Colombo")
        self.producttable.heading("loose",text="LOOSE")

        self.producttable["show"]="headings"

        self.producttable.column("pid",width=100)
        self.producttable.column("china_code",width=140)
        self.producttable.column("catogory",width=60,anchor='center')
        self.producttable.column("pdes",width=140,anchor='center')
        self.producttable.column("rprice",width=80,anchor='center')
        self.producttable.column("wprice",width=80,anchor='center')
        self.producttable.column("cost",width=80,anchor='center')
        self.producttable.column("nop",width=80,anchor='center')
        self.producttable.column("wstock",width=80,anchor='center')
        self.producttable.column("pstock",width=80,anchor='center')
        self.producttable.column("cstock",width=80,anchor='center')
        self.producttable.column("loose",width=80,anchor='center')
        

        self.producttable.pack(fill=BOTH,expand=1)
        self.producttable.bind("<ButtonRelease-1>")

        self.show()



    #"pid","china_code","catogory","pdes","rprice","wprice","cost","nop","wstock","pstock","cstock","loose"
    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("Select * from product")
            rows=cur.fetchall()
            self.producttable.delete(*self.producttable.get_children())
            for row in rows:
                self.producttable.insert('',END,values=row)
        except Exception as ex :
            messagebox.showerror("Error",f"Error Due to : {str(ex)}",parent=self.root)

    def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_searchby.get()=="Select":
                messagebox.showerror("Error","Select Search by option",parent=self.root)
            elif self.var_search_txt.get()=="":
                messagebox.showerror("Error","Search Input should be required",parent=self.root)
            else:
            #cur.execute("SELECT * from employee where eid LIKE '%"+self.var_search_txt.get()+"%'")
                cur.execute("Select * from product where "+self.var_searchby.get()+" LIKE '%"+self.var_search_txt.get()+"%'")
                rows=cur.fetchall()
            if len(rows)!=0:
                self.producttable.delete(*self.producttable.get_children())
                for row in rows:
                    self.producttable.insert('',END,values=row)
            else :
                    messagebox.showerror("Error","No Record Found!!",parent=self.root)
        except Exception as ex :
            messagebox.showerror("Error",f"Error Due to : {str(ex)}",parent=self.root)

    def addproduct(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=productClass(self.new_win)


if __name__=="__main__":
    root=Tk()
    obj=proview(root)
    root.mainloop()