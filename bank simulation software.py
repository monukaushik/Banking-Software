from tkinter import *
from tkinter.ttk import Combobox
from PIL import Image,ImageTk
from tkinter import messagebox,filedialog
import sqlite3
import os
import shutil

win=Tk()
win.state("zoomed")

img=Image.open("img.jpg")
ImgTk=ImageTk.PhotoImage(img,master=win)
l=Label(win,image=ImgTk)
l.place(relx=0,rely=0)

title=Label(win,text="Bank Account Simulation Software",font=('Futura',30,'bold'),bg="yellow",fg="Black")
title.place(relx=0.3,rely=0.005)

default_pic=ImageTk.PhotoImage(Image.open("f:\Project Python\Bank Account Simulation\profile.png").resize((70,70)),master=win)

def home_screen():
    frm=Frame(win)
    frm.configure(bg="LightSteelBlue")
    frm.place(x=400,y=130,relwidth=0.5,relheight=.5)
    def newuser():
        frm.destroy()
        newuser_screen()
    
    def forgot():
        frm.destroy()
        forgot_pass_screen()
    
    def login():
        acn=acn_entry.get()
        pwd=pass_entry.get()
        if(len(acn)==0 or len(pwd)==0):
            messagebox.showerror("Validation","Please fill both fields")
        elif(not acn.isdigit()):
            messagebox.showerror("Validation","ACN must be numeric")
        elif(not len(pwd)==6):
            messagebox.showerror("validation","Enter 6 digit password")
        else:
            con=sqlite3.connect(database="bank.sqlite")
            cur=con.cursor()
            cur.execute("select * from users where acn=? and pass=?",(acn,pwd))
            global tup
            tup=cur.fetchone()
            if(tup==None):
                messagebox.showerror("Login","Invalid ACN and PASS!!")
            else:
                frm.destroy()
                login_screen()

    lbl_acn=Label(frm,text="User LogIn",font=('Arial',20,'bold'),bg='Yellow')
    lbl_acn.place(relx=.4,rely=.01)

    lbl_acn=Label(frm,text="Account No:",font=('Arial',15,'bold'),bg='Yellow')
    lbl_acn.place(relx=.2,rely=.2)
    
    acn_entry=Entry(frm,font=('Arial',15,'bold'),bd=5)
    acn_entry.place(relx=.4,rely=.2)
    
    lbl_pass=Label(frm,text="Password:",font=('Arial',15,'bold'),bg='yellow')
    lbl_pass.place(relx=.2,rely=.33)
    
    pass_entry=Entry(frm,font=('Arial',15,'bold'),bd=5,show="*")
    pass_entry.place(relx=.4,rely=.33)

    login_btn=Button(frm,font=('Arial',15,'bold'),bg='yellow',bd=5,text="login",command=login)
    login_btn.place(relx=.2,rely=.6)

    fp_btn=Button(frm,font=('Arial',15,'bold'),bg='yellow',bd=5,text="Forgot Password",command=forgot)
    fp_btn.place(relx=.35,rely=.6)
    
    newuser_btn=Button(frm,font=('Arial',15,'bold'),bg='yellow',bd=5,text="New User",command=newuser)
    newuser_btn.place(relx=.68,rely=.6)

