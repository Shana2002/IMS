from tkinter import *
from tkinter import ttk,messagebox
import sqlite3


class customerClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1000x650+220+130")
        self,root.config(bg="white")
        self.root.title("Inventory Management system  >> Developed By Hanska Ravishan")
        self.root.focus_force()

        #========All Veriable =====

        self.var_searchby=StringVar()
        self.var_search_txt=StringVar()



        self.var_cus_id=StringVar()
        self.var_cus_name=StringVar()
        self.var_cus_contact=StringVar()
        self.var_cus_balance=StringVar()
        self.var_cus_chebalance=StringVar()




        #=====search Frame=========
        SearchFrame=LabelFrame(self.root,text="Search customer ", bg="white",relief=RIDGE)
        SearchFrame.place(x=250 ,y= 20 , width=650 ,height=70)


        #=========Option=======
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("Select","cusid","cusname","cuscontactt"),state='readonly',justify=CENTER)
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        txt_search=Entry(SearchFrame,textvariable=self.var_search_txt,font=("goudy old style",15),bg="lightyellow").place(x=200,y=10)
        btn_search=Button(SearchFrame,command=self.search,text="Search",font=("goudy old style",15),cursor="hand2",bg="green",fg="white").place(x=410 , y=10,height=30)
        btn_showall=Button(SearchFrame,command=self.show,text="Show All",font=("goudy old style",15),cursor="hand2",bg="green",fg="white").place(x=510 , y=10,height=30)

        emp_frame=Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=0,y=100 , relwidth=1,height=300)


        #========title=====
        title=Label(self.root,text="customer Details",font=("goudy old style",15),bg="#010c48",fg="white").place(x=50 , y=100,width=1000)

        #========Content===

        lbl_cusID=Label(self.root,text="customer ID",font=("goudy old style",15),bg="white").place(x=50 , y=150)
        lbl_cusname=Label(self.root,text="customer Name",font=("goudy old style",15),bg="white").place(x=50 , y=200)
        lbl_cuscontact=Label(self.root,text="Contact",font=("goudy old style",15),bg="white").place(x=50 , y=250)
        lbl_balance=Label(self.root,text="Balance",font=("goudy old style",15),bg="white").place(x=600 , y=150)

        txt_cusid=Entry(self.root, textvariable=self.var_cus_id ,font=("goudy old style",15),bg="light yellow").place(x=300 , y=150)
        txt_cusname=Entry(self.root,textvariable=self.var_cus_name,font=("goudy old style",15),bg="light yellow").place(x=300 , y=200)
        txt_cuscontact=Entry(self.root,textvariable=self.var_cus_contact,font=("goudy old style",15),bg="light yellow").place(x=300 , y=250)
        txt_cusbalance=Entry(self.root,textvariable=self.var_cus_balance,font=("goudy old style",15),bg="light yellow").place(x=700, y=150)

        #=========Button=====
        btn_add=Button(self.root,text="Save",command=self.add,font=("goudy old style",15),cursor="hand2",bg="green",fg="white").place(x=380 , y=300,height=30)
        btn_Update=Button(self.root,text="Update",command=self.update,font=("goudy old style",15),cursor="hand2",bg="Yellow",fg="Black").place(x=470 , y=300,height=30)
        btn_Delete=Button(self.root,text="Delete",command=self.delete,font=("goudy old style",15),cursor="hand2",bg="Red",fg="white").place(x=580 , y=300,height=30)
        btn_Clear=Button(self.root,text="Clear",command=self.clear,font=("goudy old style",15),cursor="hand2",bg="Black",fg="white").place(x=690 , y=300,height=30)


        #====customer Details==

        cus_frame=Frame(self.root,bd=3,relief=RIDGE)
        cus_frame.place(x=0,y=350 , relwidth=1,height=300)


        scoily=Scrollbar(cus_frame,orient=VERTICAL)
        scoilx=Scrollbar(cus_frame,orient=HORIZONTAL)

        self.customertable=ttk.Treeview(cus_frame,columns=("cusid","cusname","cuscontact","balance","chebalane"),yscrollcommand=scoily.set)
        scoily.pack(side=RIGHT,fill=Y)
        scoily.config(command=self.customertable.yview)
        self.customertable.heading("cusid",text="cus ID")
        self.customertable.heading("cusname",text="Name")
        self.customertable.heading("cuscontact",text="Conatct Number")
        self.customertable.heading("balance",text="Balance")
        self.customertable.heading("chebalane",text="nop Cheques")

        self.customertable["show"]="headings"

        self.customertable.column("cusid",width=60,anchor=CENTER)
        self.customertable.column("cusname",width=140,anchor=CENTER)
        self.customertable.column("cuscontact",width=100,anchor=CENTER)
        self.customertable.column("balance",width=100,anchor=CENTER)
        self.customertable.column("chebalane",width=100,anchor=CENTER)
        

        self.customertable.pack(fill=BOTH,expand=1)
        self.customertable.bind("<ButtonRelease-1>",self.get_data)
        self.show()





