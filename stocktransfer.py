from tkinter import *
from tkinter import ttk,messagebox
import sqlite3
import time

class stockt:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self,root.config(bg="white")
        self.root.title("Inventory Management system  >> Developed By Hanska Ravishan")
        self.root.focus_force()

        self.var_searchby=StringVar()
        self.var_search_txt=StringVar()

        self.get_w=StringVar()
        self.get_p=StringVar()
        self.get_c=StringVar()
        self.id=StringVar()
        self.get_nop=StringVar()
        self.china=StringVar()

        self.var_wc=StringVar()
        self.var_wp=StringVar()
        self.var_pc=StringVar()
        self.var_cp=StringVar()




        title=Label(self.root,text="STOCK TRANSFER", font=("arial",40,"bold"),bg="#010c48",fg="white",anchor="w", padx=350).place(x=0,y=0,relwidth=1,height=70)


        cmb_search=ttk.Combobox(self.root,textvariable=self.var_searchby,values=("Select","pid","china_code","nop"),state='readonly',justify=CENTER)
        cmb_search.place(x=10,y=100,width=180,height=40)
        cmb_search.current(0)

        txt_search=Entry(self.root,textvariable=self.var_search_txt,font=("goudy old style",15),bg="lightyellow").place(x=200,y=100 , width=435 , height=40)
        btn_search=Button(self.root,text="Search",command=self.search,font=("goudy old style",15),cursor="hand2",bg="green",fg="white").place(x=650 , y=100,height=40)
        btn_showall=Button(self.root,text="Show All",font=("goudy old style",15),cursor="hand2",bg="green",fg="white").place(x=720 , y=100,height=40)

        pro_frame=Frame(self.root,bd=3,relief=RIDGE)
        pro_frame.place(x=0,y=160 , relwidth=1,height=150)

        scoily=Scrollbar(pro_frame,orient=VERTICAL)
        scoilx=Scrollbar(pro_frame,orient=HORIZONTAL)

        self.producttable=ttk.Treeview(pro_frame,columns=("pid","china_code","nop","wstock","pstock","cstock"),yscrollcommand=scoily.set)
        scoily.pack(side=RIGHT,fill=Y)
        scoily.config(command=self.producttable.yview)
        self.producttable.heading("pid",text="Product ID",)
        self.producttable.heading("china_code",text="China Code")
        self.producttable.heading("nop",text="Number Of pices")
        self.producttable.heading("wstock",text="Warehouse")
        self.producttable.heading("pstock",text="Panadura")
        self.producttable.heading("cstock",text="Colombo")

        self.producttable["show"]="headings"

        self.producttable.column("pid",width=60)
        self.producttable.column("china_code",width=140)
        self.producttable.column("nop",width=140)
        self.producttable.column("wstock",width=100)
        self.producttable.column("pstock",width=100)
        self.producttable.column("cstock",width=100)
        
        self.producttable.pack(fill=BOTH,expand=1)
        self.producttable.bind("<ButtonRelease-1>",self.get_data)
        self.show()

        wc_lbl=Label(self.root,text="Warehouse TO Colombo",font=("times new roman",15),fg="black").place(x=30,y=330)
        txt_WC=Entry(self.root,textvariable=self.var_wc,font=("goudy old style",15),bg="lightyellow").place(x=85,y=360 , width=80 , height=40)
        btn_WC=Button(self.root,text="SAVE",command=self.save1,font=("goudy old style",15),cursor="hand2",bg="green",fg="white").place(x=90 , y=410,height=20)

        pc_lbl=Label(self.root,text="Panadura TO Colombo",font=("times new roman",15),fg="black").place(x=300,y=330)
        txt_pc=Entry(self.root,textvariable=self.var_pc,font=("goudy old style",15),bg="lightyellow").place(x=355,y=360 , width=80 , height=40)
        btn_pc=Button(self.root,command=self.save2,text="SAVE",font=("goudy old style",15),cursor="hand2",bg="green",fg="white").place(x=360 , y=410,height=20)

        wp_lbl=Label(self.root,text="Warehouse TO Panadura",font=("times new roman",15),fg="black").place(x=570,y=330)
        txt_wp=Entry(self.root,textvariable=self.var_wp,font=("goudy old style",15),bg="lightyellow").place(x=625,y=360 , width=80 , height=40)
        btn_wp=Button(self.root,command=self.save3,text="SAVE",font=("goudy old style",15),cursor="hand2",bg="green",fg="white").place(x=630 , y=410,height=20)

        cp_lbl=Label(self.root,text="Colombo TO Panadura",font=("times new roman",15),fg="black").place(x=840,y=330)
        txt_search=Entry(self.root,textvariable=self.var_cp,font=("goudy old style",15),bg="lightyellow").place(x=895,y=360 , width=80 , height=40)
        btn_search=Button(self.root,command=self.save4,text="SAVE",font=("goudy old style",15),cursor="hand2",bg="green",fg="white").place(x=890 , y=410,height=20)


