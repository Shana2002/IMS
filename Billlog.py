from tkinter import *
from tkinter import ttk,messagebox
import sqlite3

class billlog:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self,root.config(bg="white")
        self.root.title("Inventory Management system  >> Developed By Hanska Ravishan")
        self.root.focus_force()

        self.var_searchby=StringVar()
        self.var_search_txt=StringVar()

        title=Label(self.root,text="Transaction History", font=("arial",40,"bold"),bg="#010c48",fg="white",anchor="w", padx=350).place(x=0,y=0,relwidth=1,height=70)


        cmb_search=ttk.Combobox(self.root,textvariable=self.var_searchby,values=("Select","cusname","china_code","logid","date"),state='readonly',justify=CENTER)
        cmb_search.place(x=10,y=100,width=180,height=40)
        cmb_search.current(0)

        txt_search=Entry(self.root,textvariable=self.var_search_txt,font=("goudy old style",15),bg="lightyellow").place(x=200,y=100 , width=435 , height=40)
        btn_search=Button(self.root,command=self.search,text="Search",font=("goudy old style",15),cursor="hand2",bg="green",fg="white").place(x=650 , y=100,height=40)
        btn_showall=Button(self.root,command=self.show,text="Show All",font=("goudy old style",15),cursor="hand2",bg="green",fg="white").place(x=750 , y=100,height=40)

        log_frame=Frame(self.root,bd=3,relief=RIDGE)
        log_frame.place(x=0,y=160 , relwidth=1,height=300)

        scoily=Scrollbar(log_frame,orient=VERTICAL)
        scoilx=Scrollbar(log_frame,orient=HORIZONTAL)

        self.logtable=ttk.Treeview(log_frame,columns=("blogid","cusid","cusname","date","invoicenum","total"),yscrollcommand=scoily.set)
        scoily.pack(side=RIGHT,fill=Y)
        scoily.config(command=self.logtable.yview)
        self.logtable.heading("blogid",text="Bill log ID",)
        self.logtable.heading("cusid",text="Customer ID")
        self.logtable.heading("cusname",text="Customer Name")
        self.logtable.heading("date",text="date")
        self.logtable.heading("invoicenum",text="Invoice")
        self.logtable.heading("total",text="Total Amount")
        
       

        self.logtable["show"]="headings"

        self.logtable.column("blogid",width=60)
        self.logtable.column("cusid",width=100)
        self.logtable.column("cusname",width=100)
        self.logtable.column("date",width=140)
        self.logtable.column("invoicenum",width=100)
        self.logtable.column("total",width=100)
        self.show()
        

        self.logtable.pack(fill=BOTH,expand=1)
        self.logtable.bind("<ButtonRelease-1>")

    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("Select * from billlog")
            rows=cur.fetchall()
            self.logtable.delete(*self.logtable.get_children())
            for row in rows:
                self.logtable.insert('',END,values=row)
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
                cur.execute("Select * from billlog where "+self.var_searchby.get()+" LIKE '%"+self.var_search_txt.get()+"%'")
                rows=cur.fetchall()
            if len(rows)!=0:
                self.logtable.delete(*self.logtable.get_children())
                for row in rows:
                    self.logtable.insert('',END,values=row)
            else :
                    messagebox.showerror("Error","No Record Found!!",parent=self.root)
        except Exception as ex :
            messagebox.showerror("Error",f"Error Due to : {str(ex)}",parent=self.root)



if __name__=="__main__":
    root=Tk()
    obj=billlog(root)
    root.mainloop()