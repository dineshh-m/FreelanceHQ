from freelancehq import app
from freelancehq import config
from flask import render_template, request, redirect, url_for, session
from hashlib import sha1

import mysql.connector
import bcrypt

color_bg = 'bg-success'


def get_form_data(name):
    return request.form.get(name)

@app.route("/")
def home():
    if 'userid' in session:
        return render_template('home.html', logged_in=True)
    return render_template('index.html', is_logged=False)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        db = mysql.connector.connect(user='root', password='Pallavan$2', host='127.0.0.1', database='FreelanceHQ')
        
        cursor = db.cursor()

        sql = "SELECT * FROM users WHERE email=%s"
        values = (email,)
        cursor.execute(sql, values)
        user = cursor.fetchone()

        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
                session['userid'] = user[0]
                return redirect(url_for('home'))
            else:
                return "Incorrect password"
        else:
            return "User doesn't exists"




@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if(request.method == 'GET'):
        return render_template('signup.html')
    elif(request.method == 'POST'):
        firstname = get_form_data('firstname')
        lastname = get_form_data('lastname')
        email  = get_form_data('email')
        password = get_form_data('password')

        db = mysql.connector.connect(**config.db_credentials)
        cursor = db.cursor()

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        if user:
            # User already exists with that email
            db.close()
            return "User already exists"
        
        sql = "INSERT INTO users(username, email, password_hash) VALUES(%s, %s,%s)"

        # Hashing password
        # hashed_password = hashed_password = sha1(password.encode()).hexdigest()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        values = (firstname+' '+lastname, email, hashed_password)

        cursor.execute(sql, values)
        db.commit()

        session['userid'] = cursor.lastrowid
        cursor.close()
        db.close()
        return redirect(url_for('home'))
        
@app.route('/logout')
def logout():
    session.pop('userid', None)
    return redirect(url_for('home'))

@app.route("/account")
def account():
    if 'userid' in session:
        db = mysql.connector.connect(**config.db_credentials)
        cursor = db.cursor()
        sql = "SELECT * FROM users WHERE id=%s"
        values = (session.get('userid'),)
        cursor.execute(sql, values)
        user = cursor.fetchone()
        return render_template('account.html', logged_in=True, user=user)