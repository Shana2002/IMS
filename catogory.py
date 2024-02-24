from tkinter import *
from tkinter import ttk,messagebox
import sqlite3

class catogoryClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self,root.config(bg="white")
        self.root.title("Inventory Management system  >> Developed By Hanska Ravishan")
        self.root.focus_force()

        #====variable==
        self.var_cat_id=StringVar()
        self.var_name=StringVar()

        #========title

        lbl_Title=Label(self.root,text="Manage Product Catogory",font=("goudy old style",30),bg="#184a45",fg="white").pack(side=TOP,fill=X,padx=10,pady=2)
        lbl_name=Label(self.root,text="Enter Product Catogory   :",font=("goudy old style",20),bg="White").place(x=50,y=100)
        txt_name=Entry(self.root,textvariable=self.var_name,font=("arial",20),bg="light yellow").place(x=350,y=100)

        btn_add=Button(self.root,command=self.add,text="Add",font=("goudy old style",15),bg="Green",cursor="hand2").place(x=700,y=100,width=100,height=30)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("goudy old style",15),bg="Red",cursor="hand2").place(x=810,y=100,width=100,height=30)
        
        #====catogory Details++++++

        cat_frame=Frame(self.root,bd=3,relief=RIDGE)
        cat_frame.place(x=50,y=200,width=380,height=250 )

        scrolly=Scrollbar(cat_frame,orient=VERTICAL)
        scrollx=Scrollbar(cat_frame,orient=HORIZONTAL)

        self.catogory_table=ttk.Treeview(cat_frame,columns=("cid","name"),yscrollcommand=scrolly)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.catogory_table.xview)
        scrolly.config(command=self.catogory_table.yview)

        self.catogory_table.heading("cid",text="C ID")
        self.catogory_table.heading("name",text="Name")
        self.catogory_table["show"]="headings"
        self.catogory_table.column("cid",width=90)
        self.catogory_table.column("name",width=100)
        self.catogory_table.pack(fill=BOTH,expand=1)
        self.catogory_table.bind("<ButtonRelease-1>",self.get_data)
        self.show()


        #fUNCTIONS 
    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_name.get()=="":
                messagebox.showerror("Error","Catogory MUST BE required",parent=self.root)
            else :
                cur.execute("Select * from catogory where name=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Catogory Already Present , Try Differnt",parent=self.root)
                else : 
                    cur.execute("Insert into catogory (name) values (?)",(self.var_name.get(),))
                    con.commit()
                    messagebox.showinfo("Succuses","Catogory Added Succusefully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error Due to :{str(ex)}",parent=self.root)
    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("Select * from catogory")
            rows=cur.fetchall()
            self.catogory_table.delete(*self.catogory_table.get_children())
            for row in rows:
                self.catogory_table.insert('',END,values=row)
        except Exception as ex :
            messagebox.showerror("Error",f"Error Due to : {str(ex)}",parent=self.root)

    def get_data(self,ev):
        f=self.catogory_table.focus()
        content=(self.catogory_table.item(f))
        row=content['values']
        self.var_cat_id.set(row[0])
        self.var_name.set(row[1])
        
    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_cat_id.get()=="":
                messagebox.showerror("Error","Please select catogory from list",parent=self.root)
            else :
                cur.execute("Select * from catogory where cid=?",(self.var_cat_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Plase Try Again , Try Differnt",parent=self.root)
                else : 
                    op=messagebox.askyesno("Conform","Do You really want to Delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from employee where eid=?",(self.var_cat_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Catogory Delete Succusefully",parent=self.root)
                        
                        self.var_cat_id.set("")
                        self.var_name.set("")
                        self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error Due to :{str(ex)}",parent=self.root) 

if __name__=="__main__":
    root=Tk()
    obj=catogoryClass(root)
    root.mainloop()