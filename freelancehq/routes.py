from freelancehq import app
from freelancehq import config
from flask import render_template, request, redirect, url_for, session
from hashlib import sha1
from freelancehq import db
from freelancehq.model import User, Profile
from freelancehq import model

import mysql.connector
import bcrypt

color_bg = 'bg-success'
print(config.db_credentials, "Heap")

# Helper functions

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

def get_user_model_by_id(userid):
    cnx = db.DBConnection()
    sql = "SELECT * FROM users WHERE id=%s"
    values = (userid,)
    cnx.execute(sql, values)
    user = cnx.cursor.fetchone()
    cnx.close_cnx()
    if user == []:
        return None
    return model.User(user)

def get_profile_model_by_userid(userid):
    cnx = db.DBConnection()
    sql = "SELECT * FROM profiles WHERE user_id=%s"
    values = (userid, )
    cnx.execute(sql, values)
    profile = cnx.cursor.fetchone()
    cnx.close_cnx()
    if profile == []:
        return None
    return model.Profile(profile)

def get_user_skills_model_by_userid(userid, cnx):
    sql = "SELECT * FROM freelancer_skills WHERE freelancer_id=%s"
    values = (userid,)
    cnx.execute(sql, values)
    skills = cnx.cursor.fetchall()
    user_skills = model.UserSkills(userid, skills)
    return user_skills

def get_user_posts_by_user_id(userid, cnx):
     # User projects
    sql = "SELECT * FROM projects WHERE client_id=%s ORDER BY created_at DESC"
    values = (userid,)
    cnx.execute(sql, values)
    project_posts = cnx.cursor.fetchall()
       
    posts = []
    for post in project_posts:
         posts.append(model.ProjectPost(post, cnx))

    return posts 

def get_post_by_id(project_id, cnx):
    sql = "SELECT * FROM projects WHERE id=%s"
    values = (project_id, )
    cnx.execute(sql, values)

    post = cnx.cursor.fetchone()

    return post


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

def is_user_logged():
    userid = session.get('userid')

    if userid == None:
        return False
    else:
        return True
    
def is_user_proposed(userid, projectid):
    cnx = db.DBConnection()
    applied = False

    sql = "SELECT * FROM projects WHERE freelancer_id=%s AND project_id=%s"
    values = (userid, projectid)
    cnx.execute(sql, values)

    if cnx.cursor.fetchone():
        applied = True

    cnx.close_cnx()
    return applied
        

# Routes

