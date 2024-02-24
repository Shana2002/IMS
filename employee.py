from tkinter import *
from tkinter import ttk,messagebox
import sqlite3
from PIL import Image,ImageTk
from createdb import create_db
from empsearch import empsearch

class employeeClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1000x500+220+130")
        self,root.config(bg="white")
        self.root.title("Inventory Management system  >> Developed By Hanska Ravishan")
        self.root.focus_force()

        #========All Veriable =====

        self.var_searchby=StringVar()
        self.var_search_txt=StringVar()



        self.var_emp_id=StringVar()
        self.var_emp_name=StringVar()
        self.var_emp_contact=StringVar()
        self.var_emp_dob=StringVar()
        self.var_emp_doj=StringVar()
        self.var_emp_salary=StringVar()




        #=====search Frame=========
        SearchFrame=LabelFrame(self.root,text="Search Employee ", bg="white",relief=RIDGE)
        SearchFrame.place(x=250 ,y= 20 , width=600 ,height=70)


        #=========Option=======
        btn_search=Button(SearchFrame,text="Search",command=self.searchframe,font=("goudy old style",15),cursor="hand2",bg="green",fg="white").place(x=410 , y=10,height=30)


        #========title=====
        title=Label(self.root,text="Employee Details",font=("goudy old style",15),bg="#010c48",fg="white").place(x=50 , y=100,width=1000)

        #========Content===

        lbl_empname=Label(self.root,text="Employee Name",font=("goudy old style",15),bg="white").place(x=50 , y=200)
        lbl_empcontact=Label(self.root,text="Contact",font=("goudy old style",15),bg="white").place(x=50 , y=250)

        txt_empname=Entry(self.root,textvariable=self.var_emp_name,font=("goudy old style",15),bg="light yellow").place(x=300 , y=200)
        txt_empcontact=Entry(self.root,textvariable=self.var_emp_contact,font=("goudy old style",15),bg="light yellow").place(x=300 , y=250)
        #=========Button=====
        btn_add=Button(self.root,text="Save",command=self.add,font=("goudy old style",15),cursor="hand2",bg="green",fg="white").place(x=380 , y=300,height=30)
        btn_Update=Button(self.root,text="Update",command=self.update,font=("goudy old style",15),cursor="hand2",bg="Yellow",fg="Black").place(x=470 , y=300,height=30)
        btn_Delete=Button(self.root,text="Delete",command=self.delete,font=("goudy old style",15),cursor="hand2",bg="Red",fg="white").place(x=580 , y=300,height=30)
        btn_Clear=Button(self.root,text="Clear",command=self.clear,font=("goudy old style",15),cursor="hand2",bg="Black",fg="white").place(x=690 , y=300,height=30)


        #====Employee Details==

        emp_frame=Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=0,y=350 , relwidth=1,height=150)


        scoily=Scrollbar(emp_frame,orient=VERTICAL)
        scoilx=Scrollbar(emp_frame,orient=HORIZONTAL)

        self.Employeetable=ttk.Treeview(emp_frame,columns=("fname","lname"),yscrollcommand=scoily.set)
        scoily.pack(side=RIGHT,fill=Y)
        scoily.config(command=self.Employeetable.yview)
        self.Employeetable.heading("fname",text="EMP ID")
        self.Employeetable.heading("lname",text="Name")


        self.Employeetable["show"]="headings"

        self.Employeetable.column("fname",width=60)
        self.Employeetable.column("lname",width=140)

        

        self.Employeetable.pack(fill=BOTH,expand=1)
        self.Employeetable.bind("<ButtonRelease-1>",self.get_data)
        self.show()





#====================================
    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error","Employee ID MUST BE required",parent=self.root)
            else :
                cur.execute("Select * from employee where fname=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This Employee ID Already Asigned , Try Differnt",parent=self.root)
                else : 
                    cur.execute("Insert into employee (fname,name,contact,dob,doj,salary) values (?,?,?,?,?,?)",(
                        self.var_emp_id.get(),
                        self.var_emp_name.get(),
                        self.var_emp_contact.get(),
                        self.var_emp_dob.get(),
                        self.var_emp_doj.get(),
                        self.var_emp_salary.get(),

                    ))
                    con.commit()
                    messagebox.showinfo("Succuses","Employee Added Succusefully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error Due to :{str(ex)}",parent=self.root)
        
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

    
    def get_data(self,ev):
        f=self.Employeetable.focus()
        content=(self.Employeetable.item(f))
        row=content['values']
        self.var_emp_id.set(row[0]),
        self.var_emp_name.set(row[1]),
        self.var_emp_contact.set(row[2]),
        self.var_emp_dob.set(row[3]),
        self.var_emp_doj.set(row[4]),
        self.var_emp_salary.set(row[5])



    def update(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error","Employee ID MUST BE required",parent=self.root)
            else :
                cur.execute("Select * from employee where fname=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Employee ID , Try Differnt",parent=self.root)
                else : 
                    cur.execute("Update employee set name=?,contact=?,dob=?,doj=?,salary=? where fname=?",(

                        self.var_emp_name.get(),
                        self.var_emp_contact.get(),
                        self.var_emp_dob.get(),
                        self.var_emp_doj.get(),
                        self.var_emp_salary.get(),
                        self.var_emp_id.get(),

                    ))
                    con.commit()
                    messagebox.showinfo("Succuses","Employee Update Succusefully",parent=self.root)
                    self.show()
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error Due to :{str(ex)}",parent=self.root)


    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error","Employee ID MUST BE required",parent=self.root)
            else :
                cur.execute("Select * from employee where fname=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Employee ID , Try Differnt",parent=self.root)
                else : 
                    op=messagebox.askyesno("Conform","Do You really want to Delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from employee where fname=?",(self.var_emp_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Employee Delete Succusefully",parent=self.root)
                        self.show()
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error Due to :{str(ex)}",parent=self.root)

    def clear(self):
        self.var_emp_id.set(""),
        self.var_emp_name.set(""),
        self.var_emp_contact.set(""),
        self.var_emp_dob.set(""),
        self.var_emp_doj.set(""),
        self.var_emp_salary.set("")


    def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_searchby.get()=="Select":
                messagebox.showerror("Error","Select Search by option",parent=self.root)
            elif self.var_search_txt.get()=="":
                messagebox.showerror("Error","Search Input should be required",parent=self.root)
            else:
                cur.execute("Select * from employee where "+self.var_searchby.get()+" LIKE '%"+self.var_search_txt.get()+"%'")
                rows=cur.fetchall()
                if len(row)!=0:
                    self.Employeetable.delete(*self.Employeetable.get_children())
                for row in rows:
                    self.Employeetable.insert('',END,values=row)
                else :
                    messagebox.showerror("Error","No Record Found!!",parent=self.root)
        except Exception as ex :
            messagebox.showerror("Error",f"Error Due to : {str(ex)}",parent=self.root)
        
    def searchframe(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=empsearch(self.new_win)

if __name__=="__main__":
    root=Tk()
    obj=employeeClass(root)
    root.mainloop()       