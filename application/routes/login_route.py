from application import app
from application import conn
from flask import render_template, request, redirect, url_for, flash, session
from datetime import datetime, date
from passlib.hash import sha256_crypt
from functools import wraps
from datetime import datetime
from application.models import login as login_table
from application.models import login_timestamp as login_timestamp_table
from application.models import customer as customer_table
from application.models import accounts as accounts_table
from application.models import transactions as transactions_table

#login_table.insert_logins("""'sainath1234','S@inath123','cashier'""")

@app.route('/')
@app.route('/login',methods = ['GET', 'POST'])
def login():
    if 'logged_in' in session:
        if session['logged_in']:
            return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        login_type = request.form['login_type']
        result = login_table.read_logins(f"username='{username}' and role='{login_type}'")
        if(len(result)>0):
            for row in result:
                if(username == row[0] and password == row[1]):
                    session['logged_in'] = True
                    session['username'] = username
                    session['login_type'] = login_type
                    login_timestamp_table.insert_login_timestamp(f"'{username}','{str(datetime.now())}'")
                
                    # flash("Successfully Logged In","success")
                    return render_template('home.html', home = True)
                else:
                    flash("Wrong password!! Try Again !!",category= "warning")
                    return redirect(url_for('login'))
        else:
            flash("Invalid Username","warning")
            return redirect(url_for('login'))
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

@app.route('/logout/')
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
        ssnid = int(request.form['cust_ssid'])
        name = request.form['cust_name']
        age = request.form['cust_age']
        address = request.form['cust_address']
        state = request.form['cust_state']
        city = request.form['cust_city']
        result = customer_table.read_customer(f"ssnid={ssnid}")
        if(len(result)>0):
            flash(f"Customer with ssnid = {ssnid} already exists!",category="warning")
            return redirect(url_for('createCustomer'))

        result = customer_table.getLastRow()
        prev_cust_id = None
        for row in result:
            prev_cust_id = row[0]
        
        if prev_cust_id != None:        
            cust_id = int(prev_cust_id) + 1
        else:
            cust_id = 100000001

        customer_table.insert_customer(f"{int(cust_id)},{int(ssnid)},'{name}','{age}','{address}','{state}','{city}','Active','{str(datetime.now())}','Customer creation initiated successfully' ")

        flash('Customer created successfully', 'success')
        return render_template('create_customer.html', activate_customer_mgmt = True)
    return render_template('create_customer.html', activate_customer_mgmt = True)
    
@app.route('/update_customer/', methods = ['GET', 'POST'])
@is_logged_in
def updateCustomer():
    if request.method == "POST":
        if( 'input_type' in request.form and 'id' in request.form):
            input_type = request.form['input_type']
            id = int(request.form['id'])
            #search for customer data with id and input_type...write a funtion to pull data from db using input_Type and id
            if(input_type=='cust_id'):
                result = customer_table.read_customer(f"cust_id={id}")
                if(len(result) > 0):
                    for row in result:
                        if(id == row[0]):
                            #flash(f"Customer found!",category="success")
                            return render_template('update_customer.html',search = False, data = row, activate_customer_mgmt = True)
                else:
                    flash(f"Customer with {input_type} = {id} not found!", category='warning')
                    return render_template('update_customer.html', search = True,  activate_customer_mgmt = True)

        
            elif(input_type=='ssn_id'):
                result = customer_table.read_customer(f"ssnid={id}")
                if(len(result) > 0 ):   
                    for row in result:
                        if(id == row[1]):
                            # flash(f"Customer found!",category="success")
                            return render_template('update_customer.html',search = False, data = row, activate_customer_mgmt = True)
                else:
                    flash(f"Customer with {input_type} = {id} not found!", category='warning')
                    return render_template('update_customer.html', search = True,  activate_customer_mgmt = True)
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
        try:
            customer_table.update_customer(f"name='{cust_new_name}', age={int(cust_new_age)}, address='{cust_new_address}', city='{cust_city}', state = '{cust_state}', message='Customer update initiated successfully',last_updated='{str(datetime.now())}'" , f"ssnid={int(cust_ssid)}")
            flash("Updated Successfully", category= 'success')
            return redirect(url_for('updateCustomer'))
        except:
            flash("An unknown error occured", category= 'warning')
            return redirect(url_for('updateCustomer'))