@app.route("/")
def home():
    if 'userid' in session:
        if(not is_user_profile_set()):
            user = get_user_by_id(session.get('userid'))
            user_model = User(user)
            return redirect(url_for('profile_setup', userid=user_model.userid, firstname = user_model.firstname, lastname=user_model.lastname))
        cnx = db.DBConnection()

        sql = "SELECT * FROM projects ORDER BY created_at DESC LIMIT %s"
        max_post_len = 10
        values = (max_post_len, )
        cnx.execute(sql, values)
        posts_result_set = cnx.cursor.fetchmany(10)

        posts = []
        for post in posts_result_set:
            posts.append(model.ProjectPost(post, cnx))

        # Fetching notifications
        logged_user_id = session.get('userid')
        sql = "SELECT * FROM (SELECT id as user_proj_id, client_id, title FROM projects WHERE client_id=%s and finished=%s) as user_prj JOIN proposals as prp ON user_prj.user_proj_id=prp.project_id"
        values = (logged_user_id, False)
        cnx.execute(sql, values)
        result_set = cnx.cursor.fetchall()
        print("Result set", result_set)
        notifications = []
        ntfn_len = 0

        for notification in result_set:
            notifications.append(model.Notification(notification))
            ntfn_len += 1

        # Fetching workspace data
        
        # Personal Workspace
        sql = "SELECT * FROM (SELECT id AS prj_id FROM projects WHERE client_id=%s) AS log_user_prj JOIN workspace AS wspce ON log_user_prj.prj_id=wspce.project_id"
        values = (logged_user_id, )
        cnx.execute(sql, values)
        result_set = cnx.cursor.fetchall()
        personal_workspaces = []

        for workspace in result_set:
            personal_workspaces.append(model.PersonalWorkspace(workspace))

        # Client Workspace
        sql = "SELECT * FROM workspace WHERE freelancer_id=%s"
        values = (logged_user_id, )
        cnx.execute(sql, values)
        result_set = cnx.cursor.fetchall()
        client_workspaces = []

        for c_workpace in result_set:
            client_workspaces.append(model.ClientWorkspace(c_workpace))

        cnx.close_cnx()
        return render_template('home.html', logged_in=True, posts=posts, get_user_model_by_id=get_user_model_by_id, get_profile_model_by_userid=get_profile_model_by_userid, logged_userid=session.get('userid'), notifications=notifications, ntfn_len=ntfn_len, personal_workspaces=personal_workspaces, client_workspaces=client_workspaces)
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
            return render_template('login.html', flashed=["User doesn't exist, Please check your credentials and try again."])




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
        cnx = db.DBConnection()
        cursor = cnx.cursor

        # User data
        sql = "SELECT * FROM users WHERE id=%s"
        userid = session.get('userid')
        values = (userid,)
        cursor.execute(sql, values)
        user = cursor.fetchone()
        user_model = User(user)

        # User profile data
        sql = "SELECT * FROM profiles where user_id=%s"
        values = (userid,)
        cnx.execute(sql, values)
        profile = cnx.cursor.fetchone()
        user_profile = Profile(profile)

        # Skills data
        sql = "SELECT * FROM freelancer_skills WHERE freelancer_id=%s"
        values = (userid,)
        cnx.execute(sql, values)
        skills = cursor.fetchall()
        user_skills = model.UserSkills(userid, skills)

        # User projects
        sql = "SELECT * FROM projects WHERE client_id=%s ORDER BY created_at DESC"
        values = (userid,)
        cnx.execute(sql, values)
        project_posts = cnx.cursor.fetchall()
       
        posts = []
        for post in project_posts:
            # p = model.ProjectPost(post)
            # nested_sql = "SELECT name FROM (SELECT * FROM project_skills WHERE project_id=%s) as p_skills join skills as sk on p_skills.project_skill_id=sk.id"
            # values = (p.id, )
            # cnx.execute(nested_sql, values)
            # project_skills = cnx.cursor.fetchall()
            # p
            posts.append(model.ProjectPost(post, cnx))       

        # Closing DB connection
        cnx.close_cnx()

        return render_template('account.html', logged_in=True, user=user_model, user_profile=user_profile, user_skills=user_skills, posts=posts)
    
@app.route("/profile_setup", methods=['POST', 'GET'])
def profile_setup():
    # If POST request
    if request.method == 'POST':
        userid = request.args.get('userid')
        firstname = get_form_data('firstname')
        lastname = get_form_data('lastname')
        summary = get_form_data('summary')
        gender = get_form_data('gender')
        dob = get_form_data('dob')
        jobrole = get_form_data('jobrole')
        living_area = f"{get_form_data('state')}, {get_form_data('country')}"
        skills = request.form.getlist('nested-values[]')
        
        str_f = ""
        # Inserting User profile data
        sql = "INSERT INTO profiles(user_id, first_name, last_name, summary, gender, dob, jobrole, living_area) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (userid, firstname, lastname, summary, gender, dob, jobrole, living_area)
        cnx = db.DBConnection()
        cnx.execute(sql, values)

        # Inserting user skills
        sql = "INSERT INTO freelancer_skills(freelancer_id, skill_id) VALUES(%s, %s)"
        for skill in skills:
            values = (userid, skill)
            cnx.execute(sql, values)

        cnx.cnx.commit()
        cnx.close_cnx()
      
        str_f = f" {request.args.get('userid')} {get_form_data('email')} {get_form_data('firstname')} {get_form_data('lastname')} {get_form_data('gender')} {get_form_data('country')} {get_form_data('state')} {get_form_data('dob')}"
        return redirect(url_for('home'))
    
    # If GET request
    db_con = db.DBConnection()
    user_id = request.args.get('userid')
    firstname = request.args.get('firstname')
    lastname = request.args.get('lastname')
    sql = "SELECT * FROM users WHERE id=%s"
    values = (user_id,)
    db_con.execute(sql, values)
    user = db_con.cursor.fetchone()
    user_model = User(user)

    db_con.close_cnx()
    return render_template('user_profile.html', user=user_model)



