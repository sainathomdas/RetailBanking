import sqlite3
from sqlite3 import Error
def create_conn():
    conn = None
    try:
        conn = sqlite3.connect('database.db')
        return conn
    except Error as e:
        print(e)
    return conn
    

def insert_accounts(values):
    conn = create_conn()
    cur = conn.cursor()
    sql = "insert into accounts(acc_id, cust_id,acc_type,balance,message,last_updated,status) values({});".format(values);
    
    try:
        cur.execute(sql)
    except:
        return False
    conn.commit()
    conn.close()
    return True
    

def read_accounts(condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "select * from accounts where {};".format(condition)
    print(sql)
    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    rows = cur.fetchall()
    
    conn.commit()
    conn.close()
    return rows
    

def update_accounts(values, condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "update accounts set {} where {};".format(values, condition)
    
    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    conn.commit()
    conn.close()
    

def delete_accounts(condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "delete from  accounts  where {};".format(condition)
    
    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    conn.commit()
    conn.close()

def getLastRow():
    conn = create_conn()
    cur = conn.cursor()
    sql = "SELECT * FROM accounts ORDER BY acc_id DESC LIMIT 1;"    
    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    rows = cur.fetchall()    
    conn.commit()
    conn.close()
    return rows