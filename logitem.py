from tkinter import *
from tkinter import ttk,messagebox
import sqlite3

class logitem:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self,root.config(bg="white")
        self.root.title("Inventory Management system  >> Developed By Hanska Ravishan")
        self.root.focus_force()

        self.var_searchby=StringVar()
        self.var_search_txt=StringVar()

        title=Label(self.root,text="LOG", font=("arial",40,"bold"),bg="#010c48",fg="white",anchor="w", padx=350).place(x=0,y=0,relwidth=1,height=70)


        cmb_search=ttk.Combobox(self.root,textvariable=self.var_searchby,values=("Select","Customer","China Number","LOG ID","Date","type"),state='readonly',justify=CENTER)
        cmb_search.place(x=10,y=100,width=180,height=40)
        cmb_search.current(0)

        txt_search=Entry(self.root,textvariable=self.var_search_txt,font=("goudy old style",15),bg="lightyellow").place(x=200,y=100 , width=435 , height=40)
        btn_search=Button(self.root,command=self.search,text="Search",font=("goudy old style",15),cursor="hand2",bg="green",fg="white").place(x=650 , y=100,height=40)
        btn_showall=Button(self.root,command=self.show,text="Show All",font=("goudy old style",15),cursor="hand2",bg="green",fg="white").place(x=750 , y=100,height=40)

        log_frame=Frame(self.root,bd=3,relief=RIDGE)
        log_frame.place(x=0,y=160 , relwidth=1,height=300)

        scoily=Scrollbar(log_frame,orient=VERTICAL)
        scoilx=Scrollbar(log_frame,orient=HORIZONTAL)

        self.logtable=ttk.Treeview(log_frame,columns=("logid","cusname","china_code","loc","type","qty","unitp","date"),yscrollcommand=scoily.set)
        scoily.pack(side=RIGHT,fill=Y)
        scoily.config(command=self.logtable.yview)
        self.logtable.heading("logid",text="log ID",)
        self.logtable.heading("cusname",text="Customer Name")
        self.logtable.heading("china_code",text="China Code")
        self.logtable.heading("loc",text="Location")
        self.logtable.heading("type",text="TYPE")
        self.logtable.heading("qty",text="QTY.")
        self.logtable.heading("unitp",text="Unit Price")
        self.logtable.heading("date",text="Date")

        self.logtable["show"]="headings"

        self.logtable.column("logid",width=60)
        self.logtable.column("cusname",width=100)
        self.logtable.column("china_code",width=140)
        self.logtable.column("loc",width=100)
        self.logtable.column("type",width=100)
        self.logtable.column("qty",width=100)
        self.logtable.column("unitp",width=100)
        self.logtable.column("date",width=100)
        self.show()
        

        self.logtable.pack(fill=BOTH,expand=1)
        self.logtable.bind("<ButtonRelease-1>")

    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("Select * from logitem")
            rows=cur.fetchall()
            self.logtable.delete(*self.logtable.get_children())
            for row in rows:
                self.logtable.insert('',END,values=row)
        except Exception as ex :
            messagebox.showerror("Error",f"Error Due to : {str(ex)}",parent=self.root)
#"cusname","china_code","logid","date"
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
                if self.var_searchby.get()=="Customer":
                    searchby="cusname"
                if self.var_searchby.get()=="China Number":#
                    searchby="china_code"
                if self.var_searchby.get()=="LOG ID":
                    searchby="logid"
                if self.var_searchby.get()=="Date":
                    searchby="date"  
                if self.var_searchby.get()=="type":
                    searchby="type"    
                cur.execute("Select * from logitem where "+searchby+" LIKE '%"+self.var_search_txt.get()+"%'")
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
    obj=logitem(root)
    root.mainloop()
