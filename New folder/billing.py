from tkinter import *
from tkinter import ttk,messagebox
import sqlite3
import time
import os
import tempfile
from xlsxwriter import Workbook
from tkinterdnd2 import DND_FILES, TkinterDnD
import xlsxwriter
from customer import customerClass

class Billing:
    
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="white")
        self.cart_list=[]
        self.chk_print=0
        #Title in Window
        self.root.title("Inventory Management system  >> Developed By Hanska Ravishan")
        title=Label(self.root,text="Inventory Management System", font=("arial",40,"bold"),bg="#010c48",fg="white",anchor="w", padx=50).place(x=0,y=0,relwidth=1,height=70)
        
        #btn_Logout
        btn_logout=Button(self.root,text="Logout",font=("times new roman",15,"bold"),bg="yellow",fg="red",cursor="hand2").place(x=1100,y=10,height=50,width=150)
        #clock
        self.lbl_clock=Label(self.root,text="Welcome to the Inventory Management System\t\t Date: DD-MM-YYYY \t\tTime : HH:MM:SS", font=("times new roman",10),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        #============Product Frame=========
        
        self.var_searchby=StringVar()
        self.var_search_txt=StringVar()
        self.var_id=StringVar()
        self.invoice=StringVar()

        ProductFrame1=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        ProductFrame1.place(x=6,y=110,width=900,height=300)

        pTitle=Label(ProductFrame1,text="All Products",font=("times new roman",20,"bold"),bg="black",fg="white").pack(side=TOP,fill=X)

        ProductFrame2=Frame(ProductFrame1,bd=2,relief=RIDGE,bg="white")
        ProductFrame2.place(x=2,y=42,width=888,height=60)

        cmb_search=ttk.Combobox(ProductFrame2,textvariable=self.var_searchby,values=("Select","pid","china_code","nop"),state='readonly',justify=CENTER)
        cmb_search.place(x=10,y=10,width=180,height=20)
        cmb_search.current(0)
        self.var_pro_cat=StringVar()
        self.cat_list=[]
        self.fetch_cat()
        cmb_cat=ttk.Combobox(ProductFrame2,textvariable=self.var_pro_cat,values=self.cat_list,state='readonly',justify=CENTER)
        cmb_cat.place(x=180 , y=35,width=200,height=20)
        cmb_cat.current(0)

        txt_search=Entry(ProductFrame2,textvariable=self.var_search_txt,font=("goudy old style",15),bg="lightyellow").place(x=200,y=10 , width=435 , height=20)
        btn_search=Button(ProductFrame2,text="Search",command=self.product_search,font=("goudy old style",15),cursor="hand2",bg="green",fg="white").place(x=650 , y=10,height=20)
        btn_showall=Button(ProductFrame2,text="Show All",command=self.product_show,font=("goudy old style",15),cursor="hand2",bg="green",fg="white").place(x=740 , y=10,height=20)
        #==========Product Table
        ProductFrame3=Frame(ProductFrame1,bd=2,relief=RIDGE,bg="light yellow")
        ProductFrame3.place(x=2,y=120,width=888,height=150)

        scoily=Scrollbar(ProductFrame3,orient=VERTICAL)
        scoilx=Scrollbar(ProductFrame3,orient=HORIZONTAL)
        self.var_l=StringVar()

        self.producttable=ttk.Treeview(ProductFrame3,columns=("pid","china_code","pdes","rprice","wprice","nop","wstock","pstock","cstock","loose"),yscrollcommand=scoily.set)
        scoily.pack(side=RIGHT,fill=Y)
        scoily.config(command=self.producttable.yview)
        self.producttable.heading("pid",text="Product ID")
        self.producttable.heading("china_code",text="China Code")
        self.producttable.heading("pdes",text="Description")
        self.producttable.heading("rprice",text="Retail Price")
        self.producttable.heading("wprice",text="Wholesale Price")
        self.producttable.heading("nop",text="No of pices")
        self.producttable.heading("wstock",text="Warehouse")
        self.producttable.heading("pstock",text="Panadura")
        self.producttable.heading("cstock",text="Colombo")
        self.producttable.heading("loose",text="Loose")

        self.producttable["show"]="headings"

        self.producttable.column("pid",width=60,anchor='center')
        self.producttable.column("china_code",width=140,anchor='center')
        self.producttable.column("pdes",width=140,anchor='center')
        self.producttable.column("rprice",width=80,anchor='center')
        self.producttable.column("wprice",width=80,anchor='center')
        self.producttable.column("nop",width=60,anchor='center')
        self.producttable.column("wstock",width=60,anchor='center')
        self.producttable.column("pstock",width=60,anchor='center')
        self.producttable.column("cstock",width=60,anchor='center')
        self.producttable.column("loose",width=60,anchor='center')
        

        self.producttable.pack(fill=BOTH,expand=1)
        self.producttable.bind("<ButtonRelease-1>",self.get_data)
        self.product_show()
        
        lbl_note=Label(ProductFrame1,text="Note : Enter 0 Quantity to remove product from cart ",font=("goudy old style",10),bg="white",fg="red").pack(side=BOTTOM,fill=X)

        #========customer frame ==================
        self.var_cus_searchby=StringVar()
        self.var_cus_searchtext=StringVar()

        self.cus_id=StringVar()
        self.cus_name=StringVar()
        self.cus_contact=StringVar()
        self.cus_balance=StringVar()


        cusFrame1=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        cusFrame1.place(x=6,y=420,width=450,height=280)

        cmb_searchcus=ttk.Combobox(cusFrame1,textvariable=self.var_cus_searchby,values=("Select","cusid","cusname","cuscontact"),state='readonly',justify=CENTER)
        cmb_searchcus.place(x=10,y=10,width=60,height=20)
        cmb_searchcus.current(0)

        txt_search=Entry(cusFrame1,textvariable=self.var_cus_searchtext,font=("goudy old style",10),bg="lightyellow").place(x=80,y=10 , width=100 , height=20)
        btn_search=Button(cusFrame1,command=self.cus_search,text="Search",font=("goudy old style",15),cursor="hand2",bg="green",fg="white").place(x=190 , y=10,height=20)
        btn_showall=Button(cusFrame1,command=self.customer_show,text="Show All",font=("goudy old style",15),cursor="hand2",bg="green",fg="white").place(x=290 , y=10,height=20)
        btn_addcus=Button(cusFrame1,command=self.cusadd,text="+",font=("goudy old style",15),cursor="hand2",bg="green",fg="white").place(x=400, y=10,height=20)

        cusFrame3=Frame(cusFrame1,bd=2,relief=RIDGE,bg="light yellow")
        cusFrame3.place(x=2,y=40,width=450,height=230)

        scoily=Scrollbar(cusFrame3,orient=VERTICAL)
        scoilx=Scrollbar(cusFrame3,orient=HORIZONTAL)

        self.custable=ttk.Treeview(cusFrame3,columns=("cusid","cusname","cuscontact","balance"),yscrollcommand=scoily.set)
        scoily.pack(side=RIGHT,fill=Y)
        scoily.config(command=self.custable.yview)
        self.custable.heading("cusid",text="Customer ID")
        self.custable.heading("cusname",text="Customer Name")
        self.custable.heading("cuscontact",text="Contact")
        self.custable.heading("balance",text="Balance")

        self.custable["show"]="headings"

        self.custable.column("cusid",width=60)
        self.custable.column("cusname",width=140)
        self.custable.column("cuscontact",width=140)
        self.custable.column("balance",width=80)
        

        self.custable.pack(fill=BOTH,expand=1)
        self.custable.bind("<ButtonRelease-1>",self.cus_get_data)
        self.customer_show()
        
        #==============cart Frame=====================

        self.var_nops=StringVar()
        self.var_pname=StringVar()
        self.var_uprice=StringVar()
        self.var_qty=StringVar()
        self.var_w=StringVar()
        self.var_p=StringVar()
        self.var_c=StringVar()
        self.var_loc=StringVar()
        self.var_type=StringVar()
    


        cartFrame1=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        cartFrame1.place(x=910,y=110,width=450,height=300)

        self.title2_lbl=Label(cartFrame1,text="\tCart \t\t\t Total Products : [0]",font=("groudy old style",12),bg="light gray",fg="black")
        self.title2_lbl.place(x=0,y=0)

        cartFrame2=Frame(cartFrame1,bd=2,relief=RIDGE,bg="white")
        cartFrame2.place(x=0,y=20,width=450,height=275)

        scoily=Scrollbar(cartFrame2,orient=VERTICAL)
        scoilx=Scrollbar(cartFrame2,orient=HORIZONTAL)

        self.carttable=ttk.Treeview(cartFrame2,columns=("location","pname","qty","uprice","tprice"),yscrollcommand=scoily.set)
        scoily.pack(side=RIGHT,fill=Y)
        scoily.config(command=self.carttable.yview)
        self.carttable.heading("location",text="loc")
        self.carttable.heading("pname",text="China ID")
        self.carttable.heading("uprice",text="Unit Price")
        self.carttable.heading("qty",text="Quantity")
        self.carttable.heading("tprice",text="total")

        self.carttable["show"]="headings"

        self.carttable.column("location",width=10)
        self.carttable.column("pname",width=80)
        self.carttable.column("uprice",width=30)
        self.carttable.column("qty",width=10)
        self.carttable.column("tprice",width=80)
        

        self.carttable.pack(fill=BOTH,expand=1)
        self.carttable.bind("<ButtonRelease-1>",self.get_data_cart)
        
        
        #===========cart widget Button====
        cartwidget=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        cartwidget.place(x=910,y=420,width=450,height=150)

        chinaid=Label(cartwidget,text="China ID",font=("times new roman",15),bg="white").place(x=5,y=5)
        txt_chinaid=Entry(cartwidget,textvariable=self.var_pname,font=("times new roman",15),bg="dark gray",state='readonly').place(x=100,y=5)

        lbl_qty=Label(cartwidget,text="Qty",font=("times new roman",15),bg="white").place(x=200,y=50)
        txt_qty=Entry(cartwidget,textvariable=self.var_qty,font=("times new roman",15),bg="light gray").place(x=250,y=50,width=60)

        clbl_price=Label(cartwidget,text="Unit Price",font=("times new roman",15),bg="white").place(x=10,y=100)
        txt_price=Entry(cartwidget,textvariable=self.var_uprice,font=("times new roman",15),bg="light gray").place(x=130,y=100,width=100)

        lbl_type=Label(cartwidget,text="Type : ",font=("times new roman",15),bg="white").place(x=5,y=50)
        cmb_setlocation1=ttk.Combobox(cartwidget,textvariable=self.var_type,values=("Select","Box","Pices"),state='readonly',justify=CENTER)
        cmb_setlocation1.place(x=60,y=57,width=100,height=20)
        cmb_setlocation1.current(0)

        lbl_loc=Label(cartwidget,text="Location",font=("times new roman",15),bg="white").place(x=335,y=10)
        cmb_setlocation2=ttk.Combobox(cartwidget,textvariable=self.var_loc,values=("Panadura","Warehouse","Colombo"),state='readonly',justify=CENTER)
        cmb_setlocation2.place(x=320,y=40,width=100,height=20)
        cmb_setlocation2.current(0)

        btn_add=Button(cartwidget,command=self.add_update_cart,text="Add to Cart",font=("goudy old style",10,"bold"),cursor="hand2",bg="green",fg="white").place(x=250 , y=100,height=40,width=80)
        btn_clr=Button(cartwidget,command=self.clr_cart,text="Clear",font=("goudy old style",10,"bold"),cursor="hand2",bg="gray",fg="black").place(x=360, y=100,height=40,width=80)

        #===================Bill Frame====================

        billframe=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billframe.place(x=460,y=420,width=450,height=280)

        Btitle=Label(billframe,text="Customer Bill Area",font=("goudy old style",15,"bold"),bg="yellow").pack(side=TOP,fill=X)
        scrolly=Scrollbar(billframe,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)

        self.txt_billarea=Text(billframe,yscrollcommand=scrolly.set)
        self.txt_billarea.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txt_billarea.yview)


        #====================Billing Area============

        billmenuFrame=Frame(self.root,bd=2,relief=RIDGE,bg='white')
        billmenuFrame.place(x=910,y=580,height=100,width=450)

        self.lbl_amt=Label(billmenuFrame,text="Bill Amount\n [0]",font=("times new roman",15,"bold"),bg="light green",fg="black")
        self.lbl_amt.place(x=2,y=5,width=130,height=50)

        btn_print=Button(billmenuFrame,command=self.openexcel,text="Print",cursor="hand2",font=("times new roman",15,"bold"),bg="light blue",fg="black")
        btn_print.place(x=150,y=5,width=130,height=50)

        btn_save=Button(billmenuFrame,text="Save Bill",command=self.gen_bill,cursor="hand2",font=("times new roman",15,"bold"),bg="yellow",fg="black")
        btn_save.place(x=300,y=5,width=130,height=50)

        btn_clear=Button(billmenuFrame,command=self.clear_all,text="Clear ALL",cursor="hand2",font=("times new roman",15,"bold"),bg="Red",fg="black")
        btn_clear.place(x=200,y=60,width=180,height=35)

        

        self.update_t_d()

    #======================Functions=================================================
    def fetch_cat(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("Select name from catogory")
            cat=cur.fetchall()
            self.cat_list.append("Empty")
            if len(cat)>0:
                del self.cat_list[:]
                self.cat_list.append("Select Catogory")
                for i in cat:
                    self.cat_list.append(i[0])   
        except Exception as ex:
            messagebox.showerror("Error",f"Error Due to :{str(ex)}",parent=self.root)
    
    def product_show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("Select pid,china_code,pdes,rprice,wprice,nop,wstock,pstock,cstock,loose from product")
            rows=cur.fetchall()
            self.producttable.delete(*self.producttable.get_children())
            for row in rows:
                self.producttable.insert('',END,values=row)
        except Exception as ex :
            messagebox.showerror("Error",f"Error Due to : {str(ex)}",parent=self.root)
    def cusadd(self):
            self.new_win=Toplevel(self.root)
            self.new_obj=customerClass(self.new_win)
    def product_search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_searchby.get()=="Select":
                messagebox.showerror("Error","Select Search by option",parent=self.root)
            elif self.var_search_txt.get()=="":
                messagebox.showerror("Error","Search Input should be required",parent=self.root)
            else:
            #cur.execute("SELECT * from employee where eid LIKE '%"+self.var_search_txt.get()+"%'")
                if self.var_pro_cat.get()=="Select Catogory":
                    cur.execute("Select pid,china_code,pdes,rprice,wprice,nop,wstock,pstock,cstock,loose from product where "+self.var_searchby.get()+" LIKE '%"+self.var_search_txt.get()+"%'")
                    rows=cur.fetchall()
                    
                else:
                    cur.execute("Select pid,china_code,pdes,rprice,wprice,nop,wstock,pstock,cstock,loose from product where "+self.var_searchby.get()+" LIKE '%"+self.var_search_txt.get()+"%' and catogory like '%"+self.var_pro_cat.get()+"%'")
                    rows=cur.fetchall()
            if len(rows)!=0:
                self.producttable.delete(*self.producttable.get_children())
                for row in rows:
                    self.producttable.insert('',END,values=row)
            else :
                    messagebox.showerror("Error","No Record Found!!",parent=self.root)
        except Exception as ex :
            messagebox.showerror("Error",f"Error Due to : {str(ex)}",parent=self.root)
    
    def get_data(self,ev):
        f=self.producttable.focus()
        content=(self.producttable.item(f))
        row=content['values']
        self.var_id.set(row[0])
        self.var_pname.set(row[1])
        self.var_uprice.set(row[4])
        self.var_nops.set(row[5])
        self.var_w.set(row[6])
        self.var_p.set(row[7])
        self.var_c.set(row[8])
        self.var_l.set(row[9])


    def get_data_cart(self,ev):
        f=self.carttable.focus()
        content=(self.carttable.item(f))
        row=content['values']
        #loc,chinacode,qty,uprice,total
        self.var_pname.set(row[1])
        self.var_uprice.set(row[3])
        self.var_loc.set(row[0])
        self.var_qty.set(row[2])
    
    def add_update_cart(self):
        if self.var_pname.get()=="" :
             messagebox.showerror("Error","Please Select Product from the List",parent=self.root)
        elif self.var_qty.get()=="" :
            messagebox.showerror("Error","Please Enter Quantity",parent=self.root)
        elif self.var_loc.get()=="Select" :
            messagebox.showerror("Error","Please Select Picking Location Quantity",parent=self.root)
        elif self.var_type.get()=="Select" :
            messagebox.showerror("Error","Please Select type Location Quantity",parent=self.root)
        else:
            get=0 
            if self.var_type.get()=="Box" :
                if self.var_loc.get()=="Panadura":
                    if int(self.var_p.get())-int(self.var_qty.get())>=0:
                        get=1
                elif self.var_loc.get()=="Warehouse":
                    if int(self.var_w.get())-int(self.var_qty.get())>=0:
                        get=1
                else:
                    if int(self.var_c.get())-int(self.var_qty.get())>=0:                   
                        get=1
                if get==1:   
                    price_cal=(int(self.var_qty.get())*int(self.var_nops.get())*int(self.var_uprice.get()))
                    totqty=(int(self.var_qty.get())*int(self.var_nops.get()))
                    qty=(str(self.var_qty.get()))
                    #loc,pname,totqty,uprice,price_cal,nop,w,p,c,l,bol
                    cart_data=[self.var_loc.get(),self.var_pname.get(),totqty,self.var_uprice.get(),price_cal,self.var_nops.get(),self.var_w.get(),self.var_p.get(),self.var_c.get(),self.var_l.get(),self.var_type.get()]
                    #===============cart Update=======
                    present='no'
                    index_=0
                    for row in self.cart_list:
                        if self.var_pname.get()==row[1]:
                            present='yes'
                            break
                        index_+=1
                    if present=='yes':
                        op=messagebox.askyesno('Confirm',"Product Already present \n do you want to Update | remove from cart List",parent=self.root)
                        if op==True:
                            if self.var_qty.get()=="0":
                                self.cart_list.pop(index_)
                            else:
                                #loc,pname,totqty,uprice,price_cal,nop,w,p,c,l,bol
                                self.cart_list[index_][0]=self.var_loc.get()
                                self.cart_list[index_][2]=self.var_qty.get()
                                self.cart_list[index_][3]=self.var_uprice.get()
                                self.cart_list[index_][4]=price_cal
                                self.cart_list[index_][5]=self.var_nops.get()
                                self.cart_list[index_][6]=self.var_w.get()
                                self.cart_list[index_][7]=self.var_p.get()
                                self.cart_list[index_][8]=self.var_c.get()
                                self.cart_list[index_][9]=self.var_l.get()
                                self.cart_list[index_][10]=self.var_type.get()
                                
                    else:
                        self.cart_list.append(cart_data)
                else:
                    messagebox.showerror("Error","location BOX not enough!!",parent=self.root)
            else :
                
                price_cal=(int(self.var_qty.get())*int(self.var_uprice.get()))
                totqty=int(self.var_qty.get())
                qty=(str(self.var_qty.get()))
                #loc,pname,totqty,uprice,price_cal,nop,w,p,c,l,bol
                cart_data=[self.var_loc.get(),self.var_pname.get(),totqty,self.var_uprice.get(),price_cal,self.var_nops.get(),self.var_w.get(),self.var_p.get(),self.var_c.get(),self.var_l.get(),self.var_type.get()]
                #===============cart Update=======
                present='no'
                index_=0
                for row in self.cart_list:
                    if self.var_pname.get()==row[1]:
                        present='yes'
                        break
                    index_+=1
                if present=='yes':
                    op=messagebox.askyesno('Confirm',"Product Already present \n do you want to Update | remove from cart List",parent=self.root)
                    if op==True:
                        if self.var_qty.get()=="0":
                            self.cart_list.pop(index_)
                        else:
                            #loc,pname,totqty,uprice,price_cal,nop,w,p,c,l,bol
                            self.cart_list[index_][0]=self.var_loc.get()
                            self.cart_list[index_][2]=self.var_qty.get()
                            self.cart_list[index_][3]=self.var_uprice.get()
                            self.cart_list[index_][4]=price_cal
                            self.cart_list[index_][5]=self.var_nops.get()
                            self.cart_list[index_][6]=self.var_w.get()
                            self.cart_list[index_][7]=self.var_p.get()
                            self.cart_list[index_][8]=self.var_c.get()
                            self.cart_list[index_][9]=self.var_l.get()
                            self.cart_list[index_][10]=self.var_type.get()
                            
                else:
                    self.cart_list.append(cart_data)
                
            self.show_cart()
            self.bill_updates()

    def bill_updates(self):
        self.bill_amt=0
        for row in self.cart_list:
            self.bill_amt=self.bill_amt+float(row[4])

        self.lbl_amt.config(text=f'Bill Amount\n {str(self.bill_amt)}')
        self.title2_lbl.config(text=f"\tCart \t\t\t Total Products : {str(len(self.cart_list))}")  

    def show_cart(self):
        try:
            
            self.carttable.delete(*self.carttable.get_children())
            
            for row in self.cart_list:
                self.carttable.insert('',END,values=row)
        except Exception as ex :
            messagebox.showerror("Error",f"Error Due to : {str(ex)}",parent=self.root)
    #==========================Customer========================
    def customer_show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("Select cusid,cusname,cuscontact,balance from customer")
            rows=cur.fetchall()
            self.custable.delete(*self.custable.get_children())
            for row in rows:
                self.custable.insert('',END,values=row)
        except Exception as ex :
            messagebox.showerror("Error",f"Error Due to : {str(ex)}",parent=self.root)

    def cus_search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_cus_searchby.get()=="Select":
                messagebox.showerror("Error","Select Search by option",parent=self.root)
            elif self.var_cus_searchtext.get()=="":
                messagebox.showerror("Error","Search Input should be required",parent=self.root)
            else:
            #cur.execute("SELECT * from employee where eid LIKE '%"+self.var_search_txt.get()+"%'")
                cur.execute("Select cusid,cusname,cuscontact,balance from customer where "+self.var_cus_searchby.get()+" LIKE '%"+self.var_cus_searchtext.get()+"%'")
                rows=cur.fetchall()
            if len(rows)!=0:
                self.custable.delete(*self.custable.get_children())
                for row in rows:
                    self.custable.insert('',END,values=row)
            else :
                    messagebox.showerror("Error","No Record Found!!",parent=self.root)
        except Exception as ex :
            messagebox.showerror("Error",f"Error Due to : {str(ex)}",parent=self.root)
    
    def cus_get_data(self,ev):
        f=self.custable.focus()
        content=(self.custable.item(f))
        row=content['values']
        self.cus_id.set(row[0])
        self.cus_name.set(row[1])
        self.cus_contact.set(row[2])
        self.cus_balance.set(row[3])

    #================Generate Bill===================================
    
    def gen_bill(self):
        
        if self.cus_id.get()=="":
            messagebox.showerror("Error","Select Customer or add Customer",parent=self.root)
        elif len(self.cart_list)==0:
            messagebox.showerror("Error","Please Add Products to cart",parent=self.root)
        else:
            self.chk_print=1
            #=======Bill Top============
            self.bill_top()
            #=======Bill Middle=========
            self.bill_middle()
            #=======Bill Bottom=========
            self.bill_bottom()
           
            fp=open(f'billtxt/{str(self.invoice)}.txt','w')
            fp.write(self.txt_billarea.get('1.0',END))
            fp.close()
            messagebox.showinfo('Saved',"Bill Has Been Saved in Backend",parent=self.root)
            

    
            

    def bill_top(self):
        self.invoice=len(os.listdir('billExcel'))+1
        bill_top_temp=f'''
\t\tThushara Photo Framing
\t\tBilling Management
{str("="*47)}
Customer Name: {self.cus_name.get()}
Phone No     : {self.cus_contact.get()}
Bill no. {str(self.invoice)}\t\tDate: {str(time.strftime("%d-%m-%Y"))}
{str("="*47)}
loc\tProduct Name\t\t\tQTY\tPrice
{str("="*47)}'''

        self.txt_billarea.delete('1.0',END)
        self.txt_billarea.insert('1.0',bill_top_temp)

    def bill_bottom(self):
        bill_bottom_temp=f'''
{str("="*47)}
Bill Amount\t\t\tRs.{self.bill_amt}
{str("="*47)}
        '''
        self.txt_billarea.insert(END,bill_bottom_temp)

    def bill_middle(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            logdate=str(time.strftime("%d-%m-%Y"))
            for row in self.cart_list:
                #loc,pname,totqty,uprice,price_cal,nop,w,p,c,l
                lock=row[0]
                name=row[1]
                qty=row[2]
                uprice=row[3]
                price=str(row[4])
                nop=int(row[5])
                w=row[6]
                p=row[7]
                c=row[8]
                l=row[9]
                lob=row[10]
                #logid,cusname,pid,china code,type,date
                if lob=="Box":
                    qty1=int(qty)/nop
                    qty1=int(qty1)
                else:
                    qty1=qty
                cur.execute("Insert into logitem (cusname,china_code,loc,type,qty,unitp,date) values (?,?,?,?,?,?,?)",(

                    self.cus_name.get(),
                    name,
                    lock,
                    lob,
                    qty1,
                    uprice,
                    logdate,

                    
                    ))
                con.commit()

                self.txt_billarea.insert(END,"\n"+lock+"\t"+name+"\t\t\t"+str(row[2])+"\t"+price)
                if lob=="Box":
                    if lock=="Panadura":
                        balp=int(p)-int(qty/nop)
                        balw=int(w)-0
                        balc=int(c)-0
                        ball=int(l)-0
                    elif lock=="Warehouse":
                        balp=int(p)-0
                        balw=int(w)-int(qty/nop)
                        balc=int(c)-0
                        ball=int(l)-0
                    else:
                        balp=int(p)-0
                        balw=int(w)-0
                        balc=int(c)-int(qty/nop)
                        ball=int(l)-0
                else:
                    ball=int(l)-int(qty)
                    balp=int(p)-0
                    balw=int(w)-0
                    balc=int(c)-0
                    if ball<0:
                        ball=0
                cur.execute("Update product set wstock=?,pstock=?,cstock=?,loose=? where china_code=?",(
                        balw,
                        balp,
                        balc,
                        ball,
                        name,
                    ))
                con.commit()
            
            self.product_show()
            self.excel()
            states="NON-Selected"
            #bid,cusid,cusname,date,invoicenum,amount,states,pmethod,cpdate
            cur.execute("Insert into balance (cusid,cusname,date,invoicenum,amount,states) values (?,?,?,?,?,?)",(
                    
                    self.cus_id.get(),
                    self.cus_name.get(),
                    logdate,
                    self.invoice,
                    self.bill_amt,
                    states,
                    
                    ))
            con.commit()
            con.close()   
        except Exception as ex:
            messagebox.showerror("Error",f"Error Due to :{str(ex)}")
        


    def excel(self):

        
        Workbook=xlsxwriter.Workbook(f'billExcel/{str(self.invoice)}.xlsx')
        worksheet=Workbook.add_worksheet()
                    
        worksheet.set_paper(11)  # A5 size
        worksheet.set_margins(
                                left=0.25,
                                right=0.25,
                                top=0.75,
                                bottom=0.75)
        worksheet.set_header(header='&C&25&"Times New Roman"Thushara Phot Framing',)
        bold_font=Workbook.add_format({'bold': True})
        textformat=Workbook.add_format()
        textformat.set_font_size(11)
        border=Workbook.add_format()
        border.set_border()
        border.set_align('center')
        border.set_font("Times New Roman")
        border.set_font_size(12)
        invoice=Workbook.add_format()
        invoice.set_align('center')
        invoice.set_align('vcenter')
        invoice.set_font("Bahnschrift SemiBold Condensed")
        invoice.set_font_size(28)
        date_format=Workbook.add_format({'num_format':"mmmm d yyyy"})
        date_format.set_align('center')
        date_format.set_border()

        border1=Workbook.add_format()
        border1.set_border()
        border1.set_font("Times New Roman")

        border2=Workbook.add_format()
        border2.set_border()
        border2.set_align('center')
        border2.set_font("Times New Roman")
        border2.set_font_size(12)
        border2.set_bold()
        border2.set_bg_color("#D3D3D3")

        worksheet.set_column('A:A', 4)
        worksheet.set_column('B:B', 24)
        worksheet.set_column('C:C', 7.43)
        worksheet.set_column('D:D', 10.86)
        worksheet.set_column('E:E', 15)



        worksheet.merge_range('A2:B6',"INVOICE",invoice)


        #======Heading Branches

        worksheet.write('C1',"Branches",bold_font)
        worksheet.write('C2',"NO. 44 ,Prince Street,",textformat)
        worksheet.write('C3',"Colombo-11",textformat)
        worksheet.write('C4',"TEl: 0726153040",textformat)
        worksheet.write('C5',"Mob:-  072-6153040 ",textformat)
        worksheet.write('C6',"       077-7148851",textformat)

        worksheet.write('E1',"Branches",bold_font)
        worksheet.write('E2',"NO. 44 ,Prince Street,",textformat)
        worksheet.write('E3',"Colombo-11",textformat)
        worksheet.write('E4',"TEl: 0726153040",textformat)
        worksheet.write('E5',"Mob:-  072-6153040 ",textformat)
        worksheet.write('E6',"       077-7148851",textformat)

        worksheet.merge_range("A8:B8","Customer ",border)
        worksheet.merge_range("A9:B9",str(self.cus_name.get()),border)

        worksheet.write('D8',"Invoice No.",border)
        worksheet.write('D9',"Date",border)

        #==============Price Table===================

        worksheet.write('A11','No',border2)
        worksheet.write('B11','Description',border2)
        worksheet.write('C11','QTY',border2)
        worksheet.write('D11','Unit',border2)
        worksheet.write('E11','Amount',border2)

        worksheet.write('A12','1',border)
        worksheet.write('A13','2',border)
        worksheet.write('A14','3',border)
        worksheet.write('A15','4',border)
        worksheet.write('A16','5',border)
        worksheet.write('A17','6',border)
        worksheet.write('A18','7',border)
        worksheet.write('A19','8',border)
        worksheet.write('A20','9',border)
        worksheet.write('A21','10',border)
        worksheet.write('A22','11',border)
        worksheet.write('A23','12',border)
        worksheet.write('A24','13',border)
        worksheet.write('A25','14',border)
        worksheet.write('A26','15',border)
        worksheet.write('A27','16',border)

        worksheet.merge_range('A28:D28','TOTAL',border)
        worksheet.write('A29','Date',border)
        worksheet.merge_range('C29:D29','Balance',border)
        worksheet.merge_range('C30:D30',"SUB Total",border)

        worksheet.write('B12','',border)
        worksheet.write('B13','',border)
        worksheet.write('B14','',border)
        worksheet.write('B15','',border)
        worksheet.write('B16','',border)
        worksheet.write('B17','',border)
        worksheet.write('B18','',border)
        worksheet.write('B19','',border)
        worksheet.write('B20','',border)
        worksheet.write('B21','',border)
        worksheet.write('B22','',border)
        worksheet.write('B23','',border)
        worksheet.write('B24','',border)
        worksheet.write('B25','',border)
        worksheet.write('B26','',border)
        worksheet.write('B27','',border)

        worksheet.write('C12','',border)
        worksheet.write('C13','',border)
        worksheet.write('C14','',border)
        worksheet.write('C15','',border)
        worksheet.write('C16','',border)
        worksheet.write('C17','',border)
        worksheet.write('C18','',border)
        worksheet.write('C19','',border)
        worksheet.write('C20','',border)
        worksheet.write('C21','',border)
        worksheet.write('C22','',border)
        worksheet.write('C23','',border)
        worksheet.write('C24','',border)
        worksheet.write('C25','',border)
        worksheet.write('C26','',border)
        worksheet.write('C27','',border)

        worksheet.write('D12','',border)
        worksheet.write('D13','',border)
        worksheet.write('D14','',border)
        worksheet.write('D15','',border)
        worksheet.write('D16','',border)
        worksheet.write('D17','',border)
        worksheet.write('D18','',border)
        worksheet.write('D19','',border)
        worksheet.write('D20','',border)
        worksheet.write('D21','',border)
        worksheet.write('D22','',border)
        worksheet.write('D23','',border)
        worksheet.write('D24','',border)
        worksheet.write('D25','',border)
        worksheet.write('D26','',border)
        worksheet.write('D27','',border)

        worksheet.write('E12','',border)
        worksheet.write('E13','',border)
        worksheet.write('E14','',border)
        worksheet.write('E15','',border)
        worksheet.write('E16','',border)
        worksheet.write('E17','',border)
        worksheet.write('E18','',border)
        worksheet.write('E19','',border)
        worksheet.write('E20','',border)
        worksheet.write('E21','',border)
        worksheet.write('E22','',border)
        worksheet.write('E23','',border)
        worksheet.write('E24','',border)
        worksheet.write('E25','',border)
        worksheet.write('E26','',border)
        worksheet.write('E27','',border)
        worksheet.write('E28','',border)
        worksheet.write('E29','',border)
        worksheet.write('E30','',border)

        #loc,pname,totqty,uprice,price_cal,nop,w,p,c,l

        worksheet.write('E8',str(self.invoice),border)
        worksheet.write('E9',time.strftime("%d-%m-%Y"),date_format)

        x=11
        int(x)
        col=0
        int(col)
        for row in(self.cart_list):
            if row[10]=="Box":
                box=int(row[2])/int(row[5])
                box=int(box)
                worksheet.write(x,col+1,f"{row[1]} (Box - {box})",border)
            else:
                worksheet.write(x,col+1,row[1],border)
            worksheet.write_number(x,col+2,int(row[2]),border1)
            worksheet.write_number(x,col+3,int(row[3]),border1)
            worksheet.write_number(x,col+4,int(row[4]),border1)
            
            x+=1

        worksheet.write_number('E28',int(self.bill_amt),border)
        Workbook.close()
        
 
            


    def clr_cart(self):
        self.var_pname.set("")
        self.var_uprice.set("")
        self.var_loc.set("Panadura")
        self.var_qty.set("")
        self.var_type.set("Select")


    def clear_all(self):
        del self.cart_list[:]
        self.cus_name.set('')
        self.cus_id.set('')
        self.cus_contact.set('')
        self.cus_balance.set('')
        self.txt_billarea.delete('1.0',END)
        self.clr_cart()
        self.product_show()
        self.show_cart()
        self.customer_show()
        self.title2_lbl.config(text=f"\tCart \t\t\t Total Products : [0]")
        self.chk_print=0

    def update_t_d (self):
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome to the Inventory Management System\t\t Date: {str(date_)} \t\tTime : {str(time_)}")
        self.lbl_clock.after(200,self.update_t_d)


    def openexcel(self):
        if self.chk_print==1:
            messagebox.showinfo('Print',"Please Waiting Printing",parent=self.root)
            os.startfile(f'billExcel\\{str(self.invoice)}.xlsx')  
        else:
            messagebox.showerror('Print',"Please Generate Bill To Print the recipt",parent=self.root) 
        
            
       
if __name__=="__main__":
    root=Tk()
    obj=Billing(root)
    root.mainloop()
