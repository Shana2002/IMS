from tkinter import *
from tkinter import ttk,messagebox
import sqlite3
import os


class saleClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1000x650+220+130")
        self,root.config(bg="white")
        self.root.title("Inventory Management system  >> Developed By Hanska Ravishan")
        self.root.focus_force()

        #==============Variables==========
        self.var_invoice=StringVar()
        self.bill_list=[]


        #=======================
        title=Label(self.root,text="Customer BILL", font=("arial",40,"bold"),bg="#010c48",fg="white",anchor="w", padx=350).place(x=0,y=0,relwidth=1,height=70)
        
        
        lbl_invoice=Label(self.root,text="Invoice Number " , font=("times new roman",15),bg="white").place(x=50,y=100)
        txt_invoice=Entry(self.root,textvariable=self.var_invoice, font=("times new roman",15),bg="white").place(x=200,y=100)

        btn_search=Button(self.root,command=self.search,text="Search",font=("times new roman",15),fg="white",bg="green",cursor="hand2").place(x=420,y=100,height=30)
        btn_clera=Button(self.root,text="clear",command=self.clear,font=("times new roman",15),fg="black",bg="light gray",cursor="hand2").place(x=500,y=100,height=30)

        #======Bill List+++++++

        sales_frame=Frame(self.root,bd=3,relief=RIDGE)
        sales_frame.place(x=50,y=140,width=200,height=500)

        scrolly=Scrollbar(sales_frame,orient=VERTICAL)
        self.sales_List=Listbox(sales_frame,font=("goudy old style",15),bg="white",yscrollcommand=scrolly)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.sales_List.yview)
        self.sales_List.pack(fill=BOTH,expand=1)

        self.sales_List.bind("<ButtonRelease-1>",self.get_data)

        #=====Bill Area=======
        bill_Frame=Frame(self.root,bd=3,relief=RIDGE)
        bill_Frame.place(x=280,y=140,width=700,height=500)

        lbl_title2=Label(bill_Frame,text="Customer Bill Area", font=("arial",15,"bold"),bg="orange",anchor="w").pack(side=TOP,fill=X)

        scrolly2=Scrollbar(bill_Frame,orient=VERTICAL)
        self.bill_Frame=Text(bill_Frame,font=("goudy old style",15),bg="lightyellow",yscrollcommand=scrolly)
        scrolly2.pack(side=RIGHT,fill=Y)
        scrolly2.config(command=self.bill_Frame.yview)
        self.bill_Frame.pack(fill=BOTH,expand=1)

        self.show()
#==================
    def show(self):
        del self.bill_list[:]
        self.sales_List.delete(0,END)
        for i in os.listdir('billtxt'):
           if i.split('.')[-1]=='txt':
                self.sales_List.insert(END,i)
                self.bill_list.append(i.split('.')[0])

    def get_data(self,ev):
        index_=self.sales_List.curselection()
        file_name=self.sales_List.get(index_)
        self.bill_Frame.delete('1.0',END)
        fp=open(f'billtxt/{file_name}','r')
        for i in fp:
            self.bill_Frame.insert(END,i)
        fp.close()

    def search(self):
        if self.var_invoice.get()=="" :
            messagebox.showerror("Error","Invoice Number Must Be Required",parent=self.root)
        else :
            if self.var_invoice.get() in self.bill_list:
                fp=open(f'billtxt/{self.var_invoice.get()}.txt','r')
                self.bill_Frame.delete('1.0',END)
                for i in fp:
                    self.bill_Frame.insert(END,i)
                fp.close()
            else:
                messagebox.showerror("Error","Invalid Invoice Number",parent=self.root)
    def clear(self):
        self.show()
        self.bill_Frame.delete('1.0',END)
if __name__=="__main__":
    root=Tk()
    obj=saleClass(root)
    root.mainloop()