def newuser_screen():
    frm=Frame(win)
    frm.configure(bg="LightSteelBlue")
    frm.place(x=400,y=130,relwidth=0.5,relheight=.5)

    def back():
        frm.destroy()
        home_screen()

    def submit():
        name=name_entry.get()
        pas=pass_entry.get()
        email=email_entry.get()
        mob=mob_entry.get()
        acntype=cb_type.get()
        bal=1000
          
        if(len(name)==0 or len(pas)==0 or len(email)==0 or len(mob)==0):
            messagebox.showerror("Validation","Please fill all fields")   
        elif(not mob.isdigit()):
            messagebox.showerror("Validation","Mobile no must be numeric")

        elif(not len(mob)==10):
            messagebox.showerror("validation","Enter 10 digit mob no")
        elif(not len(pas)==6):
            messagebox.showerror("validation","Enter 6 digit password")
            
        elif(not email.endswith(".com")):
             messagebox.showerror("Validation","Enter Valid Mail ")
        else:
          frm.destroy()
          home_screen()

 
        con=sqlite3.connect(database="bank.sqlite")
        cur=con.cursor()
        cur.execute("insert into users(name,pass,email,mob,type,bal) values(?,?,?,?,?,?)",(name,pas,email,mob,acntype,bal))
        con.commit()
        con.close()
        
        con=sqlite3.connect(database="bank.sqlite")
        cur=con.cursor()
        cur.execute("select max(acn) from users")
        tup=cur.fetchone()
        messagebox.showinfo("Account",f"Account opened with ACN:{tup[0]}")
        con.close()



    lbl_name=Label(frm,text="New User Details",font=('Arial',15,'bold'),bg='Yellow')
    lbl_name.place(relx=.4,rely=0)
    
    back_btn=Button(frm,font=('Arial',15,'bold'),bd=5,text="back",bg='Yellow',command=back)
    back_btn.place(relx=.6,rely=.72)
    
    lbl_name=Label(frm,text="Name:",font=('Arial',15,'bold'),bg='Yellow')
    lbl_name.place(relx=.3,rely=.1)
    
    name_entry=Entry(frm,font=('Arial',15,'bold'),bd=5)
    name_entry.place(relx=.4,rely=.1)
    
    lbl_pass=Label(frm,text="Pass:",font=('Arial',15,'bold'),bg='Yellow')
    lbl_pass.place(relx=.3,rely=.21)
    
    pass_entry=Entry(frm,font=('Arial',15,'bold'),bd=5,show="*")
    pass_entry.place(relx=.4,rely=.21)
    
    lbl_email=Label(frm,text="Email:",font=('Arial',15,'bold'),bg='Yellow')
    lbl_email.place(relx=.3,rely=.31)
    
    email_entry=Entry(frm,font=('Arial',15,'bold'),bd=5)
    email_entry.place(relx=.4,rely=.31)
    
    lbl_mob=Label(frm,text="Mob:",font=('Arial',15,'bold'),bg='Yellow')
    lbl_mob.place(relx=.3,rely=.41)
    
    mob_entry=Entry(frm,font=('Arial',15,'bold'),bd=5)
    mob_entry.place(relx=.4,rely=.41)
    
    ack_type=Label(frm,text="Type:",font=('Arial',15,'bold'),bg='Yellow')
    ack_type.place(relx=.3,rely=.53)
    
    cb_type=Combobox(frm,values=['Saving','Current'],font=('Arial',15,'bold'))
    cb_type.place(relx=.4,rely=.53)
    cb_type.current(0)
    
    sub_btn=Button(frm,font=('Arial',15,'bold'),bd=5,text="Submit",bg='Yellow',command=submit)
    sub_btn.place(relx=.4,rely=.72)

def forgot_pass_screen():
    frm=Frame(win)
    frm.configure(bg="LightSteelBlue")
    frm.place(x=400,y=130,relwidth=0.5,relheight=.5)

    def submit():
        ack3=ack3_entry.get()
        email2=email_entry.get()
        mob2=mob_entry.get()
          
        if(len(ack3)==0 or len(email2)==0 or len(mob2)==0):
            messagebox.showerror("Validation","Please fill all fields")   
        elif(not mob2.isdigit()):
            messagebox.showerror("Validation","Mobile no must be numeric")
        elif(not len(mob2)==10):
            messagebox.showerror("validation","Enter 10 digit mob no")
        elif(not len(ack3)==6):
            messagebox.showerror("validation","Enter 6 digit ack no")
        elif(not email2.endswith(".com")):
             messagebox.showerror("Validation","Enter Valid Mail ")
        elif(not ack3.isdigit()):
             messagebox.showerror("Validation","Enter digit in account no")
        else:
          frm.destroy()
          home_screen()

    def back():
        frm.destroy()
        home_screen()

    lbl_name=Label(frm,text="Enter User Details",font=('Arial',15,'bold'),bg='Yellow')
    lbl_name.place(relx=.4,rely=0)
    
    back_btn=Button(frm,font=('Arial',15,'bold'),bd=5,text="Back",bg='Yellow',command=back)
    back_btn.place(relx=.6,rely=.62)
    
    ack3_no=Label(frm,text="Account No:",font=('Arial',15,'bold'),bg='Yellow')
    ack3_no.place(relx=.2,rely=.22)
    
    ack3_entry=Entry(frm,font=('Arial',15,'bold'),bd=5)
    ack3_entry.place(relx=.4,rely=.22)
    
    lbl_email=Label(frm,text="Email ID:",font=('Arial',15,'bold'),bg='Yellow')
    lbl_email.place(relx=.2,rely=.32)
    
    email_entry=Entry(frm,font=('Arial',15,'bold'),bd=5)
    email_entry.place(relx=.4,rely=.32)
    
    lbl_mob=Label(frm,text="Mob No:",font=('Arial',15,'bold'),bg='Yellow')
    lbl_mob.place(relx=.2,rely=.42)
    
    mob_entry=Entry(frm,font=('Arial',15,'bold'),bd=5)
    mob_entry.place(relx=.4,rely=.42)
    
    sub_btn=Button(frm,font=('Arial',15,'bold'),bd=5,text="Submit",bg='Yellow',command=submit)
    sub_btn.place(relx=.4,rely=.62)