# For job
@app.route("/post/new/", methods=['GET', 'POST'])
def newjob():
    if request.method == 'POST':
        userid = session.get('userid')
        cnx = db.DBConnection()
        cursor = cnx.cursor

        title = get_form_data('title')
        description = get_form_data('description')
        budget = get_form_data('budget')
        currency = get_form_data('currency')
        deadline = get_form_data('deadline')
        skills = request.form.getlist('nested-values[]')

        # Project data
        sql = "INSERT INTO projects(client_id, title, description, budget, currency, deadline) VALUES(%s, %s, %s, %s, %s, %s)"
        values = (userid, title, description, budget, currency, deadline)
        cnx.execute(sql, values)
        project_id = cnx.cursor.lastrowid

        cnx.cnx.commit()
      

        # Skills for the project
        sql = "INSERT INTO project_skills(project_id, project_skill_id) VALUES(%s, %s)"
        for skill in skills:
            values = (project_id, int(skill))
            cnx.execute(sql, values)

        
        cnx.cnx.commit()
        cnx.close_cnx()
        return redirect(url_for('account'))
    return render_template('newjob.html')


@app.route("/user/profile/<int:userid>")
def user_profile(userid):
    cnx = db.DBConnection()
    logged_user_id = session.get('userid')
    if logged_user_id == None:
        return "Login required"
    user_itself = False

    if logged_user_id == userid:
        user_itself = True

    user_model = get_user_model_by_id(userid)
    user_profile = get_profile_model_by_userid(userid)
    user_skills = get_user_skills_model_by_userid(userid, cnx)
    posts = get_user_posts_by_user_id(userid, cnx)

    cnx.close_cnx()

    return render_template('profile.html', user_itself=user_itself, logged_in=user_itself, user=user_model, user_profile=user_profile, user_skills=user_skills, posts=posts)

@app.route("/personal/workspace/<int:personal_workspace_id>")
def personal_workspace(personal_workspace_id):

    logged_user_id = session.get('userid')
    
    sql = "SELECT * FROM workspace where id=%s"
    values = (personal_workspace_id, )
    cnx = db.DBConnection()

    cnx.execute(sql, values)
    result_set = cnx.cursor.fetchone()

    workspace = model.Workspace(result_set)

    sql = "SELECT * FROM messages WHERE workspace_id=%s"
    values = ( personal_workspace_id, )
    cnx.execute(sql, values)

    result_set = cnx.cursor.fetchall()
    messages = []

    for message in result_set:
        messages.append(model.Message(message))
    print("messages", result_set)
    cnx.close_cnx()
    return render_template('workspace.html', workspace=workspace, logged_user_id=logged_user_id, messages=messages)

@app.route("/client/workspace/<int:client_workspace_id>")
def client_workspace(client_workspace_id):
    logged_user_id = session.get('userid')

    sql = "SELECT * FROM workspace where id=%s"
    values = (client_workspace_id, )
    cnx = db.DBConnection()

    cnx.execute(sql, values)
    result_set = cnx.cursor.fetchone()
    workspace = model.Workspace(result_set)

    sql = "SELECT * FROM messages WHERE workspace_id=%s"
    values = (client_workspace_id, )
    cnx.execute(sql, values)

    result_set = cnx.cursor.fetchall()
    messages = []

    for message in result_set:
        messages.append(model.Message(message))

    cnx.close_cnx()
    return render_template('workspace.html', workspace=workspace, logged_user_id=logged_user_id ,messages=messages)

@app.route("/delete_workspace", methods=['POST'])
def delete_workspace():
    workspace_id = request.form.get('workspace-id')
    proposal_id = request.form.get('proposal-id')
    print("WorkspaceID", workspace_id, "ProposalID", proposal_id)
    cnx = db.DBConnection()

    # Deleting chat messages
    sql = "DELETE FROM messages WHERE workspace_id=%s"
    values = (workspace_id, )

    cnx.execute(sql, values)

    # Deleting the workspace
    sql = "DELETE FROM workspace WHERE id=%s"
    values = (workspace_id, )

    cnx.execute(sql, values)
    
    # Deleting the proposals
    sql = "DELETE FROM proposals WHERE id=%s"
    values = (proposal_id, )

    cnx.execute(sql, values)

    cnx.commit()

    print('workspace-id')

    cnx.close_cnx()
    return redirect(url_for('home'))

# Just for debugging stuffs
@app.route("/debug", methods=['POST'])
def debug():
    skills = request.form.getlist('nested-values[]')
    string = ''
    for skill in skills:
        string = string + skill
        string += ' '

    return string

