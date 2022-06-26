try: import mysql.connector as mc
except: pass

import sqlite3 as sq
import tkinter as tk

root=tk.Tk()
root.geometry('1380x720+0+0')
root.configure(background='white')
okk=tk.PhotoImage(file='ok.png')
#back=tk.PhotoImage(file='back.png')
#backl=tk.Label(root, image=back)
#backl.grid(row=0, column=0)
###################################################
login=tk.Toplevel(root)
login.configure(background='white')
login.wm_attributes('-topmost',1)
label1=tk.Label(login, text='Enter Your Username: ')
label1.grid(row=1,column=1)
entry1=tk.Entry(login)
entry1.grid(row=1,column=2)
label2=tk.Label(login, text='Enter Your Password: ')
label2.grid(row=2,column=1)
entry2=tk.Entry(login)
entry2.grid(row=2,column=2)
label3=tk.Label(login, text="else you may use sqlite\nfor using sqlite kindly enter your database name\nexisting database in used \nwhile non existing is created")
label3.grid(row=5,column=1)
entry3=tk.Entry(login)
entry3.grid(row=5,column=2)
def ok():
    global mydb
    mydb=mc.connect(
        host='localhost',
        user=str(entry1.get()),
        passwd=str(entry2.get()),
        buffered=True
        )
    login.destroy()
button1=tk.Button(login, image=okk,relief='flat', command=ok)
button1.grid(row=4, column=2)
def forsqlit():
    global mydb
    mydb=sq.connect(entry3.get())
    login.destroy()
button2=tk.Button(login, text="sqlit", relief="flat", command=forsqlit)
button2.grid(row=6,column=2)

###################################################
root.rowconfigure(1, minsize=170, weight=0)
#--------------------------------------------------
sc=tk.Scrollbar(root)
sc.grid(row=3, column=2, sticky=tk.S+tk.N)
sc1=tk.Scrollbar(root)
sc1.grid(row=3, column=4, sticky=tk.S+tk.N)
sc3=tk.Scrollbar(root, orient=tk.HORIZONTAL)
sc3.grid(row=4, column=3, sticky=tk.E+tk.W)
#--------------------------------------------------
txt=tk.Text(root, relief='solid', height=30, width=75, wrap='word', yscrollcommand=sc.set, selectbackground='blue')
txt.grid(row=3, column=1)
txt1=tk.Text(root, relief='solid', height=30, width=75, wrap=tk.NONE, yscrollcommand=sc1.set, xscrollcommand=sc3.set, selectbackground='blue')
txt1.grid(row=3, column=3, sticky=tk.E)
sc.config(command=txt.yview)
sc1.config(command=txt1.yview)
sc3.config(command=txt1.xview)
#---------------------------------------------------------
l=tk.Label(root, text='INPUT', bg='black', fg='white')
l.grid(row=2, column=1)
l2=tk.Label(root, text='OUTPUT', bg='black', fg='white')
l2.grid(row=2, column=3)
#---------------------------------------------------------
dc=tk.Scrollbar(root)
dc.grid(row=1, column=4, sticky=tk.E+tk.W+tk.N+tk.S)
errortext=tk.Text(root, relief='groove', width=75, height=10, fg='lightgreen', bg='black', wrap='word', yscrollcommand=dc.set, selectbackground='blue')
errortext.grid(row=1,column=3)
dc.config(command=errortext.yview)
#---------------------------------------------------------
def gett():
    global mydb
    global mycurs
    global p
    a=str(txt.get('1.0', 'end-1c'))
    p=[]
    indi=0
    '''
    if " " in a:
        a=a.replace(' ','')'''
    if '\n' in a:
        a=a.replace('\n','')
    for i in range(len(a)):
        if a[i]==';':
            p+=[a[indi:i+1]]
            indi=i+1
    #print(p)
    mcurs=mydb.cursor()
    txt1.delete('1.0', tk.END)
    errortext.delete('1.0', tk.END)
    for ind in p:
        try:
            mcurs.execute(ind)
            mydb.commit()
        except Exception as e:
            errortext.insert('1.0', 'line: '+str(p.index(ind)+1)+' '+str(e)+'\n')
        mcursrev=[]
        for ze in mcurs:
            mcursrev.append(ze)
        #print(mcursrev)
        largest=0
        for q in mcursrev:
            for j in q:
                if len(str(j))-1>largest:
                        largest=len(str(j))
                        #print(largest)
        #print(mcursrev)           
        for te in mcursrev[::-1]:
            for j in te[::-1]:
                txt1.insert('1.0',str(j)+(largest-len(str(j)))*' '+'|')
            txt1.insert('1.0','\n')
        txt1.insert('1.0','\n-----------\n')

but=tk.Button(root, text='run', fg='white', bg='red', command=gett,activebackground='white', activeforeground='red')
but.grid(row=1,column=1)



root.mainloop()
mydb.close()
