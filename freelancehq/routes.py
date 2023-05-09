from freelancehq import app
from freelancehq import config
from flask import render_template, request, redirect, url_for, session
from hashlib import sha1
from freelancehq import db
from freelancehq.model import User, Profile

import mysql.connector
import bcrypt

color_bg = 'bg-success'
print(config.db_credentials, "Heap")

def get_user_by_id(userid):
    cnx = db.DBConnection()
    sql = "SELECT * FROM users WHERE id=%s"
    values = (userid,)
    cnx.execute(sql, values)
    user = cnx.cursor.fetchone()
    cnx.close_cnx()
    if user == []:
        return None
    return user

def get_form_data(name):
    return request.form.get(name)

def is_user_profile_set():
    cnx = db.DBConnection()
    sql = "SELECT COUNT(*) FROM profiles WHERE user_id=%s;"
    user_id = session.get('userid')
    values=(user_id,)
    cnx.execute(sql, values)
    user_count = cnx.cursor.fetchone()
    cnx.close_cnx()
    if(user_count[0] == 0):
        return False
    return True

@app.route("/")
def home():
    if 'userid' in session:
        if(not is_user_profile_set()):
            user = get_user_by_id(session.get('userid'))
            user_model = User(user)
            return redirect(url_for('profile_setup', userid=user_model.userid, firstname = user_model.firstname, lastname=user_model.lastname))
        return render_template('home.html', logged_in=True)
    return render_template('index.html', is_logged=False)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        db = mysql.connector.connect(**config.db_credentials)
        
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
        
        sql = "INSERT INTO users(firstname, lastname, username, email, password_hash) VALUES(%s, %s, %s, %s,%s)"

        # Hashing password
        # hashed_password = hashed_password = sha1(password.encode()).hexdigest()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        values = (firstname, lastname, firstname+' '+lastname, email, hashed_password)

        cursor.execute(sql, values)
        db.commit()
        userid = cursor.lastrowid
        session['userid'] = userid
        session['profile'] = False
        cursor.close()
        db.close()
        return redirect(url_for('profile_setup', userid=userid, firstname=firstname, lastname=lastname))
        
@app.route('/logout')
def logout():
    session.pop('userid', None)
    return redirect(url_for('home'))

@app.route("/account")
def account():
    if 'userid' in session:
        cnx = mysql.connector.connect(**config.db_credentials)
        cursor = cnx.cursor()
        sql = "SELECT * FROM users WHERE id=%s"
        userid = session.get('userid')
        values = (userid,)
        cursor.execute(sql, values)
        user = cursor.fetchone()
        cursor.close()
        cnx.close()
        user_model = User(user)
        sql = "SELECT * FROM profiles where user_id=%s"
        values = (userid,)
        cnx = db.DBConnection()
        cnx.execute(sql, values)
        profile = cnx.cursor.fetchone()
        user_profile = Profile(profile)
        cnx.close_cnx()

        return render_template('account.html', logged_in=True, user=user_model, user_profile=user_profile)
    
@app.route("/profile_setup", methods=['POST', 'GET'])
def profile_setup():
    if request.method == 'POST':
        userid = request.args.get('userid')
        firstname = get_form_data('firstname')
        lastname = get_form_data('lastname')
        summary = get_form_data('summary')
        gender = get_form_data('gender')
        dob = get_form_data('dob')
        jobrole = get_form_data('jobrole')
        living_area = f"{get_form_data('state')}, {get_form_data('country')}"
        
        str_f = ""
        sql = "INSERT INTO profiles(user_id, first_name, last_name, summary, gender, dob, jobrole, living_area) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (userid, firstname, lastname, summary, gender, dob, jobrole, living_area)
        cnx = db.DBConnection()
        cnx.execute(sql, values)

        cnx.cnx.commit()
        cnx.close_cnx()
      
        # str_f = f" {request.args.get('userid')} {get_form_data('email')} {get_form_data('firstname')} {get_form_data('lastname')} {get_form_data('gender')} {get_form_data('country')} {get_form_data('state')} {get_form_data('dob')}"
        return redirect(url_for('home'))
    db_con = db.DBConnection()
    user_id = request.args.get('userid')
    firstname = request.args.get('firstname')
    lastname = request.args.get('lastname')
    sql = "SELECT * FROM users WHERE id=%s"
    values = (user_id,)
    db_con.execute(sql, values)
    user = db_con.cursor.fetchone()
    user_model = User(user)
    print("@routes<-------------------->",user, "<--------------------------------->")
    db_con.close_cnx()
    return render_template('user_profile.html', user=user_model)