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
    

def insert_login_timestamp(values):
    conn = create_conn()
    cur = conn.cursor()
    sql = "insert into login_timestamp(username, timestamp) values({});".format(values);
    
    try:
        cur.execute(sql)
    except:
        return False
    conn.commit()
    conn.close()
    

def read_login_timestamp(condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "select * from login_timestamp where {};".format(condition)
    
    try:
        cur.execute(sql)
    except:
        return False
    rows = cur.fetchall()
    
    conn.commit()
    conn.close()
    return rows
    

def update_login_timestamp(values, condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "update login_timestamp set {} where {};".format(values, condition)
    
    try:
        cur.execute(sql)
    except:
        return False
    conn.commit()
    conn.close()
    

def delete_login_timestamp(condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "delete from  login_timestamp  where {};".format(condition)
    try:
        cur.execute(sql)
    except:
        return False
    conn.commit()
    conn.close()
