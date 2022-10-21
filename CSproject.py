import mysql.connector
from maskpass import askpass
import datetime
from tabulate import tabulate
import time
db=mysql.connector.connect(host="localhost", user="root", password="kanha", database="Banking")
cur=db.cursor()
cur2=db.cursor()
now=datetime.datetime.now()
table=[]
fd=[]
var = 0
print("=======WELCOME TO HYRULE BANK=======")
print("1➔ Login")
print("2➔ Create a new bank account")
print("3➔ Delete an existing account")
time.sleep(1)
try:
    ch=int(input("What do you want to do?  "))
    if ch==1:
        a=input("Enter Username  ")
        b=askpass(prompt="Enter Password  ", mask="*")
        sql="select * from Details"
        cur.execute(sql)
        for x in cur:
            if x[0]==a and x[1]==b:
                time.sleep(1)
                print("===========LOGIN SUCCESSFUL===========")
                print("1➔ Check Balance")
                print("2➔ Check Transaction History")
                print("3➔ Add money")
                print("4➔ Withdraw money")
                print("5➔ Fixed Deposit")
                time.sleep(1)
                ch=int(input("what do you want to do?  "))
                time.sleep(1)
                if ch==1:
                    print("===========BALANCE===========")
                    print("Balance is", x[2])
                    break
                elif ch==2:
                    print("===========TRANSACTION HISTORY===========")
                    sql="select details.username, statements, moneydelta, statements.Balance, date_of_transaction from details,statements where details.username=statements.username and details.username=%s"
                    cur2.reset()
                    cur2.execute(sql,(a,))
                    for i in cur2:
                        table.append(i)
                    print(tabulate(table, headers=["Username", "Statements","Money added/withdrawn","Balance","Date and Time"], tablefmt='pretty'))
                    break
                elif ch==3:
                    print("===========MONEY DEPOSIT===========")
                    ask=int(input("How much do you want to add?  "))
                    time.sleep(1)
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
                    time.sleep(1)
                    print("Money added")
                    break
                elif ch==4:
                    print("===========MONEY WITHDRAWAL===========")
                    ask=int(input("How much do you want to withdraw?  "))
                    time.sleep(1)
                    if ask<=x[2]:
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
                        time.sleep(1)
                        print("Money Withdrawn")
                        break
                    else:
                        print("Insufficient Balance")
                        break
                elif ch==5:
                    print("===========FIXED DEPOSITS===========")
                    print("1➔ Create a Fixed Deposit")
                    print("2➔ View Status of a Fixed Deposit")
                    print("3➔ Break a Fixed Deposit")
                    time.sleep(1)
                    cho = int(input("What do you want to do?  "))
                    time.sleep(1)
                    if cho == 1:
                        #Checking if the user already has a Fixed Deposit
                        sql = "select count(username) from fixed_deposits where username=%s"
                        cur2.reset()
                        cur2.execute(sql,(a,))
                        for i in cur2:
                            if i[0] == 1:
                                print("You can have only 1 Fixed Deposit at a time")
                                break
                            elif i[0] == 0:
                                #Creating Fixed Deposit
                                print("MINIMUM DEPOSIT = 5,000")
                                print("INTEREST RATE = 3%")
                                p = float(input("Enter Principal Amount  "))
                                t = int(input("Enter the duration (In days)  "))
                                r = 3
                                #Calculating End Date and time
                                end = datetime.timedelta(days=t)
                                end_date = now+end
                                if p>=5000 and p<=x[2]:
                                    #Storing Data in the Fixed Deposits Table
                                    SI = p*r*t/100
                                    sql = "insert into fixed_deposits values(%s,%s,%s,%s,%s,NULL,NULL,%s,%s,%s)"
                                    values = (a,p,r,t,now,SI,p+SI, end_date)
                                    cur2.reset()
                                    cur2.execute(sql,values)
                                    #Updating the Existing Balance
                                    new = x[2]-p
                                    subtract="Update Details set Balance=%s where username=%s"
                                    cur2.reset()
                                    cur2.execute(subtract,(new,a))
                                    cur2.reset()
                                    #Inserting Data into Transaction History Table
                                    sql="Insert into statements values(%s,%s,%s,%s,%s)"
                                    p=str(p)
                                    values=(a,"Ruppees "+p+" was Fixed", "-"+p, new, now)
                                    cur2.execute(sql,values)
                                    db.commit()
                                    time.sleep(1)
                                    print("Fixed Deposit Created")
                                    break
                                #Checking for Minimum Deposit Value
                                elif p<5000:
                                    time.sleep(1)
                                    print("Enter At least 5000 Ruppees")
                                    break
                                #Checking if user has enough Balance
                                else:
                                    time.sleep(1)
                                    print("Insufficient Balance")
                                    break
                                break
                            break
                    elif cho == 2:
                        #Checking if the User even has a Fixed Deposit or not
                        sql = "select * from fixed_deposits"
                        cur2.reset()
                        cur2.execute(sql)
                        for i in cur2:
                            if a == i[0]:
                                sql = "select * from fixed_deposits where username=%s"
                                cur2.reset()
                                cur2.execute(sql,(a,))
                                for i in cur2:
                                    #Calculating Current Interest Rates
                                    x = i[9]-i[4]
                                    y = now - i[4]
                                    x = x.total_seconds()
                                    y = y.total_seconds()
                                    if y>x:
                                        y = x
                                    current_interest = y/x*i[7]
                                    amount_rn = i[1]+current_interest
                                    sql = "UPDATE Fixed_Deposits SET current_interest = %s, amount_withdrawable = %s where username = %s "
                                    cur2.reset()
                                    cur2.execute(sql,(current_interest, amount_rn,a))
                                    db.commit()
                                #Displaying Details Of Fixed Deposits
                                sql = "select * from fixed_deposits where username=%s"
                                cur2.reset()
                                cur2.execute(sql,(a,))
                                for i in cur2:
                                    fd.append(i)
                                time.sleep(1)
                                print(tabulate(fd, headers=["Username", "Principal Amount","Rate of Interest","Duration(Days)","Time of Initial Deposit","Current Interest","Current Returns","Interest On Maturity", "Return on Maturity", "Time of Maturity"], tablefmt='pretty'))
                                break
                        else:
                            time.sleep(1)
                            print("You don't have a Fixed Deposit")
                        break
                    elif cho == 3:
                        sql = "select * from fixed_deposits"
                        cur2.reset()
                        cur2.execute(sql)
                        for i in cur2:
                            if a in i:
                                sql = "select * from fixed_deposits where username=%s"
                                cur2.reset()
                                cur2.execute(sql,(a,))
                                for i in cur2:
                                    p = i[9]-i[4]
                                    q = now - i[4]
                                    p = p.total_seconds()
                                    q = q.total_seconds()
                                    if q>p:
                                        q = p
                                    current_interest = q/p*i[7]
                                    amount_rn = i[1]+current_interest
                                    sql = "UPDATE Fixed_Deposits SET current_interest = %s, amount_withdrawable = %s where username = %s "
                                    cur2.reset()
                                    cur2.execute(sql,(current_interest, amount_rn,a))
                                    db.commit()
                                    break
                                #Asking if they really want to break the FD
                                sql = "select * from fixed_deposits where username=%s"
                                cur2.reset()
                                cur2.execute(sql,(a,))
                                for i in cur2:
                                    time.sleep(1)
                                    print("By Breaking the Fixed Deposit, you will get an Interest of",i[5],"and your returns will be", i[6])
                                    print("Your Interest on Maturity is",i[7],"and your return on maturity will be",i[8])
                                    time.sleep(1)
                                    Q = input("Are you sure you want to Break the Fixed Deposit? (Y/N)  ")
                                    if Q.upper()=='Y':
                                        #Adding the Money to the Bank Account
                                        new=i[6]
                                        existing = float(x[2])
                                        amt = existing+new
                                        add="Update Details set Balance=%s where username=%s"
                                        cur2.reset()
                                        cur2.execute(add,(amt,a))
                                        cur2.reset()
                                        sql="Insert into statements values(%s,%s,%s,%s,%s)"
                                        new=str(new)
                                        values=(a,"Ruppees "+new+" was added from the fixed deposit", "+"+new, amt, now)
                                        cur2.execute(sql,values)
                                        #Deleting the Data from the Fixed_Deposits Table
                                        sql = "delete from fixed_deposits where username = %s"
                                        cur2.reset()
                                        cur2.execute(sql,(a,))
                                        db.commit()
                                        time.sleep(1)
                                        print("Fixed Deposit is broken,", new,"ruppees is added to your Bank Account")
                                        break
                                    else:
                                        time.sleep(1)
                                        print("Fixed Deposit not Broken")
                                        break
                                    break
                                break

                        else:
                            time.sleep(1)
                            print("You Don't Have a Fixed Deposit")



                    else:
                        time.sleep(1)
                        print("Enter a Valid Option")
                        break
                    break
                break
        else:
            time.sleep(1)
            print("Wrong Username or Password")
    elif ch==2:
        time.sleep(1)
        a=input("Enter New Username  ")
        b=askpass(prompt="Enter Password  ", mask="*")
        c=askpass(prompt="Re-Enter Password  ", mask="*")
        sql="select * from Details"
        cur.execute(sql)
        for x in cur:
            if x[0]==a:
                time.sleep(1)
                print("Account already exists")
                break
            else:
                if b==c:
                    mon=int(input("How much money do you want to add as the first deposit  "))
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
                    time.sleep(1)
                    print("New account created")
                    break
                else:
                    time.sleep(1)
                    print("The passwords don't match")
                    break
    elif ch==3:
        time.sleep(1)
        a=input("Enter Username  ")
        b=askpass(prompt="Enter Password  ", mask="*")
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
                sql="DELETE FROM Fixed_Deposits WHERE username=%s"
                cur2.execute(sql,(a,))
                db.commit()
                time.sleep(1)
                print("Account Deleted")
                break
        else:
            time.sleep(1)
            print("Wrong Username or Password")

    else:
        time.sleep(1)
        print("Enter a valid option")
except ValueError:
    time.sleep(1)
    print("Enter a valid option")
except:
    pass

db.close()
