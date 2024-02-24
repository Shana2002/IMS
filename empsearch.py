from tkinter import *
from tkinter import ttk,messagebox
import sqlite3

class empsearch:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self,root.config(bg="white")
        self.root.title("Inventory Management system  >> Developed By Hanska Ravishan")
        self.root.focus_force()

    
        self.var_searchby=StringVar()
        self.var_search_txt=StringVar()

        #=====search Frame=========
        SearchFrame1=LabelFrame(self.root,text="Search Employee ", bg="white",relief=RIDGE)
        SearchFrame1.place(x=250 ,y= 20 , width=600 ,height=70)


        #=========Option=======
        cmb_search=ttk.Combobox(SearchFrame1,textvariable=self.var_searchby,values=("Select","eid","Name","Contact"),state='readonly',justify=CENTER)
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        txt_search=Entry(SearchFrame1,textvariable=self.var_search_txt,font=("goudy old style",15),bg="lightyellow").place(x=200,y=10)
        btn_search=Button(SearchFrame1,command=self.search,text="Search",font=("goudy old style",15),cursor="hand2",bg="green",fg="white").place(x=410 , y=10,height=30)
        btn_showall=Button(SearchFrame1,command=self.show,text="Show All",font=("goudy old style",15),cursor="hand2",bg="green",fg="white").place(x=480 , y=10,height=30)

        emp_frame=Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=0,y=100 , relwidth=1,height=300)


        scoily=Scrollbar(emp_frame,orient=VERTICAL)
        scoilx=Scrollbar(emp_frame,orient=HORIZONTAL)

        self.Employeetable=ttk.Treeview(emp_frame,columns=("eid","name","contact","dob","doj","salary"),yscrollcommand=scoily.set)
        scoily.pack(side=RIGHT,fill=Y)
        scoily.config(command=self.Employeetable.yview)
        self.Employeetable.heading("eid",text="EMP ID")
        self.Employeetable.heading("name",text="Name")
        self.Employeetable.heading("contact",text="Conatct Number")
        self.Employeetable.heading("dob",text="Date OF Birth")
        self.Employeetable.heading("doj",text="Date OF Join")
        self.Employeetable.heading("salary",text="Salary")

        self.Employeetable["show"]="headings"

        self.Employeetable.column("eid",width=60)
        self.Employeetable.column("name",width=140)
        self.Employeetable.column("contact",width=100)
        self.Employeetable.column("dob",width=100)
        self.Employeetable.column("doj",width=100)
        self.Employeetable.column("salary",width=100)

        self.Employeetable.pack(fill=BOTH,expand=1)
        
        

       
    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("Select * from employee")
            rows=cur.fetchall()
            self.Employeetable.delete(*self.Employeetable.get_children())
            for row in rows:
                self.Employeetable.insert('',END,values=row)
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
                cur.execute("Select * from employee where "+self.var_searchby.get()+" LIKE '%"+self.var_search_txt.get()+"%'")
                rows=cur.fetchall()
            if len(rows)!=0:
                self.Employeetable.delete(*self.Employeetable.get_children())
                for row in rows:
                    self.Employeetable.insert('',END,values=row)
            else :
                    messagebox.showerror("Error","No Record Found!!",parent=self.root)
        except Exception as ex :
            messagebox.showerror("Error",f"Error Due to : {str(ex)}",parent=self.root)
        
if __name__=="__main__":
    root=Tk()
    obj=empsearch(root)
    root.mainloop()