#===================================================
    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("Select pid,china_code,nop,wstock,pstock,cstock from product ")
            rows=cur.fetchall()
            self.producttable.delete(*self.producttable.get_children())
            for row in rows:
                self.producttable.insert('',END,values=row)
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
                cur.execute("Select pid,china_code,nop,wstock,pstock,cstock from product where "+self.var_searchby.get()+" LIKE '%"+self.var_search_txt.get()+"%'")
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
        self.id.set(row[0])
        self.china.set(row[1])
        self.get_nop.set(row[2])
        self.get_w.set(row[3])
        self.get_p.set(row[4])
        self.get_c.set(row[5])
        
        

    def save1(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.id.get()=="":
                messagebox.showerror("Error","Please Select Product",parent=self.root)
            if self.var_wc.get()=="":
                messagebox.showerror("Error","Please Enter Amount",parent=self.root)
            elif int(self.get_w.get())-int(self.var_wc.get())<0:
                messagebox.showerror("Error","Please Enter Curect Amount",parent=self.root)
            else:
                totw=int(self.get_w.get())-int(self.var_wc.get())
                totc=int(self.get_c.get())+int(self.var_wc.get())
                cur.execute("Update product set wstock=?,cstock=? where pid=?",(
                        totw,
                        totc,
                        self.id.get(),
                ))
                con.commit()
                cusname="colombo"
                logdate=str(time.strftime("%d-%m-%Y"))
                lock="warehouse"
                type="Box"
                qty=int(self.var_wc.get())
                
                
                self.show()
                cur.execute("Insert into logitem (cusname,china_code,loc,type,qty,date) values (?,?,?,?,?,?)",(

                    cusname,
                    self.china.get(),
                    lock,
                    type,
                    qty,
                    logdate,
                    ))
                con.commit()
                con.close()
                messagebox.showinfo("Succuses","Product Transfer Succusefully",parent=self.root)


        except Exception as ex :
            messagebox.showerror("Error",f"Error Due to : {str(ex)}",parent=self.root)


    def save2(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.id.get()=="":
                messagebox.showerror("Error","Please Select Product",parent=self.root)
            if self.var_pc.get()=="":
                messagebox.showerror("Error","Please Enter Amount",parent=self.root)
            elif int(self.get_p.get())-int(self.var_pc.get())<0:
                messagebox.showerror("Error","Please Enter Curect Amount",parent=self.root)
            else:
                totp=int(self.get_p.get())-int(self.var_pc.get())
                totc=int(self.get_c.get())+int(self.var_pc.get())
                cur.execute("Update product set pstock=?,cstock=? where pid=?",(
                        totp,
                        totc,
                        self.id.get(),
                ))
                con.commit()
                cusname="colombo"
                logdate=str(time.strftime("%d-%m-%Y"))
                lock="Panadura"
                type="Box"
                qty=int(self.var_pc.get())
                
                
                self.show()
                cur.execute("Insert into logitem (cusname,china_code,loc,type,qty,date) values (?,?,?,?,?,?)",(

                    cusname,
                    self.china.get(),
                    lock,
                    type,
                    qty,
                    logdate,
                    ))
                con.commit()
                con.close()
                messagebox.showinfo("Succuses","Product Transfer Succusefully",parent=self.root)


        except Exception as ex :
            messagebox.showerror("Error",f"Error Due to : {str(ex)}",parent=self.root)


    def save3(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.id.get()=="":
                messagebox.showerror("Error","Please Select Product",parent=self.root)
            if self.var_wp.get()=="":
                messagebox.showerror("Error","Please Enter Amount",parent=self.root)
            elif int(self.get_w.get())-int(self.var_wp.get())<0:
                messagebox.showerror("Error","Please Enter Curect Amount",parent=self.root)
            else:
                totw=int(self.get_w.get())-int(self.var_wp.get())
                totp=int(self.get_p.get())+int(self.var_wp.get())
                cur.execute("Update product set wstock=?,pstock=? where pid=?",(
                        totw,
                        totp,
                        self.id.get(),
                ))
                con.commit()
                cusname="Panadura"
                logdate=str(time.strftime("%d-%m-%Y"))
                lock="Warehouse"
                type="Box"
                qty=int(self.var_wp.get())
                
                
                self.show()
                cur.execute("Insert into logitem (cusname,china_code,loc,type,qty,date) values (?,?,?,?,?,?)",(

                    cusname,
                    self.china.get(),
                    lock,
                    type,
                    qty,
                    logdate,
                    ))
                con.commit()
                con.close()
                messagebox.showinfo("Succuses","Product Transfer Succusefully",parent=self.root)


        except Exception as ex :
            messagebox.showerror("Error",f"Error Due to : {str(ex)}",parent=self.root)

    def save4(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.id.get()=="":
                messagebox.showerror("Error","Please Select Product",parent=self.root)
            if self.var_cp.get()=="":
                messagebox.showerror("Error","Please Enter Amount",parent=self.root)
            elif int(self.get_c.get())-int(self.var_cp.get())<0:
                messagebox.showerror("Error","Please Enter Curect Amount",parent=self.root)
            else:
                totc=int(self.get_c.get())-int(self.var_cp.get())
                totp=int(self.get_p.get())+int(self.var_cp.get())
                cur.execute("Update product set cstock=?,pstock=? where pid=?",(
                        totc,
                        totp,
                        self.id.get(),
                ))
                con.commit()
                cusname="Panadura"
                logdate=str(time.strftime("%d-%m-%Y"))
                lock="Colombo"
                type="Box"
                qty=int(self.var_cp.get())
                
                
                self.show()
                cur.execute("Insert into logitem (cusname,china_code,loc,type,qty,date) values (?,?,?,?,?,?)",(

                    cusname,
                    self.china.get(),
                    lock,
                    type,
                    qty,
                    logdate,
                    ))
                con.commit()
                con.close()
                messagebox.showinfo("Succuses","Product Transfer Succusefully",parent=self.root)


        except Exception as ex :
            messagebox.showerror("Error",f"Error Due to : {str(ex)}",parent=self.root)



if __name__=="__main__":
    root=Tk()
    obj=stockt(root)
    root.mainloop()