@app.route('/delete_customer/', methods = ['GET', 'POST'])
@is_logged_in
def deleteCustomer():
    if request.method == "POST":
        flag = 0
        input_type = request.form['input_type']
        id = request.form['id']
        if(input_type=='cust_id'):
            result = customer_table.read_customer(f"cust_id={id}")
            if(len(result) > 0):
                flag = 1
                for row in result:
                    #flash("Customer Found",category="success")
                    return render_template('delete_customer.html',search = False, data = row, activate_customer_mgmt = True)
            
        elif(input_type=='ssn_id'):
            result = customer_table.read_customer(f"ssnid={id}")
            if(len(result) > 0):
                flag = 1
                for row in result:
                    #flash("Customer Found",category="success")
                    return render_template('delete_customer.html',search = False, data = row, activate_customer_mgmt = True)
        if(flag==0):
            flash(f'Customer not found with {input_type} = {id} ', 'warning')
            return render_template('delete_customer.html', search = True,  activate_customer_mgmt = True)

    return render_template('delete_customer.html', search = True,  activate_customer_mgmt = True)



@app.route('/delete_customer_from_database', methods = ['GET', 'POST'])
@is_logged_in
def deleteCustomerFromDatabase():
    if request.method == 'POST':
        custid = int(request.form['cust_id'])
        ssid = int(request.form['cust_ssid'])
        customer_table.delete_customer(f"cust_id={custid}")
        flash("Successfully Deleted !!","success")
        return redirect(url_for('deleteCustomer'))



@app.route('/view_customer/', methods = ['GET', 'POST'])
@is_logged_in
def viewCustomer():    
    if request.method=='POST':
        custid = int(request.form['custid'])
        ssnid = int(request.form['ssnid'])
        result = customer_table.read_customer(f"ssnid={ssnid}")
        if(len(result) > 0):
            flag = 1
            for row in result:
                #flash("Customer Found",category="success")
                return render_template('view_customer.html', datatable = True,  activate_customer_mgmt = True, data = row)

@app.route('/customer_status/')
@is_logged_in
def customerStatus():
    customers = customer_table.read_customer()
    return render_template('customer_status.html', datatable = True, activate_status_details = True,data=customers)

@app.route('/customer_management')
@is_logged_in
def customerManagement():
    customers = CustomerAccount.query.all()
    return render_template('customer_mgmt.html', datatable = True,  activate_customer_mgmt = True, data=customers)

@app.route('/create_account/', methods = ['GET', 'POST'])
@is_logged_in
def createAccount():
    if request.method == 'POST':
        if( 'cust_id' in request.form and 'account_type' in request.form and 'deposit_amt' in request.form ):
            cust_id = int(request.form['cust_id'])
            account_type = request.form['account_type']
            deposit_amt = int(float(request.form['deposit_amt']))
            result = accounts_table.read_accounts(f"cust_id={cust_id} and acc_type='{account_type}'")
            if(len(result)>0):
                flash(f"A {account_type} account with cust_id = {cust_id} already exists!",category="warning")
                return redirect(url_for('createAccount'))

            result = customer_table.read_customer(f"cust_id={cust_id}")
            if len(result) > 0: #if customer found
                for row in result:
                    rec = accounts_table.getLastRow()
                    prev_acc_id = None
                    for r in rec:
                        prev_acc_id = r[0]
        
                    if prev_acc_id != None:        
                        acc_id = int(prev_acc_id) + 1
                    else:
                        acc_id = 100000001
                    ans = accounts_table.insert_accounts(f"{acc_id},{cust_id},'{account_type}',{deposit_amt},'Account creation initiated successfully', '{str(datetime.now())}','active' ")
                    
                    if ans: # if deposit success
                        prev_trans_id = None
                        transIDs = transactions_table.getLastRow()
                        for t in transIDs:
                            prev_trans_id = t[1]
                        
                        if prev_trans_id == None:
                            trans_id = 100000001
                        else:
                            trans_id = prev_trans_id + 1
                        transactions_table.insert_transactions(f"{acc_id},{trans_id},'Deposit','{date.today()}',{deposit_amt} ")
                        flash('Account creation initiated successfully', 'success')
                        return redirect(url_for('createAccount'))
                    else:
                        flash('An unknown error occured', 'warning')
                        return redirect(url_for('createAccount'))
            else:
                flash(f'Customer with id = {cust_id} not found! ', 'warning')
                return redirect(url_for('createAccount'))
                
    return render_template('create_account.html', activate_account_mgmt = True)


