from application import app
from flask import render_template, request, redirect, url_for, flash

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
    if 'data' in request.args:
        data = request.args['data']
        data = eval(data)
    return render_template('update_customer.html', data = data)
            

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
        if(request.form['input_type'] and request.form['id'] and request.form['redirect_url']):
            input_type = request.form['input_type']
            id = request.form['id']
            from_page = request.form['from_page']
            redirect_url = request.form['redirect_url']
            if 1==1:
                #if customer found pull data from DB and return
                return redirect(url_for(redirect_url, data = {'name':'sainath', 'age': 21}),code=307)
            else:
                flash(f"Customer with {input_type} = {id} not found", category= 'warning')
                return redirect(url_for(redirect_url))
    


