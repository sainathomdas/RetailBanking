from flask import Flask
from config import Config
import sqlite3
from sqlite3 import Error

app = Flask(__name__,template_folder = 'templates', static_folder= 'static')

app.config.from_object(Config)

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

db_file = 'database.db'

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

login_table = """CREATE TABLE IF NOT EXISTS logins (
	username text PRIMARY KEY,
	password text NOT NULL,
	role text NOT NULL
);"""

login_timestamps_table = """CREATE TABLE IF NOT EXISTS login_timestamp (
                                    username text NOT NULL,
                                    timestamp text NOT NULL,
                                    FOREIGN KEY (username) REFERENCES login(username)
                                );"""
                        
customer_table = """CREATE TABLE IF NOT EXISTS customer (
	cust_id integer PRIMARY KEY,
	ssnid integer NOT NULL,
	name text NOT NULL,
    age integer NOT NULL,
    address text,
    state text,
    city text,
    status text,
    last_updated text,
    message text
);"""

accounts_table = """CREATE TABLE IF NOT EXISTS accounts (
                                    acc_id integer PRIMARY KEY,
                                    cust_id integer NOT NULL,
                                    acc_type text NOT NULL,
                                    balance integer NOT NULL,
                                    message text,
                                    last_updated text,
                                    status text,
                                    FOREIGN KEY (cust_id) REFERENCES customer(cust_id)
                                );"""

transactions_table = """CREATE TABLE IF NOT EXISTS transactions (
                                    acc_id integer NOT NULL,
                                    transaction_id integer PRIMARY KEY,
                                    description text NOT NULL,
                                    date text NOT NULL,
                                    amount integer NOT NULL,
                                    FOREIGN KEY (acc_id) REFERENCES accounts(acc_id)
                                );"""

conn = create_connection(db_file)
if conn is not None:
    create_table(conn, login_table)
    create_table(conn, login_timestamps_table)
    create_table(conn, customer_table)
    create_table(conn, accounts_table)
    create_table(conn, transactions_table)
else:
    print("Error! cannot create the database connection.")

from application.routes import login_route