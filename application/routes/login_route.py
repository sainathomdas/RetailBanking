from application import app
from flask import render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from passlib.hash import sha256_crypt
from functools import wraps
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sainath:123456@localhost/retailbanking'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
db.create_all()



@app.route('/')
@app.route('/login/',methods = ['GET', 'POST'])
def login():
    if 'logged_in' in session:
        if session['logged_in']:
            return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        login_type = request.form['login_type']
        result = db.session.query(ExecutiveAccount).filter(ExecutiveAccount.username==username)
        
        if(len(result.all())>0):
            for row in result:
                if(username == row.username and password == row.password):
                    session['logged_in'] = True
                    session['username'] = username
                    session['login_type'] = login_type
                    # flash("Successfully Logged In","success")
                    return redirect(url_for('home'))
                else:
                    flash("Wrong password!! Try Again !!",category= "warning")
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
            flash('Must be logged in to process','warning')
            return redirect(url_for('login'))
    return wrap

@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out !','success')
    return redirect(url_for('login'))
    
@app.route('/home/')
@is_logged_in
def home(login_type = None):
    return render_template('home.html', home = True)


@app.route('/create_customer/', methods = ['GET', 'POST'])
@is_logged_in
def createCustomer():
    if request.method == 'POST':
        #create customer and return accordingly
        flash('Customer created successfully', 'success')
        return render_template('create_customer.html', activate_customer_mgmt = True)
    return render_template('create_customer.html', activate_customer_mgmt = True)
    
@app.route('/update_customer/', methods = ['GET', 'POST'])
@is_logged_in
def updateCustomer():
    if request.method == "POST":
        if( 'input_type' in request.form and 'id' in request.form):
            input_type = request.form['input_type']
            id = request.form['id']
            #search for customer data with id and input_type...write a funtion to pull data from db using input_Type and id
            if 1==1: #if customer found
                return render_template('update_customer.html',search = False, data = 'sainath', activate_customer_mgmt = True)
            else:
                flash(f"Customer with {input_type} = {id} not found!", category='warning')

    return render_template('update_customer.html', search = True,  activate_customer_mgmt = True)

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
        #udpate into database
        if 1==1: #if updation is sucess
            flash("Updated Successfully", category= 'success')
            return redirect(url_for('updateCustomer'))
        else:
            flash("An unknown error occured", category= 'warning')
            return redirect(url_for('updateCustomer'))


@app.route('/delete_customer/', methods = ['GET', 'POST'])
@is_logged_in
def deleteCustomer():
    if request.method == "POST":
        if( 'input_type' in request.form and 'id' in request.form):
            input_type = request.form['input_type']
            id = request.form['id']
            #search for customer data with id and input_type...write a funtion to pull data from db using input_Type and id
            if 1==1: #if customer found
                return render_template('delete_customer.html',search = False, data = 'sainath', activate_customer_mgmt = True)
            else:
                flash(f"Customer with {input_type} = {id} not found!", category='warning')
    
    return render_template('delete_customer.html', search = True,  activate_customer_mgmt = True)



@app.route('/delete_customer_from_database', methods = ['GET', 'POST'])
@is_logged_in
def deleteCustomerFromDatabase():
    if request.method == 'POST':
        # same like updateIntoDatabase
        return redirect(url_for('deleteCustomer'))


@app.route('/view_customer/', methods = ['GET', 'POST'])
@is_logged_in
def viewCustomer():
    return render_template('view_customer.html', datatable = True,  activate_customer_mgmt = True)

@app.route('/customer_status/')
@is_logged_in
def customerStatus():
    return render_template('customer_status.html', datatable = True, activate_status_details = True)

@app.route('/customer_management')
@is_logged_in
def customerManagement():
    return render_template('customer_mgmt.html', datatable = True,  activate_customer_mgmt = True)

@app.route('/create_account/', methods = ['GET', 'POST'])
@is_logged_in
def createAccount():
    if request.method == 'POST':
        if( 'cust_id' in request.form and 'account_type' in request.form and 'deposit_amt' in request.form ):
            cust_id = request.form['cust_id']
            account_type = request.form['account_type']
            deposit_amt = request.form['deposit_amt']

            if 1==1: #if customer found
                if 1==1: # if deposit success
                    flash('Deposit Success', 'success')
                    return redirect(url_for('createAccount'), activate_account_mgmt = True)
                else:
                    flash('An unknown error occured', 'warning')
                    return redirect(url_for('createAccount'), activate_account_mgmt = True)
            else:
                flash(f'Customer with id = {cust_id} not found! ', 'warning')
                return redirect(url_for('createAccount'), activate_account_mgmt = True)
                
    return render_template('create_account.html', activate_account_mgmt = True)


@app.route('/delete_account/', methods = ['GET', 'POST'])
@is_logged_in
def deleteAccount():
    if request.method == "POST":
        if('input_type' in request.form and 'id' in request.form):
            input_type = request.form['input_type']
            id = request.form['id']
            if 1==1: #if customer found
                if 1==1: #if account found
                    return render_template('delete_account.html',search = False, data = 'sainath', activate_account_mgmt = True)
                else:
                    flash(f'Account not found for {input_type} = {id} ', 'warning')
                    return redirect(url_for('deleteAccount'), search = True, activate_account_mgmt = True)
                    
            else:
                flash(f"Customer with {input_type} = {id} not found!", category='warning')
    
    return render_template('delete_account.html', search = True,  activate_account_mgmt = True)

@app.route('/delete_account_from_database', methods = ['GET', 'POST'])
@is_logged_in
def deleteAccountFromDatabase():
    if request.method == 'POST':
        # same like updateIntoDatabase
        return redirect(url_for('deleteAccount'))


@app.route('/account_status/')
@is_logged_in
def accountStatus():
    return render_template('account_status.html', activate_status_details = True, datatable = True)

@app.route('/customer_search', methods = ['GET', 'POST'])
@is_logged_in
def customerSearch():
    if request.method == 'POST':
        if('input_type' in request.form and 'id' in request.form):
            input_type = request.form['input_type']
            id = request.form['id']
            if 1==1: # if customer found
                return render_template('customer_search.html', activate_search = True, search = False, data = 'pass data')
            else:
                flash(f'Customer with {input_type} = {id} not found! ')
                return redirect(url_for('customerSearch')) 
    return render_template('customer_search.html', activate_search = True, search = True)

@app.route('/account_search/', methods = ['GET', 'POST'])
@is_logged_in
def accountSearch():
    if request.method == 'POST':
        if('input_type' in request.form and 'id' in request.form):
            input_type = request.form['input_type']
            id = request.form['id']
            if 1==1: # if account found
                return render_template('account_search.html', activate_search = True, search = False, data = 'pass data')
            else:
                flash(f'Account with {input_type} = {id} not found! ')
                return redirect(url_for('accountSearch'))
    return render_template('account_search.html', activate_search = True, search = True)
