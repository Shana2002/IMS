from tkinter import *
from tkinter import ttk,messagebox
import sqlite3
import time
from cheque import cheque

class balance:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self,root.config(bg="white")
        self.root.title("Inventory Management system  >> Developed By Hanska Ravishan")
        self.root.focus_force()

        title=Label(self.root,text="Balance Log", font=("arial",40,"bold"),bg="#010c48",fg="white",anchor="w", padx=350).place(x=0,y=0,relwidth=1,height=70)

        #bid,cusid,cusname,date,invoicenum,amount,states,pmethod,cpdate
        self.var_bid=StringVar()
        self.var_cusid=StringVar()
        self.var_cusname=StringVar()
        self.var_date=StringVar()
        self.var_invoice=StringVar()
        self.var_amt=StringVar()
        self.var_states=StringVar()
        self.var_pmethod=StringVar()
        self.var_cpdate=StringVar()

        self.searchby_che=StringVar()
        self.searchtxt_che=StringVar()
        self.searchstate_che=StringVar()

        SearchFrame1=LabelFrame(self.root,text="Search ", bg="white",relief=RIDGE)
        SearchFrame1.place(x=2 ,y= 100 , width=1000 ,height=70)


        #=========Option=======
        cmb_searchstate=ttk.Combobox(SearchFrame1,textvariable=self.searchstate_che,values=("NON-Selected","Need Payment","Payment Done"),state='readonly',justify=CENTER)
        cmb_searchstate.place(x=10,y=14,width=160)
        cmb_searchstate.current(0)

        cmb_search=ttk.Combobox(SearchFrame1,textvariable=self.searchby_che,values=("Select","cusid","cusname","invoicenum","date","states","amount","pmethod","cpdate"),state='readonly',justify=CENTER)
        cmb_search.place(x=180,y=14,width=160)
        cmb_search.current(0)

        txt_search=Entry(SearchFrame1,textvariable=self.searchtxt_che,font=("goudy old style",15),bg="lightyellow").place(x=350,y=10,width=300)
        btn_search=Button(SearchFrame1,command=self.billSearch,text="Search",font=("goudy old style",15),cursor="hand2",bg="green",fg="white").place(x=650 , y=10,height=30)
        btn_showall=Button(SearchFrame1,command=self.showblogall,text="Show All",font=("goudy old style",15),cursor="hand2",bg="green",fg="white").place(x=750 , y=10,height=30)
        btn_today=Button(SearchFrame1,command=self.todaybill,text="Today Bills",font=("goudy old style",15),cursor="hand2",bg="red",fg="white").place(x=850 , y=10,height=30)
        
        #Table=============
        cheqt=Frame(self.root,bd=2,relief=RIDGE,bg="light yellow")
        cheqt.place(x=2,y=200,width=1000,height=500)
        

        scoily=Scrollbar(cheqt,orient=VERTICAL)
        scoilx=Scrollbar(cheqt,orient=HORIZONTAL)