def login_screen():
    frm=Frame(win)
    frm.configure(bg="LightSteelBlue")
    frm.place(x=400,y=130,relwidth=0.5,relheight=.5)

    def Logout():
        frm.destroy()
        home_screen()
        
    def details():
        frm.destroy()
        details_screen()
     
    def withdraw():
        frm.destroy()
        withdraw_screen()
        
    def deposit():
        frm.destroy()
        deposit_screen()
    
    def txn():
        frm.destroy()
        txnhistory_screen()        
        
    def update():
        frm.destroy()
        updateprofile_screen()

    def update_pic():
        path=filedialog.askopenfilename()
        index=path.rindex(".")
        ext=path[index+1:]
        shutil.copy(path,f"images/{tup[0]}.{ext}")
        
        pic=ImageTk.PhotoImage(Image.open(f"images/{tup[0]}.{ext}").resize((100,80)),master=win)

        
    lbl_name=Label(frm,text=f"Welcome,{tup[1]}",font=('Arial',10,'bold'),bg='Yellow')
    lbl_name.place(relx=0.01,rely=0.01)

    lbl_pic=Label(frm,image=default_pic)
    lbl_pic.place(relx=0.01,rely=.12)

    imgs=os.listdir("images")
    
    for img in imgs:
        if(img.startswith(str(tup[0]))):
            pic=ImageTk.PhotoImage(Image.open(f"images/{img}").resize((100,80)),master=win)
            lbl_pic.configure(image=pic)
            lbl_pic.image=pic   
            
    def update_pic():
        path=filedialog.askopenfilename()
        index=path.rindex(".")
        ext=path[index+1:]
        shutil.copy(path,f"images/{tup[0]}.{ext}")
        
        default_pic=ImageTk.PhotoImage(Image.open(f"images/{tup[0]}.{ext}").resize((100,80)),master=win)
        lbl_pic.configure(image=default_pic)
        lbl_pic.image=default_pic
    
    logout_btn=Button(frm,font=('Arial',10,'bold'),bd=5,text="Logout",bg='Yellow',command=Logout)
    logout_btn.place(relx=0.88,rely=0.15)

    lbl_name=Label(frm,text="Account Summary",font=('Arial',15,'bold'),bg='Yellow')
    lbl_name.place(relx=0.4,rely=0.3)

    con=sqlite3.connect(database="bank.sqlite")
    cur=con.cursor()
    cur.execute("select * from users where acn=? and pass=?",(tup[0],tup[2]))
    row=cur.fetchone()
    
    data=f"\t{row[6]}"
    
    details_lbl=Label(frm,text=data,bg="LightSteelBlue",fg="black",font=('Arial',10,'bold'))
    details_lbl.place(relx=.41,rely=.45)

    lbl_name=Label(frm,text="Current Balance :",font=('Arial',10,'bold'),bg='Yellow')
    lbl_name.place(relx=0.3,rely=0.45)

    details_btn=Button(frm,font=('Arial',10,'bold'),bd=5,text="User Details",bg='Yellow',command=details)
    details_btn.place(relx=0.26,rely=0.01)

    deposit_btn=Button(frm,font=('Arial',10,'bold'),bd=5,text="Deposit",bg='Yellow',command=deposit)
    deposit_btn.place(relx=0.41,rely=0.01)

    withdraw_btn=Button(frm,font=('Arial',10,'bold'),bd=5,text="Withdraw",bg='Yellow',command=withdraw)
    withdraw_btn.place(relx=0.52,rely=0.01)

    hist_btn=Button(frm,font=('Arial',10,'bold'),bd=5,text="Txn History",bg='Yellow',command=txn)
    hist_btn.place(relx=0.67,rely=0.01)

    update_btn=Button(frm,font=('Arial',7,'bold'),bd=5,text="Update Pic",bg='Yellow',command=update_pic)
    update_btn.place(relx=0.01,rely=0.37)

    updateprofile_btn=Button(frm,font=('Arial',10,'bold'),bd=5,text="Update Profile",bg='Yellow',command=update)
    updateprofile_btn.place(relx=0.82,rely=0.01)

