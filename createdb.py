import sqlite3
def create_db():
    con=sqlite3.connect(database=r'ims.db')
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS employee (eid  INTEGER PRIMARY KEY AUTOINCREMENT , name text,contact text ,dob text, doj text, salary text )")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS catogory (cid INTEGER PRIMARY KEY AUTOINCREMENT , name text)")
    con.commit()
                                                                                                                                                                                                                             
    cur.execute("CREATE TABLE IF NOT EXISTS product (pid text PRIMARY KEY, china_code text,catogory text, pdes text ,rprice int, wprice int , cost int , nop int, wstock int , pstock int , cstock int , loose int)")
    con.commit()
    
    cur.execute("CREATE TABLE IF NOT EXISTS customer (cusid  INTEGER PRIMARY KEY AUTOINCREMENT , cusname text,cuscontact text ,balance text,chebalance text )")
    con.commit()
    
    cur.execute("CREATE TABLE IF NOT EXISTS logitem (logid  INTEGER PRIMARY KEY AUTOINCREMENT , cusname text,china_code text,loc text,type text,qty text,unitp text,date text )")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS billlog (blogid  INTEGER PRIMARY KEY AUTOINCREMENT ,cusid int , cusname text,date text,invoicenum int,Total int )")
    con.commit()
                                                                                                            
    cur.execute("CREATE TABLE IF NOT EXISTS cheque (chequeid  INTEGER PRIMARY KEY AUTOINCREMENT ,cusid int , cusname text,states text,chequenum text,chequedate text,chequeamt text,chequebank text)")
    con.commit()
                                                                                                                                    
    cur.execute("CREATE TABLE IF NOT EXISTS balance (bid  INTEGER PRIMARY KEY AUTOINCREMENT ,cusid int , cusname text,date text,invoicenum int,amount int,states int,pmethod string ,cpdate string )")
    con.commit()

    

create_db()
    