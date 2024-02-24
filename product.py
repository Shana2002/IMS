from tkinter import *
from tkinter import ttk,messagebox
import sqlite3
import pandas as pd
from xlsxwriter import Workbook
from tkinterdnd2 import DND_FILES, TkinterDnD
import xlsxwriter

class productClass:
    def __init__(self,root):
        ttk.Style().configure("Treeview",background="light blue",
                              foreground="#000000",fieldbackground="red",
                              font=("calibri",12))
        ttk.Style().configure("Treeview.Heading",
                              font=("calibri",12,'bold'))
        self.root=root
        self.root.geometry("1200x700+220+130")
        self,root.config(bg="white")
        self.root.title("Inventory Management system  >> Developed By Hanska Ravishan")
        self.root.focus_force()

        #=======================

        self.var_pro_cat=StringVar()
        self.cat_list=[]
        self.fetch_cat()

        self.var_pro_id=StringVar()
        self.var_pro_china=StringVar()
        self.var_pro_des=StringVar()
        self.var_pro_rprice=StringVar()
        self.var_pro_wprice=StringVar()
        self.var_pro_cost=StringVar()
        self.var_pro_nop=StringVar()
        self.var_pro_warehouse=StringVar()
        self.var_pro_panadura=StringVar()
        self.var_pro_colombo=StringVar()
        self.var_pro_loose=StringVar()

        self.var_searchby=StringVar()
        self.var_search_txt=StringVar()
        self.var_searchbycat=StringVar()


        product_Frame=Frame(self.root,bd=3,relief=RIDGE)
        product_Frame.place(x=100,y=50,width=1000,height=350)

        title=Label(product_Frame,text="Product Details",font=("goudy old style ",15),bg="#0f4d7d",fg="white").pack(side=TOP,fill=X)

        lbl_catogory=Label(product_Frame,text="Catogory",font=("goudy old style ",15)).place(x=30,y=60)
        lbl_id=Label(product_Frame,text="Product ID ",font=("goudy old style ",15)).place(x=30,y=90)
        lbl_china=Label(product_Frame,text="China ID",font=("goudy old style ",15)).place(x=30,y=120)
        lbl_des=Label(product_Frame,text="Product Description",font=("goudy old style ",15)).place(x=30,y=150)
        lbl_rprice=Label(product_Frame,text="Retail Price",font=("goudy old style ",15)).place(x=30,y=180)
        lbl_wprice=Label(product_Frame,text="Wholesale Price",font=("goudy old style ",15)).place(x=30,y=215)
        lbl_cost=Label(product_Frame,text="Cost",font=("goudy old style ",15)).place(x=30,y=245)

        cmb_cat=ttk.Combobox(product_Frame,textvariable=self.var_pro_cat,values=self.cat_list,state='readonly',justify=CENTER)
        cmb_cat.place(x=300 , y=60,width=200)
        cmb_cat.current(0)
        
        #txt_catogory=Entry(product_Frame,font=("goudy old style",15),bg="light yellow").place(x=300 , y=60)
        txt_id=Entry(product_Frame,textvariable=self.var_pro_id,font=("calibri",15),bg="light yellow").place(x=300 , y=90)
        txt_china=Entry(product_Frame,textvariable=self.var_pro_china,font=("calibri",15),bg="light yellow").place(x=300 , y=120)
        txt_des=Entry(product_Frame,textvariable=self.var_pro_des,font=("calibri",15),bg="light yellow").place(x=300 , y=150)
        txt_rprice=Entry(product_Frame,textvariable=self.var_pro_rprice,font=("calibri",15),bg="light yellow").place(x=300 , y=180)
        txt_wprice=Entry(product_Frame,textvariable=self.var_pro_wprice,font=("calibri",15),bg="light yellow").place(x=300, y=215)
        txt_cost=Entry(product_Frame,textvariable=self.var_pro_cost,font=("calibri",15),bg="light yellow").place(x=300, y=245)


        lbl_npices=Label(product_Frame,text="No Pices in Box",font=("goudy old style ",15)).place(x=550,y=60)
        lbl_box=Label(product_Frame,text="No . BOX",font=("goudy old style ",15)).place(x=750,y=90)
        lbl_warehouse=Label(product_Frame,text="Warehouse",font=("goudy old style ",15)).place(x=550,y=120)
        lbl_panadura=Label(product_Frame,text="Panadura",font=("goudy old style ",15)).place(x=550,y=150)
        lbl_colobo=Label(product_Frame,text="Colombo",font=("goudy old style ",15)).place(x=550,y=180)
        lbl_loose=Label(product_Frame,text="Loose",font=("goudy old style ",15)).place(x=550,y=215)

        txt_npices=Entry(product_Frame,textvariable=self.var_pro_nop,font=("calibri",15),bg="light yellow").place(x=700 , y=60)
        txt_warehouse=Entry(product_Frame,textvariable=self.var_pro_warehouse,font=("calibri",15),bg="light yellow").place(x=700 , y=120)
        txt_panadura=Entry(product_Frame,textvariable=self.var_pro_panadura,font=("calibri",15),bg="light yellow").place(x=700 , y=150)
        txt_colombo=Entry(product_Frame,textvariable=self.var_pro_colombo,font=("calibri",15),bg="light yellow").place(x=700 , y=180)
        txt_loose=Entry(product_Frame,textvariable=self.var_pro_loose,font=("calibri",15),bg="light yellow").place(x=700 , y=215)






        btn_save=Button(product_Frame,command=self.add,text="Save",font=("goudy old style",15),bg="green").place(x=60,y=300,height=30)
        btn_Update=Button(product_Frame,command=self.update,text="Update",font=("goudy old style",15),cursor="hand2",bg="Yellow",fg="Black").place(x=150 , y=300,height=30)
        btn_Delete=Button(product_Frame,command=self.delete,text="Delete",font=("goudy old style",15),cursor="hand2",bg="Red",fg="white").place(x=240 , y=300,height=30)
        btn_Clear=Button(product_Frame,command=self.clear,text="Clear",font=("goudy old style",15),cursor="hand2",bg="Black",fg="white").place(x=330 , y=300,height=30)


         #=====search Frame=========
        SearchFrame1=LabelFrame(self.root,text="Search Products ", bg="white",relief=RIDGE)
        SearchFrame1.place(x=180 ,y= 420 , width=900 ,height=70)


        #=========Option=======
        cmb_earchcat=ttk.Combobox(SearchFrame1,textvariable=self.var_searchbycat,values=self.cat_list,state='readonly',justify=CENTER)
        cmb_earchcat.place(x=10,y=14,width=160)
        cmb_earchcat.current(0)

        cmb_search=ttk.Combobox(SearchFrame1,textvariable=self.var_searchby,values=("Select","pid","China_code","pdes"),state='readonly',justify=CENTER)
        cmb_search.place(x=180,y=14,width=160)
        cmb_search.current(0)

        txt_search=Entry(SearchFrame1,textvariable=self.var_search_txt,font=("goudy old style",15),bg="lightyellow").place(x=350,y=10,width=300)
        btn_search=Button(SearchFrame1,command=self.search,text="Search",font=("goudy old style",15),cursor="hand2",bg="green",fg="white").place(x=700 , y=10,height=30)
        btn_showall=Button(SearchFrame1,command=self.show,text="Show All",font=("goudy old style",15),cursor="hand2",bg="green",fg="white").place(x=800 , y=10,height=30)

        btn_export=Button(self.root,command=self.excelp,text="Export Assest",font=("goudy old style",10),cursor="hand2",bg="green",fg="white").place(x=1100,y=450)
        #=====================table

        pro_frame=Frame(self.root,bd=3,relief=RIDGE)
        pro_frame.place(x=0,y=500 , relwidth=1,height=200)


        scoily=Scrollbar(pro_frame,orient=VERTICAL)
        scoilx=Scrollbar(pro_frame,orient=HORIZONTAL)

        self.Producttable=ttk.Treeview(pro_frame,columns=("pid","china_code","catogory","pdes","rprice","wprice","cost","nop","wstock","pstock","cstock","loose"),yscrollcommand=scoily.set)
        scoily.pack(side=RIGHT,fill=Y)
        scoily.config(command=self.Producttable.yview)
        self.Producttable.heading("pid",text="Product ID")
        self.Producttable.heading("china_code",text="China Code")
        self.Producttable.heading("catogory",text="catogory")
        self.Producttable.heading("pdes",text="Description")
        self.Producttable.heading("rprice",text="Retail Price")
        self.Producttable.heading("wprice",text="Wholesale Price")
        self.Producttable.heading("cost",text="Cost")
        self.Producttable.heading("nop",text="No of pices")
        self.Producttable.heading("wstock",text="Warehouse")
        self.Producttable.heading("pstock",text="Panadura")
        self.Producttable.heading("cstock",text="Colombo")
        self.Producttable.heading("loose",text="Loose")

        self.Producttable["show"]="headings"

        self.Producttable.column("pid",width=100,anchor='center')
        self.Producttable.column("china_code",width=140,anchor='center')
        self.Producttable.column("catogory",width=100,anchor='center')
        self.Producttable.column("pdes",width=100,anchor='center')
        self.Producttable.column("rprice",width=100,anchor='center')
        self.Producttable.column("wprice",width=100,anchor='center')
        self.Producttable.column("cost",width=100,anchor='center')
        self.Producttable.column("nop",width=60,anchor='center')
        self.Producttable.column("wstock",width=60,anchor='center')
        self.Producttable.column("pstock",width=60,anchor='center')
        self.Producttable.column("cstock",width=60,anchor='center')
        self.Producttable.column("loose",width=60,anchor='center')
        

        self.Producttable.pack(fill=BOTH,expand=1)
        self.Producttable.bind("<ButtonRelease-1>",self.get_data)
        self.show()


        