def details_screen():
    frm=Frame(win)
    frm.configure(bg="LightSteelBlue")
    frm.place(x=400,y=130,relwidth=0.5,relheight=.5)

    def Logout():
        frm.destroy()
        home_screen()  
        
    def back():
        frm.destroy()
        login_screen()

    lbl_name=Label(frm,text=f"Welcome,{tup[1]}",font=('Arial',15,'bold'),bg='Yellow')
    lbl_name.place(relx=0.01,rely=0.01)

    lbl_pic=Label(frm,image=default_pic)
    lbl_pic.place(relx=0.01,rely=.12)

    imgs=os.listdir("images")
    
    for img in imgs:
        if(img.startswith(str(tup[0]))):
            pic=ImageTk.PhotoImage(Image.open(f"images/{img}").resize((100,80)),master=win)
            lbl_pic.configure(image=pic)
            lbl_pic.image=pic   


    lbl_name=Label(frm,text="User Information",font=('Arial',15,'bold'),bg='Yellow')
    lbl_name.place(relx=0.4,rely=0.01)
    
    con=sqlite3.connect(database="bank.sqlite")
    cur=con.cursor()
    cur.execute("select * from users where acn=? and pass=?",(tup[0],tup[2]))
    row=cur.fetchone()
    
    data=f"""  \tAcn:\t{row[0]}
               Name :\t{row[1]}
               Mob:\t{row[3]}
               \tEmail:\t{row[4]}
               type:\t{row[5]}
               bal:\t{row[6]}
  
    """
    details_lbl=Label(frm,text=data,bg="LightSteelBlue",fg="black",font=('Arial',10,'bold'))
    details_lbl.place(relx=.2,rely=.2)
    
    logout_btn=Button(frm,font=('Arial',10,'bold'),bd=5,text="Logout",bg='Yellow',command=Logout)
    logout_btn.place(relx=0.9,rely=0.01)

    back_btn=Button(frm,font=('Arial',15,'bold'),bd=5,text="back",bg='Yellow',command=back)
    back_btn.place(relx=.01,rely=.8)   