#bid,cusid,cusname,date,invoicenum,amount,states,pmethod,cpdate
        self.chequetable=ttk.Treeview(cheqt,columns=("bid","cusid","cusname","date","invoicenum","amount","states","pmethod","cpdate"),yscrollcommand=scoily.set)
        scoily.pack(side=RIGHT,fill=Y)
        scoily.config(command=self.chequetable.yview)
        self.chequetable.heading("bid",text="ID")
        self.chequetable.heading("cusid",text="Customer ID")
        self.chequetable.heading("cusname",text="Customer Name")
        self.chequetable.heading("date",text="Bill Date")
        self.chequetable.heading("invoicenum",text="Invoice Num")
        self.chequetable.heading("amount",text="Amount")
        self.chequetable.heading("states",text="States")
        self.chequetable.heading("pmethod",text="Payment Method")
        self.chequetable.heading("cpdate",text="Paid Date")


        self.chequetable["show"]="headings"

        self.chequetable.column("bid",width=10)
        self.chequetable.column("cusid",width=10)
        self.chequetable.column("cusname",width=140)
        self.chequetable.column("date",width=60)
        self.chequetable.column("invoicenum",width=40)
        self.chequetable.column("amount",width=60)
        self.chequetable.column("states",width=60)
        self.chequetable.column("pmethod",width=40)
        self.chequetable.column("cpdate",width=40)

        self.chequetable.pack(fill=BOTH,expand=1)
        self.chequetable.bind("<ButtonRelease-1>",self.balance_get_data)

        chequeentryframe=Frame(self.root,bd=3,relief=RIDGE,bg="Light yellow")
        chequeentryframe.place(x=1010,y=100,width=350,height=550)
        #Side Window
        lbl_ID=Label(chequeentryframe,       text="Customer ID  ",font=("Times new roman",15),bg="Light yellow",fg="black").place(x=10,y=10)
        lbl_name=Label(chequeentryframe,     text="Customer Name ",font=("Times new roman",15),bg="Light yellow",fg="black").place(x=10,y=40)
        lbl_bdate=Label(chequeentryframe, text="Bill Date ",font=("Times new roman",15),bg="Light yellow",fg="black").place(x=10,y=100)
        lbl_invoicenum=Label(chequeentryframe,text="Invoice Number ",font=("Times new roman",15),bg="Light yellow",fg="black").place(x=10,y=130)
        lbl__amt=Label(chequeentryframe,     text="Amount ",font=("Times new roman",15),bg="Light yellow",fg="black").place(x=10,y=160)
        lbl_states=Label(chequeentryframe,text="States :",font=("Times new roman",15),bg="Light yellow",fg="black").place(x=40,y=220)
        lbl_paymentmethod=Label(chequeentryframe,text="Payment Method :",font=("Times new roman",15),bg="Light yellow",fg="black").place(x=10,y=270)
        lbl_paiddate=Label(chequeentryframe,text="Paid Date",font=("Times new roman",15),bg="Light yellow",fg="black").place(x=10,y=350)

        txt_ID=Entry(chequeentryframe,textvariable=self.var_cusid,font=("Times new roman",13),state='readonly',bg="white",fg="black").place(x=150,y=10)
        txt_name=Entry(chequeentryframe,textvariable=self.var_cusname,font=("Times new roman",13),state='readonly',bg="white",fg="black").place(x=150,y=40)
        txt_bdate=Entry(chequeentryframe,textvariable=self.var_date,font=("Times new roman",13),state='readonly',bg="white",fg="black").place(x=150,y=100)
        txt_invoice=Entry(chequeentryframe,textvariable=self.var_invoice,font=("Times new roman",13),state='readonly',bg="white",fg="black").place(x=150,y=130)
        txt__amt=Entry(chequeentryframe,textvariable=self.var_amt,font=("Times new roman",13),state='readonly',bg="white",fg="black").place(x=150,y=160)
        cmb_select=ttk.Combobox(chequeentryframe,textvariable=self.var_states,values=("NON-Selected","Need Payment","Payment Done"),font=("Times new roman",12),state='readonly',justify=CENTER)
        cmb_select.place(x=110,y=220)
        cmb_select.current(0)
        cmb_select2=ttk.Combobox(chequeentryframe,textvariable=self.var_pmethod,values=("None","Cash","Cheque"),font=("Times new roman",12),state='readonly',justify=CENTER)
        cmb_select2.place(x=100,y=310)
        cmb_select2.current(0)
        txt_cpment=Entry(chequeentryframe,textvariable=self.var_cpdate,font=("Times new roman",13),bg="white",fg="black").place(x=150,y=350)

        btn_update=Button(chequeentryframe,command=self.update,text="Update",font=("Times new roman",15),fg="black",bg="yellow").place(x=40,y=400,width=70)
        btn_delete=Button(chequeentryframe,text="Delete",command=self.delete,font=("Times new roman",15),fg="black",bg="red").place(x=130,y=400,width=70)
        btn_clear=Button(chequeentryframe,text="Clear",command=self.clear,font=("Times new roman",15),fg="black",bg="gray").place(x=220,y=400,width=70)
        btn_clear=Button(chequeentryframe,text="GO TO CHEQUE BOOK",command=self.chequebook,font=("Times new roman",15),fg="black",bg="light Green").place(x=40,y=450,width=250,height=70)
        self.showblog()
        #Functions

    def billSearch(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.searchstate_che.get()=="ALL" and self.searchby_che.get()=="Select" and self.searchtxt_che.get()=="":
                cur.execute("Select * from balance")
                rows=cur.fetchall()
            elif self.searchby_che.get()=="Select" and self.searchtxt_che.get()=="": 
                cur.execute("Select * from balance where states LIKE '%"+self.searchstate_che.get()+"%'")
                rows=cur.fetchall()
            else:
                #cur.execute("SELECT * from employee where eid LIKE '%"+self.var_search_txt.get()+"%'")
                if self.searchstate_che.get()=="ALL":
                    cur.execute("Select * from balance where "+self.searchby_che.get()+" LIKE '%"+self.searchtxt_che.get()+"%'")
                    rows=cur.fetchall()
                else:
                    cur.execute("Select * from balance where "+self.searchby_che.get()+" LIKE '%"+self.searchtxt_che.get()+"%' and states LIKE '%"+self.searchstate_che.get()+"%'")
                    rows=cur.fetchall()
            if len(rows)!=0:
                self.chequetable.delete(*self.chequetable.get_children())
                for row in rows:
                    self.chequetable.insert('',END,values=row)
            else :
                    messagebox.showerror("Error","No Record Found!!",parent=self.root)
        except Exception as ex :
            messagebox.showerror("Error",f"Error Due to : {str(ex)}",parent=self.root)

    def showblog(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("Select * from balance")
            rows=cur.fetchall()
            self.chequetable.delete(*self.chequetable.get_children())
            for row in rows:
                self.chequetable.insert('',END,values=row)
        except Exception as ex :
            messagebox.showerror("Error",f"Error Due to : {str(ex)}",parent=self.root)

    def showblogall(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("Select * from balance")
            rows=cur.fetchall()
            self.chequetable.delete(*self.chequetable.get_children())
            for row in rows:
                self.chequetable.insert('',END,values=row)
            self.searchby_che.set("Select")
            self.searchtxt_che.set("")
            self.searchstate_che.set("ALL")
        except Exception as ex :
            messagebox.showerror("Error",f"Error Due to : {str(ex)}",parent=self.root)

    def balance_get_data(self,ev):
        f=self.chequetable.focus()
        content=(self.chequetable.item(f))
        row=content['values']
        self.var_bid.set(int(row[0])),
        self.var_cusid.set(row[1]),
        self.var_cusname.set(row[2]),
        self.var_date.set(row[3]),
        self.var_invoice.set(row[4]),
        self.var_amt.set(row[5]),
        self.var_states.set(row[6]),
        self.var_pmethod.set(row[7]),
        self.var_cpdate.set(row[8]), 
    
    def update(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_bid.get()=="":
                messagebox.showerror("Error","Please Customer and Invoice Num From List ID MUST BE required",parent=self.root)
            else :
                cur.execute("Select * from balance where bid=?",(self.var_bid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Cheque ID , Try Differnt",parent=self.root)
                else : #bid,cusid,cusname,date,invoicenum,amount,states,pmethod,cpdate
                    cur.execute("Update balance set states=?,pmethod=?,cpdate=? where bid=?",(

                    self.var_states.get(),
                    self.var_pmethod.get(),
                    self.var_cpdate.get(),
                    self.var_bid.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Succuses","Cheque Update Succusefully",parent=self.root)
                    self.showblog()
        except Exception as ex:
            messagebox.showerror("Error",f"Error Due to :{str(ex)}",parent=self.root)

    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_bid.get()=="":
                messagebox.showerror("Error","Select Cheque MUST BE required",parent=self.root)
            else :
                cur.execute("Select * from balance where bid=?",(self.var_bid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Balance ID , Try Differnt",parent=self.root)
                else : 
                    op=messagebox.askyesno("Conform","Do You really want to Delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from balance where bid=?",(self.var_bid.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","cheque Delete Succusefully",parent=self.root)
                        self.showblog()
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error Due to :{str(ex)}",parent=self.root)

    def clear(self):
        self.var_bid.set(""),
        self.var_cusid.set(""),
        self.var_cusname.set(""),
        self.var_date.set(""),
        self.var_invoice.set(""),
        self.var_amt.set(""),
        self.var_states.set("NON-Selected"),
        self.var_pmethod.set("None"),
        self.var_cpdate.set(""), 

    def todaybill(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            date_=time.strftime("%d-%m-%Y")
            today=str(date_)
            cur.execute("Select * from balance where date LIKE '%"+today+"%'")
            rows=cur.fetchall()
            if len(rows)!=0:
                self.chequetable.delete(*self.chequetable.get_children())
                for row in rows:
                    self.chequetable.insert('',END,values=row)
            else :
                    messagebox.showerror("Error","No Record Found!!",parent=self.root)
        except Exception as ex :
            messagebox.showerror("Error",f"Error Due to : {str(ex)}",parent=self.root)

    def chequebook(self):
            self.new_win=Toplevel(self.root)
            self.new_obj=cheque(self.new_win)




if __name__=="__main__":
    root=Tk()
    obj=balance(root)
    root.mainloop()