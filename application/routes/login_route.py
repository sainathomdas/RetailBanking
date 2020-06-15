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


@app.route('/create_customer')
def createCustomer():
    return render_template('create_customer.html', customer_mgmt = True)
    
@app.route('/update_customer/', methods = ['GET', 'POST'])
def updateCustomer(data = False):
    return render_template('update_customer.html')
            

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

@app.route('/search_customer', methods = ['GET', 'POST'])
def searchCustomer():
    if request.method == 'POST':
        input_type = request.form['input_type']
        id = request.form['id']

        if input_type and id:
            if 1==1:
                return jsonify({'name' : 'sainath'})
            else:
                return jsonify({'error' : 'Customer not found!'})



    


