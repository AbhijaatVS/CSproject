import mysql.connector
from maskpass import askpass
from datetime import datetime
from tabulate import tabulate
db=mysql.connector.connect(host="localhost", user="root", password="kanha", database="Banking")
cur=db.cursor()
cur2=db.cursor()
now=datetime.now()
table=[]
print("1) Login")
print("2) Create a new bank account")
print("3) Delete an existing account")
try:
    ch=int(input("What do you want to do?"))
    if ch==1:
        a=input("Enter Username")
        b=askpass(prompt="Enter Password", mask="*")
        sql="select * from Details"
        cur.execute(sql)
        for x in cur:
            if x[0]==a and x[1]==b:
                print("login success")
                print("1)Check Balance")
                print("2)Check Transaction History")
                print("3)Add money")
                print("4)Withdraw money")
                ch=int(input("what do you want to do?"))
                if ch==1:
                    print("Balance is", x[2])
                    break
                elif ch==2:
                    sql="select details.username, statements, moneydelta, statements.Balance, date_of_transaction from details,statements where details.username=statements.username and details.username=%s"
                    cur2.reset()
                    cur2.execute(sql,(a,))
                    for i in cur2:
                        table.append(i)
                    print(tabulate(table, headers=["Username", "Statements","Money added/withdrawn","Balance","Date and Time"], tablefmt='fancy_grid'))
                    break
                elif ch==3:
                    ask=int(input("How much do you want to add?"))
                    amt=x[2]+ask
                    add="Update Details set Balance=%s where username=%s"
                    cur2.reset()
                    cur2.execute(add,(amt,a))
                    cur2.reset()
                    sql="Insert into statements values(%s,%s,%s,%s,%s)"
                    ask=str(ask)
                    values=(a,"Ruppees "+ask+" was added", "+"+ask, amt, now)
                    cur2.execute(sql,values)
                    db.commit()
                    print("Money added")
                    break
                elif ch==4:
                    ask=int(input("How much do you want to withdraw?"))
                    if ask<x[2]:
                        amt=x[2]-ask
                        add="Update Details set Balance=%s where username=%s"
                        cur2.reset()
                        cur2.execute(add,(amt,a))
                        cur2.reset()
                        sql="Insert into statements values(%s,%s,%s,%s,%s)"
                        ask=str(ask)
                        values=(a,"Ruppees "+ask+" was withdrawn", "-"+ask, amt, now)
                        cur2.execute(sql,values)
                        db.commit()
                        print("Money Withdrawn")
                        break
                    else:
                        print("Insufficient Balance")
                        break
        else:
            print("Wrong Username or Password")
    elif ch==2:
        a=input("Enter New Username")
        b=askpass(prompt="Enter Password", mask="*")
        c=askpass(prompt="Re-Enter Password", mask="*")
        sql="select * from Details"
        cur.execute(sql)
        for x in cur:
            if x[0]==a:
                print("Account already exists")
                break
            else:
                if b==c:
                    mon=int(input("How much money do you want to add as the first deposit"))
                    new="INSERT into Details values(%s,%s,%s)"
                    value=(a,b,mon)
                    cur2.reset()
                    cur2.execute(new,value)
                    cur2.reset()
                    sql="Insert into statements values(%s,%s,%s,%s,%s)"
                    mon=str(mon)
                    values=(a,"Ruppees "+mon+" was added", "+"+mon, mon, now)
                    cur2.execute(sql,values)
                    db.commit()
                    print("New account created")
                    break
                else:
                    print("The passwords don't match")
                    break
    elif ch==3:
        a=input("Enter Username")
        b=askpass(prompt="Enter Password", mask="*")
        sql="select * from Details"
        cur.execute(sql)
        for x in cur:
            if x[0]==a and x[1]==b:
                sql="DELETE FROM Details WHERE username=%s"
                cur2.reset()
                cur2.execute(sql,(a,))
                cur2.reset()
                sql="DELETE FROM Statements WHERE username=%s"
                cur2.execute(sql,(a,))
                db.commit()
                print("Account Deleted")
                break
        else:
            print("Wrong Username or Password")

    else:
        print("Enter a valid option")
except:
    print("Enter a valid option")
db.close()