def withdraw_screen():
    frm=Frame(win)
    frm.configure(bg="LightSteelBlue")
    frm.place(x=400,y=130,relwidth=0.5,relheight=.5)

    def Logout():
        frm.destroy()
        home_screen()  
        
    def back():
        frm.destroy()
        login_screen()
    def submit():
        amt=int(wbalance_entry.get())
        con=sqlite3.connect(database="bank.sqlite")
        cur=con.cursor()
        cur.execute("select bal from users where acn=?",(tup[0],))
        t=cur.fetchone()
        bal=t[0]
        if(bal>amt):
            
            bal=bal-amt
            con.close()

            con=sqlite3.connect(database="bank.sqlite")
            cur=con.cursor()
            cur.execute("update users set bal=? where acn=?",(bal,tup[0]))
            con.commit()
            con.close()
            messagebox.showinfo("Deposit","Amount withdrawn")

            con=sqlite3.connect(database="bank.sqlite")
            cur=con.cursor()
            cur.execute("insert into txn values(?,?,?,?)",(tup[0],amt," ",bal))
            con.commit()
            con.close()
        else:
            messagebox.showerror("Withdraw","Insufficient Bal")


    lbl_name=Label(frm,text=f"Welcome{tup[1]}",font=('Arial',15,'bold'),bg='Yellow')
    lbl_name.place(relx=0.01,rely=0.01)

    lbl_pic=Label(frm,image=default_pic)
    lbl_pic.place(relx=0.01,rely=.12)

    imgs=os.listdir("images")
    
    for img in imgs:
        if(img.startswith(str(tup[0]))):
            pic=ImageTk.PhotoImage(Image.open(f"images/{img}").resize((100,80)),master=win)
            lbl_pic.configure(image=pic)
            lbl_pic.image=pic   


    lbl_name=Label(frm,text="Account Information",font=('Arial',15,'bold'),bg='Yellow')
    lbl_name.place(relx=0.4,rely=0.01)

    con=sqlite3.connect(database="bank.sqlite")
    cur=con.cursor()
    cur.execute("select * from users where acn=? and pass=?",(tup[0],tup[2]))
    row=cur.fetchone()
    
    data=f"\t{row[6]}"
    
    details_lbl=Label(frm,text=data,bg="LightSteelBlue",fg="black",font=('Arial',10,'bold'))
    details_lbl.place(relx=.45,rely=.2)

    lbl_name=Label(frm,text="Current Balance :",font=('Arial',10,'bold'),bg='Yellow')
    lbl_name.place(relx=0.3,rely=0.2)
    

    lbl_name=Label(frm,text="Withdraw Amount :",font=('Arial',10,'bold'),bg='Yellow')
    lbl_name.place(relx=0.3,rely=0.3)

    wbalance_entry=Entry(frm,font=('Arial',10,'bold'),bd=5)
    wbalance_entry.place(relx=.5,rely=.3)


    logout_btn=Button(frm,font=('Arial',10,'bold'),bd=5,text="Submit",bg='Yellow',command=submit)
    logout_btn.place(relx=0.55,rely=0.47)
    
    logout_btn=Button(frm,font=('Arial',10,'bold'),bd=5,text="Logout",bg='Yellow',command=Logout)
    logout_btn.place(relx=0.9,rely=0.01)

    back_btn=Button(frm,font=('Arial',15,'bold'),bd=5,text="back",bg='Yellow',command=back)
    back_btn.place(relx=.01,rely=.8)   

