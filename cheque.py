from tkinter import *
from tkinter import ttk,messagebox
import sqlite3

class cheque:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x700+220+130")
        self,root.config(bg="white")
        self.root.title("Inventory Management system  >> Developed By Hanska Ravishan")
        self.root.focus_force()

        title=Label(self.root,text="Cheque Log", font=("arial",40,"bold"),bg="#010c48",fg="white",anchor="w", padx=350).place(x=0,y=0,relwidth=1,height=70)

        self.var_searchby=StringVar()
        self.var_search_txt=StringVar()

        self.var_cus_searchby=StringVar()
        self.var_cus_searchtext=StringVar()

        self.cus_id=StringVar()
        self.cus_name=StringVar()
        self.var_states=StringVar()
        self.var_chenum=StringVar()
        self.var_chedate=StringVar()
        self.var_amt=StringVar()
        self.var_bank=StringVar()
        self.var_id=StringVar()



        cusFrame1=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        cusFrame1.place(x=6,y=100,width=450,height=300)

        cmb_searchcus=ttk.Combobox(cusFrame1,textvariable=self.var_cus_searchby,values=("Select","cusid","cusname","cuscontact"),state='readonly',justify=CENTER)
        cmb_searchcus.place(x=10,y=10,width=60,height=20)
        cmb_searchcus.current(0)

        txt_search=Entry(cusFrame1,textvariable=self.var_cus_searchtext,font=("goudy old style",10),bg="lightyellow").place(x=80,y=10 , width=100 , height=20)
        btn_search=Button(cusFrame1,command=self.cus_search,text="Search",font=("goudy old style",15),cursor="hand2",bg="green",fg="white").place(x=190 , y=10,height=20)
        btn_showall=Button(cusFrame1,text="Show All",font=("goudy old style",15),cursor="hand2",bg="green",fg="white").place(x=290 , y=10,height=20)
        btn_addcus=Button(cusFrame1,text="+",font=("goudy old style",15),cursor="hand2",bg="green",fg="white").place(x=400, y=10,height=20)

        cusFrame3=Frame(cusFrame1,bd=2,relief=RIDGE,bg="light yellow")
        cusFrame3.place(x=2,y=40,width=450,height=260)

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

        

        chequeentryframe=Frame(self.root,bd=3,relief=RIDGE,bg="Light yellow")
        chequeentryframe.place(x=470,y=100,width=550,height=300)

        lbl_ID=Label(chequeentryframe,       text="Customer ID  ",font=("Times new roman",15),bg="Light yellow",fg="black").place(x=10,y=10)
        lbl_name=Label(chequeentryframe,     text="Customer Name ",font=("Times new roman",15),bg="Light yellow",fg="black").place(x=10,y=40)
        lbl_chueqnum=Label(chequeentryframe, text="Cheque Number ",font=("Times new roman",15),bg="Light yellow",fg="black").place(x=10,y=100)
        lbl_chquedate=Label(chequeentryframe,text="Cheque date  ",font=("Times new roman",15),bg="Light yellow",fg="black").place(x=10,y=130)
        lbl__amt=Label(chequeentryframe,     text="Amount ",font=("Times new roman",15),bg="Light yellow",fg="black").place(x=10,y=160)
        lbl_chquebank=Label(chequeentryframe,text="Bank",font=("Times new roman",15),bg="Light yellow",fg="black").place(x=10,y=190)
        lbl_states=Label(chequeentryframe,text="States",font=("Times new roman",15),bg="Light yellow",fg="black").place(x=420,y=130)

        txt_ID=Entry(chequeentryframe,textvariable=self.cus_id,font=("Times new roman",11),state='readonly',bg="white",fg="black").place(x=200,y=10)
        txt_name=Entry(chequeentryframe,textvariable=self.cus_name,font=("Times new roman",11),state='readonly',bg="white",fg="black").place(x=200,y=40)
        txt_chueqnum=Entry(chequeentryframe,textvariable=self.var_chenum,font=("Times new roman",11),bg="white",fg="black").place(x=200,y=100,width=250)
        txt_chquedate=Entry(chequeentryframe,textvariable=self.var_chedate,font=("Times new roman",11),bg="white",fg="black").place(x=200,y=130)
        txt__amt=Entry(chequeentryframe,textvariable=self.var_amt,font=("Times new roman",11),bg="white",fg="black").place(x=200,y=160)
        txt_chquebank=Entry(chequeentryframe,textvariable=self.var_bank,font=("Times new roman",11),bg="white",fg="black").place(x=200,y=190)
        cmb_select=ttk.Combobox(chequeentryframe,textvariable=self.var_states,values=("Active","Collected","Returned"),font=("Times new roman",12),state='readonly',justify=CENTER)
        cmb_select.place(x=360,y=160)
        cmb_select.current(0)

        btn_save=Button(chequeentryframe,text="Save",command=self.add,font=("Times new roman",15),fg="black",bg="light green").place(x=100,y=240,width=70)
        btn_update=Button(chequeentryframe,text="Update",command=self.update,font=("Times new roman",15),fg="black",bg="yellow").place(x=180,y=240,width=70)
        btn_delete=Button(chequeentryframe,text="Delete",command=self.delete,font=("Times new roman",15),fg="black",bg="red").place(x=260,y=240,width=70)
        btn_clear=Button(chequeentryframe,text="Clear",command=self.clear,font=("Times new roman",15),fg="black",bg="gray").place(x=340,y=240,width=70)
    
         #=====search Frame=========

        self.searchby_che=StringVar()
        self.searchtxt_che=StringVar()
        self.searchstate_che=StringVar()

        SearchFrame1=LabelFrame(self.root,text="Search ", bg="white",relief=RIDGE)
        SearchFrame1.place(x=180 ,y= 420 , width=900 ,height=70)


        #=========Option=======
        cmb_searchstate=ttk.Combobox(SearchFrame1,textvariable=self.searchstate_che,values=("ALL","Active","Collected","Returned"),state='readonly',justify=CENTER)
        cmb_searchstate.place(x=10,y=14,width=160)
        cmb_searchstate.current(0)

        cmb_search=ttk.Combobox(SearchFrame1,textvariable=self.searchby_che,values=("Select","cusid","cusname","chequenum","chequedate","chequebank"),state='readonly',justify=CENTER)
        cmb_search.place(x=180,y=14,width=160)
        cmb_search.current(0)

        txt_search=Entry(SearchFrame1,textvariable=self.searchtxt_che,font=("goudy old style",15),bg="lightyellow").place(x=350,y=10,width=300)
        btn_search=Button(SearchFrame1,command=self.chequesearch,text="Search",font=("goudy old style",15),cursor="hand2",bg="green",fg="white").place(x=700 , y=10,height=30)
        btn_showall=Button(SearchFrame1,command=self.showcheque,text="Show All",font=("goudy old style",15),cursor="hand2",bg="green",fg="white").place(x=800 , y=10,height=30)

        cheqt=Frame(self.root,bd=2,relief=RIDGE,bg="light yellow")
        cheqt.place(x=2,y=500,width=1100,height=260)

        scoily=Scrollbar(cheqt,orient=VERTICAL)
        scoilx=Scrollbar(cheqt,orient=HORIZONTAL)

        self.chequetable=ttk.Treeview(cheqt,columns=("chequeid","cusid","cusname","states","chequenum","chequedate","chequeamt","chequebank"),yscrollcommand=scoily.set)
        scoily.pack(side=RIGHT,fill=Y)
        scoily.config(command=self.chequetable.yview)
        self.chequetable.heading("chequeid",text="ID")
        self.chequetable.heading("cusid",text="Customer ID")
        self.chequetable.heading("cusname",text="Customer Name")
        self.chequetable.heading("states",text="Cheque State")
        self.chequetable.heading("chequenum",text="Cheque Number")
        self.chequetable.heading("chequedate",text="Cheque Date")
        self.chequetable.heading("chequeamt",text="Amount")
        self.chequetable.heading("chequebank",text="Bank")
