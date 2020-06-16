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

def insert_customer(values):
    print(values)
    conn = create_conn()
    cur = conn.cursor()
    sql = "insert into customer(cust_id, ssnid,name,age,address,state,city,status,last_updated,message) values({});".format(values);
    
    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    conn.commit()
    conn.close()
    

def read_customer(condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "select * from customer where {};".format(condition)
    print(sql)
    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    rows = cur.fetchall()
    
    conn.commit()
    conn.close()
    return rows
    

def update_customer(values, condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "update customer set {} where {};".format(values, condition)
    
    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    conn.commit()
    conn.close()
    

def delete_customer(condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "delete from  customer  where {};".format(condition)
    print(sql)
    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    conn.commit()
    conn.close()

def getLastRow():
    conn = create_conn()
    cur = conn.cursor()
    sql = "SELECT * FROM customer ORDER BY cust_id DESC LIMIT 1;"    
    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    rows = cur.fetchall()    
    conn.commit()
    conn.close()
    return rows
    