def deposit_screen():
    frm=Frame(win)
    frm.configure(bg="LightSteelBlue")
    frm.place(x=400,y=130,relwidth=0.5,relheight=.5)

    def Logout():
        frm.destroy()
        home_screen()  
        
    def back():
        frm.destroy()
        login_screen()

    def submit():
        amt=int(dbalance_entry.get())
        con=sqlite3.connect(database="bank.sqlite")
        cur=con.cursor()
        cur.execute("select bal from users where acn=?",(tup[0],))
        t=cur.fetchone()
        bal=t[0]
        bal=bal+amt
        con.close()
        
        con=sqlite3.connect(database="bank.sqlite")
        cur=con.cursor()
        cur.execute("update users set bal=? where acn=?",(bal,tup[0]))
        con.commit()
        con.close()
        messagebox.showinfo("Deposit","Amount deposited")
        
        con=sqlite3.connect(database="bank.sqlite")
        cur=con.cursor()
        cur.execute("insert into txn values(?,?,?,?)",(tup[0]," ",amt,bal))
        con.commit()
        con.close()

    lbl_name=Label(frm,text=f"Welcome{tup[1]}",font=('Arial',15,'bold'),bg='Yellow')
    lbl_name.place(relx=0.01,rely=0.01)

    lbl_pic=Label(frm,image=default_pic)
    lbl_pic.place(relx=0.01,rely=.12)

    imgs=os.listdir("images")
    
    for img in imgs:
        if(img.startswith(str(tup[0]))):
            pic=ImageTk.PhotoImage(Image.open(f"images/{img}").resize((100,80)),master=win)
            lbl_pic.configure(image=pic)
            lbl_pic.image=pic   


    lbl_name=Label(frm,text="Account Information",font=('Arial',15,'bold'),bg='Yellow')
    lbl_name.place(relx=0.4,rely=0.01)

    con=sqlite3.connect(database="bank.sqlite")
    cur=con.cursor()
    cur.execute("select * from users where acn=? and pass=?",(tup[0],tup[2]))
    row=cur.fetchone()
    
    data=f"\t{row[6]}"
    
    details_lbl=Label(frm,text=data,bg="LightSteelBlue",fg="black",font=('Arial',10,'bold'))
    details_lbl.place(relx=.45,rely=.2)

    lbl_name=Label(frm,text="Current Balance :",font=('Arial',10,'bold'),bg='Yellow')
    lbl_name.place(relx=0.3,rely=0.2)
    

    lbl_name=Label(frm,text="Deposit Amount :",font=('Arial',10,'bold'),bg='Yellow')
    lbl_name.place(relx=0.3,rely=0.3)

    dbalance_entry=Entry(frm,font=('Arial',10,'bold'),bd=5)
    dbalance_entry.place(relx=.5,rely=.3)

    logout_btn=Button(frm,font=('Arial',10,'bold'),bd=5,text="Submit",bg='Yellow',command=submit)
    logout_btn.place(relx=0.55,rely=0.5)

    
    logout_btn=Button(frm,font=('Arial',10,'bold'),bd=5,text="Logout",bg='Yellow',command=Logout)
    logout_btn.place(relx=0.9,rely=0.01)

    back_btn=Button(frm,font=('Arial',15,'bold'),bd=5,text="back",bg='Yellow',command=back)
    back_btn.place(relx=.01,rely=.8)   

def txnhistory_screen():
    frm=Frame(win)
    frm.configure(bg="LightSteelBlue")
    frm.place(x=400,y=130,relwidth=0.5,relheight=.5)

    def Logout():
        frm.destroy()
        home_screen()  
        
    def back():
        frm.destroy()
        login_screen()

    lbl_name=Label(frm,text=f"Welcome{tup[1]}",font=('Arial',15,'bold'),bg='Yellow')
    lbl_name.place(relx=0.01,rely=0.01)

    lbl_pic=Label(frm,image=default_pic)
    lbl_pic.place(relx=0.01,rely=.12)

    imgs=os.listdir("images")
    
    for img in imgs:
        if(img.startswith(str(tup[0]))):
            pic=ImageTk.PhotoImage(Image.open(f"images/{img}").resize((100,80)),master=win)
            lbl_pic.configure(image=pic)
            lbl_pic.image=pic   


    lbl_name=Label(frm,text="Transaction History",font=('Arial',15,'bold'),bg='Yellow')
    lbl_name.place(relx=0.4,rely=0.01)
   
    logout_btn=Button(frm,font=('Arial',10,'bold'),bd=5,text="Logout",bg='Yellow',command=Logout)
    logout_btn.place(relx=0.91,rely=0.01)

    back_btn=Button(frm,font=('Arial',15,'bold'),bd=5,text="back",bg='Yellow',command=back)
    back_btn.place(relx=.01,rely=.8)

     
    con=sqlite3.connect(database="bank.sqlite")
    cur=con.cursor()
    cur.execute("select * from txn where acn=?",(tup[0],))
    txn_data="Account No\t Withdrow Amt\t Deposite Amt\t Updated Balance\n\n"
    all_data=cur.fetchall() 
    for t in all_data:
        t=map(str,t)
        t1="                         ".join(t)
        txn_data=txn_data+t1+"\n\n"
    lbl_txndata=Label(frm,text=txn_data,font=("Arial",10,"bold"),bg="LightSteelBlue",fg="black")
    lbl_txndata.place(relx=.2,rely=.3)  
    con.close()