#"chequeid","cusid","cusname","states","chequenum","chequedate","chequeamt","chequebank"

        self.chequetable["show"]="headings"

        self.chequetable.column("chequeid",width=20)
        self.chequetable.column("cusid",width=20)
        self.chequetable.column("cusname",width=140)
        self.chequetable.column("states",width=60)
        self.chequetable.column("chequenum",width=100)
        self.chequetable.column("chequedate",width=60)
        self.chequetable.column("chequeamt",width=60)
        self.chequetable.column("chequebank",width=40)

        self.chequetable.pack(fill=BOTH,expand=1)
        self.chequetable.bind("<ButtonRelease-1>",self.cheque_get_data)
        self.showcheque()
        

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

    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.cus_id==""   :
                messagebox.showerror("Error","Please Select Customer",parent=self.root)
            elif self.var_chedate=="" or self.var_amt=="":
                messagebox.showerror("Error","Please Enter Cheque Date And Amount",parent=self.root)
            else :#"chequeid","cusid","cusname","states","chequenum","chequedate","chequeamt","chequebank"
                cur.execute("Select * from cheque where chequeid=?",(self.var_id.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This Cheque Already Assign , Try Differnt",parent=self.root)
                else : 
                    cur.execute("Insert into cheque (cusid,cusname,states,chequenum,chequedate,chequeamt,chequebank) values (?,?,?,?,?,?,?)",(

                    self.cus_id.get(),
                    self.cus_name.get(),
                    self.var_states.get(),
                    self.var_chenum.get(),
                    self.var_chedate.get(),
                    self.var_amt.get(),
                    self.var_bank.get(),
                    
                    ))
                    con.commit()
                    cur.execute("Select * from cheque where cusid LIKE '%"+self.cus_id.get()+"%'")
                    rows=cur.fetchall()
                    no=len(rows)
                    

                    con.commit()
                    cur.execute("Update customer set chebalance=? where cusid=?",(
                        no,
                        self.cus_id.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Succuses","cheque Added Succusefully",parent=self.root)
                    
                    self.showcheque()
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error Due to :{str(ex)}",parent=self.root)

    def update(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_id.get()=="":
                messagebox.showerror("Error","Please Cheque From List ID MUST BE required",parent=self.root)
            else :
                cur.execute("Select * from cheque where chequeid=?",(self.var_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Cheque ID , Try Differnt",parent=self.root)
                else : 
                    cur.execute("Update cheque set cusid=?,cusname=?,states=?,chequenum=?,chequedate=?,chequeamt=?,chequebank=? where chequeid=?",(

                    self.cus_id.get(),
                    self.cus_name.get(),
                    self.var_states.get(),
                    self.var_chenum.get(),
                    self.var_chedate.get(),
                    self.var_amt.get(),
                    self.var_bank.get(),
                    self.var_id.get(), 
                        

                    ))
                    con.commit()
                    messagebox.showinfo("Succuses","Cheque Update Succusefully",parent=self.root)
                    self.showcheque()
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error Due to :{str(ex)}",parent=self.root)

    def chequesearch(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.searchstate_che.get()=="ALL" and self.searchby_che.get()=="Select" and self.searchtxt_che.get()=="":
                cur.execute("Select * from cheque")
                rows=cur.fetchall()
            elif self.searchby_che.get()=="Select" and self.searchtxt_che.get()=="": 
                cur.execute("Select * from cheque where states LIKE '%"+self.searchstate_che.get()+"%'")
                rows=cur.fetchall()
            else:
                #cur.execute("SELECT * from employee where eid LIKE '%"+self.var_search_txt.get()+"%'")
                if self.searchstate_che.get()=="ALL":
                    cur.execute("Select * from cheque where "+self.searchby_che.get()+" LIKE '%"+self.searchtxt_che.get()+"%'")
                    rows=cur.fetchall()
                else:
                    cur.execute("Select * from cheque where "+self.searchby_che.get()+" LIKE '%"+self.searchtxt_che.get()+"%' and states LIKE '%"+self.searchstate_che.get()+"%'")
                    rows=cur.fetchall()
            if len(rows)!=0:
                self.chequetable.delete(*self.chequetable.get_children())
                for row in rows:
                    self.chequetable.insert('',END,values=row)
            else :
                    messagebox.showerror("Error","No Record Found!!",parent=self.root)
        except Exception as ex :
            messagebox.showerror("Error",f"Error Due to : {str(ex)}",parent=self.root)


    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_id.get()=="":
                messagebox.showerror("Error","Select Cheque MUST BE required",parent=self.root)
            else :
                cur.execute("Select * from cheque where chequeid=?",(self.var_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Cheque ID , Try Differnt",parent=self.root)
                else : 
                    op=messagebox.askyesno("Conform","Do You really want to Delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from cheque where chequeid=?",(self.var_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","cheque Delete Succusefully",parent=self.root)
                        self.showcheque()
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error Due to :{str(ex)}",parent=self.root)
        
    def showcheque(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("Select * from cheque")
            rows=cur.fetchall()
            self.chequetable.delete(*self.chequetable.get_children())
            for row in rows:
                self.chequetable.insert('',END,values=row)
            self.searchby_che.set("Select")
            self.searchstate_che.set("ALL")
            self.searchtxt_che.set("")
        except Exception as ex :
            messagebox.showerror("Error",f"Error Due to : {str(ex)}",parent=self.root)
    
    def clear(self):
            self.cus_id.set(""),
            self.cus_name.set(""),
            self.var_states.set("Active"),
            self.var_chenum.set(""),
            self.var_chedate.set(""),
            self.var_amt.set(""),
            self.var_bank.set(""),
    
    def cus_get_data(self,ev):
        f=self.custable.focus()
        content=(self.custable.item(f))
        row=content['values']
        self.cus_id.set(int(row[0]))
        self.cus_name.set(row[1])

    def cheque_get_data(self,ev):
        f=self.chequetable.focus()
        content=(self.chequetable.item(f))
        row=content['values']
        self.var_id.set(int(row[0]))
        self.cus_id.set(int(row[1]))
        self.cus_name.set(row[2])
        self.var_states.set(row[3]),
        self.var_chenum.set(row[4]),
        self.var_chedate.set(row[5]),
        self.var_amt.set(row[6]),
        self.var_bank.set(row[7])
        
        


if __name__=="__main__":
    root=Tk()
    obj=cheque(root)
    root.mainloop()