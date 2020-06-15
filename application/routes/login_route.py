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
@app.route('/login/',methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        login_type = request.form['login_type']
        
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



@app.route('/create_customer/')
@is_logged_in
def createCustomer():
    return render_template('create_customer.html', customer_mgmt = True)
    
@app.route('/update_customer/', methods = ['GET', 'POST'])
@is_logged_in
def updateCustomer():
    if request.method == "POST":
        if(request.form['input_type'] and request.form['id']):
            input_type = request.form['input_type']
            id = request.form['id']
            #search for customer data with id and input_type
            if 1==1: #if customer found
                return render_template('update_customer.html',search = False, data = 'sainath')
            else:
                flash(f"Customer with {input_type} = {id} not found!", category='warning')

    return render_template('update_customer.html', search = True)

@app.route('/update_into_database', methods = ['GET', 'POST'])
@is_logged_in
def updateIntoDatabase():
    if request.method == 'POST':
        cust_ssid = request.form['cust_ssid']
        cust_id = request.form['cust_id']
        cust_old_name = request.form['cust_old_name']
        cust_new_name = request.form['cust_new_name']
        cust_old_age = request.form['cust_old_age']
        cust_new_age = request.form['cust_new_age']
        cust_new_address = request.form['cust_new_address']
        cust_state = request.form['cust_state']
        cust_city = request.form['cust_city']


@app.route('/delete_customer/', methods = ['GET', 'POST'])
@is_logged_in
def deleteCustomer():
    return render_template('delete_customer.html')

@app.route('/view_customer', methods = ['GET', 'POST'])
@is_logged_in
def viewCustomer():
    return render_template('view_customer.html', datatable = True, customer_mgmt = True)

@app.route('/customer_status')
@is_logged_in
def customerStatus():
    return render_template('customer_status.html', datatable = True)

@app.route('/customer_management')
@is_logged_in
def customerManagement():
    return render_template('customer_mgmt.html', datatable = True, customer_mgmt = True)



