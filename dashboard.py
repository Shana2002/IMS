from tkinter import *
from product import productClass
from tkinter import ttk,messagebox
from catogory import catogoryClass
from employee import employeeClass
from productsearch import proview
from customer import customerClass
from billing import Billing
from stocktransfer import stockt
from logitem import logitem
from Billlog import billlog
from balance import balance
import time
import sqlite3
import os


class IMS:
    
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self,root.config(bg="#23252D")
        #Title in Window
        self.root.title("Inventory Management system  >> Developed By Hanska Ravishan")
        title=Label(self.root,text="Inventory Management System", font=("arial",40,"bold"),bg="#111213",fg="white",anchor="w", padx=50).place(x=0,y=0,relwidth=1,height=70)
        
        #btn_Logout
        btn_logout=Button(self.root,text="Logout",font=("times new roman",15,"bold"),bg="yellow",fg="red",cursor="hand2").place(x=1100,y=10,height=50,width=150)
        #clock
        self.lbl_clock1=Label(self.root,text="Welcome to the Inventory Management System\t\t Date: DD-MM-YYYY \t\tTime : HH:MM:SS", font=("times new roman",10),bg="#4d636d",fg="white")
        self.lbl_clock1.place(x=0,y=70,relwidth=1,height=30)


        # left Menu

        LeftMenu = Frame(self.root, bd=2, relief=RIDGE,bg="#111213")
        LeftMenu.place(x=0, y=140, width=250, height=490)

        btn_billing = Button(LeftMenu, text="Billing",command=self.billing, font=("times new roman", 22, "bold"),fg="white", bg="#111213", bd=1,cursor="hand2").pack(side=TOP, fill=X)
        btn_balance = Button(LeftMenu, text="Balances",command=self.balance , font=("times new roman", 22, "bold"),fg="white", bg="#111213", bd=1,cursor="hand2").pack(side=TOP, fill=X)
        btn_st = Button(LeftMenu, text="Stock Transfering",command=self.stocktt , font=("times new roman", 22, "bold"),fg="white", bg="#111213", bd=1,cursor="hand2").pack(side=TOP, fill=X)
        btn_catogory = Button(LeftMenu, text="Catogory",command=self.catogory, font=("times new roman", 22, "bold"),fg="white", bg="#111213", bd=1,cursor="hand2").pack(side=TOP, fill=X)
        btn_viewproduct = Button(LeftMenu, text="View Product",command=self.searchproduct,font=("times new roman", 22, "bold"),fg="white", bg="#111213", bd=1,cursor="hand2").pack(side=TOP, fill=X)
        btn_cus = Button(LeftMenu, text="Customers",command=self.cus , font=("times new roman", 22, "bold"),fg="white", bg="#111213", bd=1,cursor="hand2").pack(side=TOP, fill=X)
        btn_employee = Button(LeftMenu, text="Employee",command=self.employee , font=("times new roman", 22, "bold"),fg="white", bg="#111213", bd=1,cursor="hand2").pack(side=TOP, fill=X)
        btn_sales = Button(LeftMenu,command=self.sales, text="Show Transaction",font=("times new roman", 22, "bold"),fg="white", bg="#111213", bd=1,cursor="hand2").pack(side=TOP, fill=X)
        btn_Exit = Button(LeftMenu, text="Exit", font=("times new roman", 22, "bold"),fg="white", bg="#111213", bd=1,cursor="hand2").pack(side=TOP, fill=X)

        #Content
        btn_log=Button(self.root,command=self.log, text="LOG", font=("times new roman", 22, "bold"),fg="white", bg="#111213", bd=1,cursor="hand2").place(x=1100,y=620,width=250)

        self.lbl_Sales=Label(self.root,text="Total Sales\n [0]",font=("arial",20),bd=5,bg="white",fg="black")
        self.lbl_Sales.place(x=300,y=120,height=150,width=300)

        self.lbl_Catogory = Label(self.root, text="Total Catogory\n [0]", font=("arial", 20), bd=5, bg="white",fg="black")
        self.lbl_Catogory.place(x=650, y=120, height=150, width=300)

        self.lbl_products = Label(self.root, text="Total Products\n [0]", font=("arial", 20), bd=5, bg="white",fg="black")
        self.lbl_products.place(x=1000, y=120, height=150, width=300)

        self.lbl_assest = Label(self.root, text="Total Assest\n [0]", font=("arial", 20), bd=5, bg="#12ffa7",fg="black")
        self.lbl_assest.place(x=300, y=350, height=150, width=300)
        #Footer

        lbl_footer = Label(self.root,text="Welcome to the Inventory Management System || Developed by Hanska Ravishan\t\t Version 1.4",font=("times new roman", 10), bg="#4d636d", fg="white").pack(side=BOTTOM,fill=X)
        lbl=Label(self.root,text="Today ",fg="black").place(x=850,y=430)
        self.update_content()

        cheqt=Frame(self.root,bd=2,relief=RIDGE,bg="light yellow")
        cheqt.place(x=800,y=450,width=500,height=150)
        
        scoily=Scrollbar(cheqt,orient=VERTICAL)
        scoilx=Scrollbar(cheqt,orient=HORIZONTAL)
                                                        #chequid,cusname,states,chequeamt,chequebak
        self.chequetable=ttk.Treeview(cheqt,columns=("bid","cusname","states","pmethod","amount"),yscrollcommand=scoily.set)
        scoily.pack(side=RIGHT,fill=Y)
        scoily.config(command=self.chequetable.yview)
        self.chequetable.heading("bid",text="ID")
        self.chequetable.heading("cusname",text="Customer Name")
        self.chequetable.heading("states",text="States")
        self.chequetable.heading("pmethod",text="Payment M")
        self.chequetable.heading("amount",text="Amount")
