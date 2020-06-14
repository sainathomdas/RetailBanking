from application import app
from flask import render_template, request, redirect, url_for, flash

#@app.route('/')
@app.route('/login/',methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if(len(username) < 8 ):
            flash("Username must contain a minimum of 8 characters", "warning")
            return redirect(url_for('login'))
        if(len(password) < 8):
            flash("Password must contain a minimum of 10 characters", "warning")
            return redirect(url_for('login'))
    return render_template('login.html', login_page = True)


@app.route('/create_customer')
def createCustomer():
    return render_template('create_customer.html')