@app.route('/delete_account/', methods = ['GET', 'POST'])
@is_logged_in
def deleteAccount():
    if request.method == "POST":
        flag = 0
        if('input_type' in request.form and 'id' in request.form):
            input_type = request.form['input_type']
            id = int(request.form['id'])
            if(input_type=='cust_id'):
                result = accounts_table.read_accounts(f"cust_id={id}")
                if(len(result) > 0):
                    flag = 1
                    # for row in result:
                        #flash("Customer Found",category="success")
                    return render_template('delete_account.html',search = False, data = result, activate_account_mgmt = True)
            
            elif(input_type=='acc_id'):
                result = accounts_table.read_accounts(f"acc_id={id}")
                if(len(result) > 0):
                    flag = 1
                    #for row in result:
                        #flash("Customer Found",category="success")
                    return render_template('delete_account.html',search = False, data = result, activate_account_mgmt = True)
            if(flag==0):
                flash(f'Account with {input_type} = {id} not found!!', 'warning')
                return redirect(url_for('deleteAccount'))
    
    return render_template('delete_account.html', search = True,  activate_account_mgmt = True)

@app.route('/delete_account_from_database', methods = ['GET', 'POST'])
@is_logged_in
def deleteAccountFromDatabase():
    if request.method == 'POST':
        custid = int(request.form['cust_id'])
        acc_id = int(request.form['account_id'])
        accounts_table.delete_accounts(f"acc_id={acc_id}")
        flash("Successfully Deleted !!","success")
        return redirect(url_for('deleteAccount'))


@app.route('/account_status/')
@is_logged_in
def accountStatus():
    accounts = accounts_table.read_accounts()
    return render_template('account_status.html', activate_status_details = True, datatable = True, data = accounts)

@app.route('/customer_search', methods = ['GET', 'POST'])
@is_logged_in
def customerSearch():
    if request.method == "POST":
        if( 'input_type' in request.form and 'id' in request.form):
            input_type = request.form['input_type']
            id = int(request.form['id'])
            #search for customer data with id and input_type...write a funtion to pull data from db using input_Type and id
            if(input_type=='cust_id'):
                result = customer_table.read_customer(f"cust_id={id}")
                if(len(result) > 0):
                    for row in result:
                        if(id == row[0]):
                            #flash(f"Customer found!",category="success")
                            return render_template('customer_search.html',search = False, data = row, activate_search = True)
                else:
                    flash(f"Customer with {input_type} = {id} not found!", category='warning')
                    return render_template('customer_search.html', search = True,  activate_search = True)
        
            elif(input_type=='ssn_id'):
                result = customer_table.read_customer(f"ssnid={id}")
                if(len(result) > 0):
                    for row in result:
                        if(id == row[1]):
                            #flash(f"Customer found!",category="success")
                            return render_template('customer_search.html',search = False, data = row, activate_search = True)
                else:
                    flash(f"Customer with {input_type} = {id} not found!", category='warning')
                    return render_template('customer_search.html', search = True,  activate_search = True)
    return render_template('customer_search.html', search = True,  activate_search = True)

@app.route('/account_search/', methods = ['GET', 'POST'])
@is_logged_in
def accountSearch():
    if request.method == 'POST':
        if('input_type' in request.form and 'id' in request.form):
            input_type = request.form['input_type']
            id = int(request.form['id'])
            if(input_type=='cust_id'):
                result = accounts_table.read_accounts(f"cust_id={id}")
                if(len(result) > 0):
                    # for row in result:
                    #     if(id == row[0]):
                    #         #flash(f"Customer found!",category="success")
                    return render_template('account_search.html',search = False, data = result, activate_search = True)
                else:
                    flash(f"Account with {input_type} = {id} not found!", category='warning')
                    return render_template('account_search.html', search = True,  activate_search = True)
        
            elif(input_type=='acc_id'):
                result = accounts_table.read_accounts(f"acc_id={id}")
                if(len(result) > 0):
                    # for row in result:
                    #     if(id == row[0]):
                            #flash(f"Customer found!",category="success")
                    return render_template('account_search.html',search = False, data = result, activate_search = True)
                else:
                    flash(f"Account with {input_type} = {id} not found!", category='warning')
                    return render_template('account_search.html', search = True,  activate_search = True)
    return render_template('account_search.html', activate_search = True, search = True)

@app.route('/account_details/')
@is_logged_in
def accountDetails():
    accounts = accounts_table.read_accounts()
    return render_template('account_details.html', activate_account_details = True, datatable = True, data = accounts)

