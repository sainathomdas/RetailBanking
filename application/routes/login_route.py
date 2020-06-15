from application import app
from flask import render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from passlib.hash import sha256_crypt
from functools import wraps

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
db = SQLAlchemy(app)

# Table for customer executive account
class ExecutiveAccount(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100),nullable=False)
    password = db.Column(db.String(20),nullable=False)
    timestamp = db.Column(db.DateTime,nullable=False,default = datetime.utcnow)

    def __repr__(self):
        return 'Executive : ' + str(self.id)

# password = sha256_crypt.encrypt(passwd)
# if(sha256_crypt.verify(password_candidate,password))

@app.route('/')
def base_page():
    return '<h3>welcome to root page</h3><br><a href="/login">GO TO LOGIN</a>'

@app.route('/login/',methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form['username']
        password_candidate = request.form['password']
        if(len(user_name) < 8 ):
            flash("Username must contain a minimum of 8 characters", "warning")
            return redirect(url_for('login'))
        if(len(password_candidate) < 8):
            flash("Password must contain a minimum of 10 characters", "warning")
            return redirect(url_for('login'))
        
        result = db.session.query(ExecutiveAccount).filter(ExecutiveAccount.username==user_name)
        
        if(len(result.all())>0):
            for row in result:
                if(user_name == row.username and password_candidate == row.password):
                    session['logged_in'] = True
                    session['username'] = user_name
                    flash("Successfully Logged In","success")
                    return render_template('create_customer.html')
                else:
                    flash("Wrong password!! Try Again !!","warning")
                    return render_template('login.html', login_page = True)
        else:
            flash("Invalid Username","warning")
            return render_template('login.html', login_page = True)


    return render_template('login.html', login_page = True)

# Declaring a decorator to check if user is logged in (Authorization)
def is_logged_in(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args,*kwargs)
        else:
            flash('Unauthorized to access this page','warning')
            return redirect(url_for('login'))
    return wrap


@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out !','success')
    return render_template('login.html')


@app.route('/create_customer')
@is_logged_in
def createCustomer():
    return render_template('create_customer.html')
    

@app.route('/update_customer')
@is_logged_in
def updateCustomer():
    return render_template('update_customer.html')


@app.route('/delete_customer')
@is_logged_in
def deleteCustomer():
    return render_template('delete_customer.html')


"""
cd ~
source webflask/bin/activate
cd Documents/Flask\ Apps/RetailBanking
python app.py
"""