#====================================
    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_cus_id.get()=="":
                messagebox.showerror("Error","customer ID MUST BE required",parent=self.root)
            else :
                cur.execute("Select * from customer where cusid=?",(self.var_cus_id.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This customer ID Already Asigned , Try Differnt",parent=self.root)
                else : 
                    cur.execute("Insert into customer (cusid,cusname,cuscontact,balance) values (?,?,?,?)",(
                        self.var_cus_id.get(),
                        self.var_cus_name.get(),
                        self.var_cus_contact.get(),
                        self.var_cus_balance.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Succuses","customer Added Succusefully",parent=self.root)
                    self.show()
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error Due to :{str(ex)}",parent=self.root)
        
    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("Select * from customer")
            rows=cur.fetchall()
            self.customertable.delete(*self.customertable.get_children())
            for row in rows:
                self.customertable.insert('',END,values=row)
        except Exception as ex :
            messagebox.showerror("Error",f"Error Due to : {str(ex)}",parent=self.root)

    
    def get_data(self,ev):
        f=self.customertable.focus()
        content=(self.customertable.item(f))
        row=content['values']
        self.var_cus_id.set(row[0]),
        self.var_cus_name.set(row[1]),
        self.var_cus_contact.set(row[2]),
        self.var_cus_balance.set(row[3]),



    def update(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_cus_id.get()=="":
                messagebox.showerror("Error","customer ID MUST BE required",parent=self.root)
            else :
                cur.execute("Select * from customer where cusid=?",(self.var_cus_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid customer ID , Try Differnt",parent=self.root)
                else : 
                    cur.execute("Update customer set cusname=?,cuscontact=?,balance=? where cusid=?",(
                        self.var_cus_name.get(),
                        self.var_cus_contact.get(),
                        self.var_cus_balance.get(),
                        self.var_cus_id.get(),

                    ))
                    con.commit()
                    messagebox.showinfo("Succuses","customer Update Succusefully",parent=self.root)
                    self.show()
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error Due to :{str(ex)}",parent=self.root)


    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_cus_id.get()=="":
                messagebox.showerror("Error","customer ID MUST BE required",parent=self.root)
            else :
                cur.execute("Select * from customer where cusid=?",(self.var_cus_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid customer ID , Try Differnt",parent=self.root)
                else : 
                    op=messagebox.askyesno("Conform","Do You really want to Delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from customer where cusid=?",(self.var_cus_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","customer Delete Succusefully",parent=self.root)
                        self.show()
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error Due to :{str(ex)}",parent=self.root)

    def clear(self):
        self.var_cus_id.set(""),
        self.var_cus_name.set(""),
        self.var_cus_contact.set(""),
        self.var_cus_balance.set(""),


    def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_searchby.get()=="Select":
                messagebox.showerror("Error","Select Search by option",parent=self.root)
            elif self.var_search_txt.get()=="":
                messagebox.showerror("Error","Search Input should be required",parent=self.root)
            else:
            #cur.execute("SELECT * from employee where cusid LIKE '%"+self.var_search_txt.get()+"%'")
                cur.execute("Select * from customer where "+self.var_searchby.get()+" LIKE '%"+self.var_search_txt.get()+"%'")
                rows=cur.fetchall()
            if len(rows)!=0:
                self.customertable.delete(*self.customertable.get_children())
                for row in rows:
                    self.customertable.insert('',END,values=row)
            else :
                    messagebox.showerror("Error","No Record Found!!",parent=self.root)
        except Exception as ex :
            messagebox.showerror("Error",f"Error Due to : {str(ex)}",parent=self.root)

if __name__=="__main__":
    root=Tk()
    obj=customerClass(root)
    root.mainloop()       