#====================================
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
    
    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_pro_id.get()=="" or self.var_pro_cat.get()=="Select" :
                messagebox.showerror("Error","Product ID AND CATEGORY MUST BE required",parent=self.root)
            else :
                cur.execute("Select * from product where pid=?",(self.var_pro_id.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This product ID Already Asigned , Try Differnt",parent=self.root)
                else : 
                    cur.execute("Insert into product (pid,china_code,catogory,pdes,rprice,wprice,cost,nop,wstock,pstock,cstock,loose) values (?,?,?,?,?,?,?,?,?,?,?,?)",(

                    self.var_pro_id.get(),
                    self.var_pro_china.get(),
                    self.var_pro_cat.get(),
                    self.var_pro_des.get(),
                    self.var_pro_rprice.get(),
                    self.var_pro_wprice.get(),
                    self.var_pro_cost.get(),
                    self.var_pro_nop.get(),
                    self.var_pro_warehouse.get(),
                    self.var_pro_panadura.get(),
                    self.var_pro_colombo.get(),
                    self.var_pro_loose.get(), 
                    
                    ))
                    con.commit()
                    messagebox.showinfo("Succuses","Product Added Succusefully",parent=self.root)
                    self.show()
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error Due to :{str(ex)}",parent=self.root)
        
    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("Select * from product")
            rows=cur.fetchall()
            self.Producttable.delete(*self.Producttable.get_children())
            for row in rows:
                self.Producttable.insert('',END,values=row)
        except Exception as ex :
            messagebox.showerror("Error",f"Error Due to : {str(ex)}",parent=self.root)

    
    def get_data(self,ev):
        f=self.Producttable.focus()
        content=(self.Producttable.item(f))
        row=content['values']
        self.var_pro_id.set(row[0]),
        self.var_pro_china.set(row[1]),
        self.var_pro_cat.set(row[2]),
        self.var_pro_des.set(row[3]),
        self.var_pro_rprice.set(row[4]),
        self.var_pro_wprice.set(row[5]),
        self.var_pro_cost.set(row[6]),
        self.var_pro_nop.set(row[7]),
        self.var_pro_warehouse.set(row[8]),
        self.var_pro_panadura.set(row[9]),
        self.var_pro_colombo.set(row[10]),
        self.var_pro_loose.set(row[11]), 
                    



    def update(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_pro_id.get()=="":
                messagebox.showerror("Error","Employee ID MUST BE required",parent=self.root)
            else :
                cur.execute("Select * from product where pid=?",(self.var_pro_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Employee ID , Try Differnt",parent=self.root)
                else : 
                    cur.execute("Update product set china_code=?,pdes=?,catogory=?,rprice=?,wprice=?,cost=?,nop=?,wstock=?,pstock=?,cstock=?,loose=? where pid=?",(

                    self.var_pro_china.get(),
                    self.var_pro_des.get(),
                    self.var_pro_cat.get(),
                    self.var_pro_rprice.get(),
                    self.var_pro_wprice.get(),
                    self.var_pro_cost.get(),
                    self.var_pro_nop.get(),
                    self.var_pro_warehouse.get(),
                    self.var_pro_panadura.get(),
                    self.var_pro_colombo.get(),
                    self.var_pro_loose.get(),
                    self.var_pro_id.get(), 
                        

                    ))
                    con.commit()
                    messagebox.showinfo("Succuses","Product Update Succusefully",parent=self.root)
                    self.show()
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error Due to :{str(ex)}",parent=self.root)


    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_pro_id.get()=="":
                messagebox.showerror("Error","Product ID MUST BE required",parent=self.root)
            else :
                cur.execute("Select * from product where pid=?",(self.var_pro_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Product ID , Try Differnt",parent=self.root)
                else : 
                    op=messagebox.askyesno("Conform","Do You really want to Delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from product where pid=?",(self.var_pro_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","product Delete Succusefully",parent=self.root)
                        self.show()
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error Due to :{str(ex)}",parent=self.root)

    def clear(self):
                #id,chin,CAT,des,cost,nop,w,p
                self.var_pro_id.set("")
                self.var_pro_china.set("")
                self.var_pro_cat.set("Select")
                self.var_pro_des.set("")
                self.var_pro_rprice.set("")
                self.var_pro_wprice.set("")
                self.var_pro_cost.set("")
                self.var_pro_nop.set("")
                self.var_pro_warehouse.set("")
                self.var_pro_panadura.set("")
                self.var_pro_colombo.set("")
                self.var_pro_loose.set("") 


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
                if self.var_searchbycat.get()=="Select Catogory":
                    cur.execute("Select * from product where "+self.var_searchby.get()+" LIKE '%"+self.var_search_txt.get()+"%'")
                    rows=cur.fetchall()
                else:
                    cur.execute("Select * from product where "+self.var_searchby.get()+" LIKE '%"+self.var_search_txt.get()+"%' and catogory LIKE '%"+self.var_searchbycat.get()+"%'")
                    rows=cur.fetchall()
            if len(rows)!=0:
                self.Producttable.delete(*self.Producttable.get_children())
                for row in rows:
                    self.Producttable.insert('',END,values=row)
            else :
                    messagebox.showerror("Error","No Record Found!!",parent=self.root)
        except Exception as ex :
            messagebox.showerror("Error",f"Error Due to : {str(ex)}",parent=self.root)


    def excelp(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            Workbook=xlsxwriter.Workbook(f'aassest.xlsx')
            worksheet=Workbook.add_worksheet()
            worksheet.write('A1',"Item No")
            worksheet.write('B1',"China Code")
            worksheet.write('C1',"Cost")
            worksheet.write('D1',"QTY")
            worksheet.write('E1',"Total")

            worksheet.set_column('A:A', 18.7)
            worksheet.set_column('B:B', 24)
            worksheet.set_column('C:C', 10)
            worksheet.set_column('D:D', 8)
            worksheet.set_column('E:E', 17.71)

            x=1 
            int(x)
            col=0
            int(col)
            tot=0
            cur.execute("Select pid , china_code , cost ,nop, wstock , pstock,loose from product")
            rows=cur.fetchall()
            for row in rows:
                w=row[4]
                p=row[5]
                nop=row[3]
                cost=row[2]
                l=row[6]

                totp=int(int(w+p)*int(nop))+int(l)
                tota=totp*int(cost)
                tot=tot+tota
                
                worksheet.write(x,col,row[0])
                worksheet.write(x,col+1,row[1])
                worksheet.write(x,col+2,row[2])
                worksheet.write(x,col+3,totp)
                worksheet.write(x,col+4,tota)
                
                x+=1
            
            Workbook.close()

        except Exception as ex :
            messagebox.showerror("Error",f"Error Due to : {str(ex)}",parent=self.root)
        


if __name__=="__main__":
    root=Tk()
    obj=productClass(root)
    root.mainloop()