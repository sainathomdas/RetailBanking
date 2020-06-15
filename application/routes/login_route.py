from application import app
from flask import render_template, request, redirect, url_for, flash, jsonify

@app.route('/')
@app.route('/login/',methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        login_type = request.form['login_type']
        
    return render_template('login.html', login_page = True)

@app.route('/create_customer/')
def createCustomer():
    return render_template('create_customer.html', customer_mgmt = True)
    
@app.route('/update_customer/', methods = ['GET', 'POST'])
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
def deleteCustomer():
    return render_template('delete_customer.html')

@app.route('/view_customer', methods = ['GET', 'POST'])
def viewCustomer():
    return render_template('view_customer.html', datatable = True, customer_mgmt = True)

@app.route('/customer_status')
def customerStatus():
    return render_template('customer_status.html', datatable = True)

@app.route('/customer_management')
def customerManagement():
    return render_template('customer_mgmt.html', datatable = True, customer_mgmt = True)