def updateprofile_screen():
    frm=Frame(win)
    frm.configure(bg="LightSteelBlue")
    frm.place(x=400,y=130,relwidth=0.5,relheight=.5)

    def Logout():
        frm.destroy()
        home_screen()  
        
    def back():
        frm.destroy()
        login_screen()
        
    def Submit():
        pwd=pass_entry.get()
        email=emailid_entry.get()
        mob=mobno_entry.get()
        name=name_entry.get()
          
        if(len(name)==0 or len(email)==0 or len(mob)==0 or pwd==0):
            messagebox.showerror("Validation","Please fill all fields")   
        elif(not mob.isdigit()):
            messagebox.showerror("Validation","Mobile no must be numeric")
        elif(not len(mob)==10):
            messagebox.showerror("validation","Enter 10 digit mob no")
        elif(not email.endswith(".com")):
            messagebox.showerror("Validation","Enter Valid Mail ")
        elif(not len(pwd)==6):
            messagebox.showerror("validation","Enter 6 digit password")       
        else:
          frm.destroy()
          home_screen()
        
        con=sqlite3.connect(database="bank.sqlite")
        cur=con.cursor()
        cur.execute("update users set name=?,pass=?,email=?,mob=? where acn=?",(name,pwd,email,mob,tup[0]))
        con.commit()
        con.close()
        messagebox.showinfo("Update","Details Updated")

    lbl_name=Label(frm,text=f"Welcome{tup[1]}",font=('Arial',15,'bold'),bg='Yellow')
    lbl_name.place(relx=0.01,rely=0.01)

    lbl_pic=Label(frm,image=default_pic)
    lbl_pic.place(relx=0.01,rely=.12)

    imgs=os.listdir("images")
    
    for img in imgs:
        if(img.startswith(str(tup[0]))):
            pic=ImageTk.PhotoImage(Image.open(f"images/{img}").resize((100,80)),master=win)
            lbl_pic.configure(image=pic)
            lbl_pic.image=pic   


    lbl_name=Label(frm,text="Update Information",font=('Arial',15,'bold'),bg='Yellow')
    lbl_name.place(relx=0.4,rely=0.01)

    lbl_name=Label(frm,text="Name :",font=('Arial',10,'bold'),bg='Yellow')
    lbl_name.place(relx=0.3,rely=0.2)

    name_entry=Entry(frm,font=('Arial',10,'bold'),bd=5)
    name_entry.place(relx=.5,rely=.2)
    name_entry.insert(0,tup[1])
    
    lbl_name=Label(frm,text="Password :",font=('Arial',10,'bold'),bg='Yellow')
    lbl_name.place(relx=0.3,rely=0.3)

    pass_entry=Entry(frm,font=('Arial',10,'bold'),bd=5)
    pass_entry.place(relx=.5,rely=.3)
    pass_entry.insert(0,tup[2])

    lbl_name=Label(frm,text="Email ID :",font=('Arial',10,'bold'),bg='Yellow')
    lbl_name.place(relx=0.3,rely=0.4)

    emailid_entry=Entry(frm,font=('Arial',10,'bold'),bd=5)
    emailid_entry.place(relx=.5,rely=.4)
    emailid_entry.insert(0,tup[4])

    lbl_name=Label(frm,text="Mobil No :",font=('Arial',10,'bold'),bg='Yellow')
    lbl_name.place(relx=0.3,rely=0.5)

    mobno_entry=Entry(frm,font=('Arial',10,'bold'),bd=5)
    mobno_entry.place(relx=.5,rely=.5)
    mobno_entry.insert(0,tup[3])
    
    logout_btn=Button(frm,font=('Arial',10,'bold'),bd=5,text="Logout",bg='Yellow',command=Logout)
    logout_btn.place(relx=0.9,rely=0.01)

    back_btn=Button(frm,font=('Arial',15,'bold'),bd=5,text="back",bg='Yellow',command=back)
    back_btn.place(relx=.01,rely=.8)

    back_btn=Button(frm,font=('Arial',15,'bold'),bd=5,text="Update",bg='Yellow',command=Submit)
    back_btn.place(relx=.85,rely=.8)

home_screen()
win.mainloop()



import sqlite3
con=sqlite3.connect(database="bank.sqlite")
cur=con.cursor()
cur.execute("create table users(acn integer primary key autoincrement,name text,pass text,mob text,email text,type text,bal float)")
cur.execute("create table txn(acn integer,withdrow_amt integer,deposite_amt float,updated_bal float)")
con.commit()   
con.close()

