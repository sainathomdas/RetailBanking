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

def insert_transactions(values):
    
    conn = create_conn()
    cur = conn.cursor()
    sql = "insert into transactions(acc_id, transaction_id,description,date,amount) values({});".format(values);

    try:
        cur.execute(sql)
    except:
        return False
    conn.commit()
    conn.close()
    return True
    

def read_transactions(condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "select * from transactions where {};".format(condition)
  
    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    rows = cur.fetchall()
    data_dictionary = {}
    indices = 0
    for row in rows:
        data_dictionary[indices] = list(row)
        indices += 1
    conn.commit()
    conn.close()
    return data_dictionary
    

def update_transactions(values, condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "update transactions set {} where {};".format(values, condition)
    
    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    conn.commit()
    conn.close()
    

def delete_transactions(condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "delete from  transactions  where {};".format(condition)
   
    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    conn.commit()
    conn.close()


def getLastRow():
    conn = create_conn()
    cur = conn.cursor()
    sql = "SELECT * FROM transactions ORDER BY transaction_id DESC LIMIT 1;"    
    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    rows = cur.fetchall()    
    conn.commit()
    conn.close()
    return rows
    