#"bid","cusid","cusname","states","chequenum","chequedate","amoubt","chequebank"

        self.chequetable["show"]="headings"

        self.chequetable.column("bid",width=20)
        self.chequetable.column("cusname",width=140)
        self.chequetable.column("states",width=60)
        self.chequetable.column("pmethod",width=60)
        self.chequetable.column("amount",width=60)

        self.chequetable.pack(fill=BOTH,expand=1)
        self.chequetable.bind("<ButtonRelease-1>")
        self.today_show()
        
#=============================================
    def Product(self):
            self.new_win=Toplevel(self.root)
            self.new_obj=productClass(self.new_win)

    def catogory(self):
            self.new_win=Toplevel(self.root)
            self.new_obj=catogoryClass(self.new_win)
    def employee(self):
            self.new_win=Toplevel(self.root)
            self.new_obj=employeeClass(self.new_win)
    def searchproduct(self):
            self.new_win=Toplevel(self.root)
            self.new_obj=proview(self.new_win)
    def billing(self):
            self.new_win=Toplevel(self.root)
            self.new_obj=Billing(self.new_win)
    def sales(self):
            self.new_win=Toplevel(self.root)
            self.new_obj=billlog(self.new_win)
    def cus(self):
            self.new_win=Toplevel(self.root)
            self.new_obj=customerClass(self.new_win)
    def stocktt(self):
            self.new_win=Toplevel(self.root)
            self.new_obj=stockt(self.new_win)
    def log(self):
            self.new_win=Toplevel(self.root)
            self.new_obj=logitem(self.new_win)
    def balance(self):
            self.new_win=Toplevel(self.root)
            self.new_obj=balance(self.new_win)

    def today_show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            date_=time.strftime("%d-%m-%Y")
            today=str(date_)
            cur.execute("Select bid,cusname,states,pmethod,amount from balance where cpdate LIKE '%"+today+"%'")
            rows=cur.fetchall()
            self.chequetable.delete(*self.chequetable.get_children())
            for row in rows:
                self.chequetable.insert('',END,values=row)

            self.chequetable.after(200,self.today_show)
        except Exception as ex :
            messagebox.showerror("Error",f"Error Due to : {str(ex)}",parent=self.root)

        

    def update_content(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            bill1=len(os.listdir('billExcel'))
            self.lbl_Sales.config(text=f"Total Sales\n {str(bill1)}")
            cur.execute("Select * from product")
            product=cur.fetchall()
            self.lbl_products.config(text=f"Total Products\n {str(len(product))}")

            cur.execute("Select * from catogory")
            product=cur.fetchall()
            self.lbl_Catogory.config(text=f"Total Catogory\n {str(len(product))}")
            
                #pid,china,cat,rp,wp,co,nop,ws,p,c,l 
            cur.execute("Select * from product")
            rows=cur.fetchall()
            totp=0
            for row in rows:
                uprice=row[6]
                nop=row[7]
                w=row[8]
                p=row[9]
                c=row[10]
                l=row[11]
                totb=int(int(w)+int(p)+int(c))*int(nop)+int(l)
                tota=int(totb)*int(uprice)
                totp=totp+tota       
            self.lbl_assest.config(text=f"Total Assest\n {str(totp)}")

            time_=time.strftime("%I:%M:%S")
            date_=time.strftime("%d-%m-%Y")
            self.lbl_clock1.config(text=f"Welcome to the Inventory Management System\t\t Date: {str(date_)} \t\tTime : {str(time_)}")
            self.lbl_clock1.after(200,self.update_content)
        except Exception as ex :
            messagebox.showerror("Error",f"Error Due to : {str(ex)}",parent=self.root)



if __name__=="__main__":
    root=Tk()
    obj=IMS(root)
    root.mainloop()