@app.route('/deposit/', methods = ['GET', 'POST'])
@app.route('/deposit/<acc_id>', methods = ['GET', 'POST'])
@is_logged_in
def deposit(acc_id=None):
    if request.method == 'POST':
        if('account_id' in request.form and 'account_type' in request.form and 'deposit_amt' in request.form and 'balance' in request.form):
            account_id = request.form['account_id']
            account_type = request.form['account_type']
            balance = request.form['balance']
            deposit_amt = request.form['deposit_amt']
            new_balance = int(float(balance)) + int(float(deposit_amt))
            #update the DB
            if 1==1: #deposited successfully
                flash('Amount deposited successfully', 'success')
                return redirect(url_for('accountDetails'))
            else:
                flash('An unknown error occured', 'warning')
                return redirect(url_for('accountDetails'))

    else:
        if acc_id != None:
            #retrieve account details
            return render_template('deposit.html', activate_account_details = True, data = {'acc_id':'123456789', 'name':'sainath', 'balance': 2000} )
        else:
            flash('Please select an account', 'warning')
            return redirect(url_for('accountDetails'))

@app.route('/withdraw/', methods = ['GET', 'POST'])
@app.route('/withdraw/<acc_id>', methods = ['GET', 'POST'])
@is_logged_in
def withdraw(acc_id = None):
    if request.method == 'POST':
        if('account_id' in request.form and 'account_type' in request.form and 'withdraw_amt' in request.form and 'balance' in request.form):
            account_id = request.form['account_id']
            account_type = request.form['account_type']
            balance = request.form['balance']
            withdraw_amt = request.form['withdraw_amt']
            new_balance = int(float(balance)) - int(float(withdraw_amt))
            print(new_balance)
            if(new_balance < 0):
                flash('Withdraw not allowed, please choose smaller amount', 'warning')
                return redirect(url_for('withdraw', acc_id = account_id))

            #update the DB
            if 1==1: #withdrawn successfully
                flash('Amount withdrawn successfully', 'success')
                return redirect(url_for('accountDetails'))
            else:
                flash('An unknown error occured', 'warning')
                return redirect(url_for('accountDetails'))

    else:
        if acc_id != None:
            #retrieve account details
            return render_template('withdraw.html', activate_account_details = True, data = {'acc_id':'123456789', 'name':'sainath', 'balance': 100})
        else:
            flash('Please select an account', 'warning')
            return redirect(url_for('accountDetails'))
        
@app.route('/transfer/', methods = ['GET', 'POST'])
@app.route('/transfer/<acc_id>', methods = ['GET', 'POST'])
@is_logged_in
def transfer(acc_id=None):
    if request.method == 'POST':
        if('source_account_id' in request.form and 'src_account_type' in request.form and 'target_account_id' in request.form and 'transfer_amt' in request.form and 'balance' in request.form and 'target_account_type' in request.form):
            source_account_id = request.form['source_account_id']
            src_account_type = request.form['src_account_type']
            target_account_id = request.form['target_account_id']
            target_account_type = request.form['target_account_type']
            balance = request.form['balance']
            transfer_amt = request.form['transfer_amt']
            new_balance = int(float(balance)) - int(float(transfer_amt))
            print(new_balance)
            if(new_balance < 0):
                flash('Transfer not allowed, please choose smaller amount', 'warning')
                return redirect(url_for('transfer', acc_id = source_account_id))

            #update the DB
            if 1==1: #withdrawn successfully
                flash('Amount transferred successfully', 'success')
                return redirect(url_for('accountDetails'))
            else:
                flash('An unknown error occured', 'warning')
                return redirect(url_for('accountDetails'))

    else:
        if acc_id != None:
            #retrieve account details
            return render_template('transfer.html', activate_account_details = True, data = {'acc_id':'123456789', 'name':'sainath', 'balance': 100})
        else:
            flash('Please select an account', 'warning')
            return redirect(url_for('accountDetails'))



@app.route('/account_statement', methods = ['GET', 'POST'])
@is_logged_in
def accountStatement():
    if request.method == 'POST':
        if('account_id' in request.form and 'statement_type' in request.form):
            account_id = request.form['account_id']            
            if request.form['statement_type'] == 'transactions':
                num_of_transactions = request.form['num_of_transactions']
                # get last number of transactions
                return render_template('account_stmt.html', activate_account_stmt = True, datatable_for_stmt = True, data = {'name':'sainath'})
            else:
                start_date = request.form['start_date'] 
                end_date = request.form['end_date'] 
                # get statement btween these dates
                return render_template('account_stmt.html', activate_account_stmt = True, datatable_for_stmt = True, data = {'name':'sainath'})

    return render_template('account_stmt.html', activate_account_stmt = True, input = True)

