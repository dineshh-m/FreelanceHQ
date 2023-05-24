from freelancehq import db, routes
from datetime import datetime, timedelta
from flask import session

class Model:
    def __init__(self):
        pass


class User:
    def __init__(self, user):
        print("@db-------------------", user, "---------------------")
        self.userid = user[0]
        self.username = user[1]
        self.email = user[2]
        self.firstname = user[7]
        self.lastname = user[8]

    def get_firstname(self):
        return self.firstname
    
    def get_lastname(self):
        return self.lastname
    

class Profile:
    def __init__(self, profile):
        self.profile_id = profile[0]
        self.user_id = profile[1]
        self.firstname = profile[2]
        self.lastname = profile[3]
        self.summary = profile[5]
        self.gender = profile[6]
        self.dob = profile[7]
        self.jobrole = profile[8]
        self.living_area = profile[9]

class UserSkills:
    def __init__(self,userid,  skills):
        self.userid = userid
        self.skill_ids = []
        for s in skills:
            self.skill_ids.append(s[1])

        # Constructing Actual skills
        self.skills = []
        cnx = db.DBConnection()
        cursor = cnx.cursor
        sql = "SELECT name FROM skills where id=%s"
        for id in self.skill_ids:
            values = (id,)
            cursor.execute(sql, values)
            skill_name = cursor.fetchone()
            self.skills.append(skill_name[0])

        # Closing connection
        cnx.close_cnx()

        
class ProjectPost:
    def __init__(self, post, cnx):
        self.id = post[0]
        self.client_id = post[1]
        self.title = post[2]
        self.description = post[3]
        self.budget = post[4]
        self.deadline = post[5]
        self.created_at = post[6]
        self.currency = post[7]
        self.finished = post[8]
        self.applied = False

        # Fetching skills associated with the project
        nested_sql = "SELECT name FROM (SELECT * FROM project_skills WHERE project_id=%s) as p_skills join skills as sk on p_skills.project_skill_id=sk.id"
        values = (self.id, )
        cnx.execute(nested_sql, values)
        p_skills = cnx.cursor.fetchall()
        self.project_skills = []


        time_difference = datetime.now() - self.created_at
    
        # Convert the time difference to a human-readable format
        if time_difference.days > 0:
            if time_difference.days == 1:
                self.relative_time = f'{time_difference.days} day ago'
            else:
                self.relative_time = f'{time_difference.days} days ago'
        elif time_difference.seconds // 3600 > 0:
            if time_difference.seconds // 3600 == 1:
                self.relative_time = f'{time_difference.seconds // 3600} hour ago'
            else:
                self.relative_time = f'{time_difference.seconds // 3600} hours ago'
        elif time_difference.seconds // 60 > 0:
            if time_difference.seconds // 60 == 1:
                self.relative_time = f'{time_difference.seconds // 60} minute ago'
            else:
                self.relative_time = f'{time_difference.seconds // 60} minutes ago'
        else:
            self.relative_time = 'Just now'

        for skill in p_skills:
            self.project_skills.append(skill[0])

        logged_userid = session.get('userid')
        sql = "SELECT * FROM proposals WHERE freelancer_id=%s AND project_id=%s"
        values = (logged_userid, self.id)
        cnx.execute(sql, values)
        if cnx.cursor.fetchone():
            self.applied = True


class Notification:

    def __init__(self, ntfn):
        self.user_project_id = ntfn[0]
        self.client_id = ntfn[1]
        self.title = ntfn[2]
        self.proposal_id = ntfn[3]
        self.proposed_freelancer_id = ntfn[4]
        self.proposed_at = ntfn[5]
        self.freelancer_model = routes.get_user_model_by_id(self.proposed_freelancer_id)


class PersonalWorkspace:

    def __init__(self, workspace) -> None:
        cnx = db.DBConnection()
        self.project_id = workspace[0]
        self.personal_workspace_id = workspace[1]
        self.freelancer_id = workspace[3]
        self.proposal_id = workspace[4]
        self.project_post = ProjectPost(routes.get_post_by_id(self.project_id, cnx), cnx)

        cnx.close_cnx()
    

class ClientWorkspace:

    def __init__(self, client_workspace) -> None:
        cnx = db.DBConnection()
        self.client_workspace_id = client_workspace[0]
        self.project_id = client_workspace[1]
        self.freelancer_id = client_workspace[2]
        self.proposal_id  = client_workspace[3]
        self.project_post = ProjectPost(routes.get_post_by_id(self.project_id, cnx), cnx)
        cnx.close_cnx()


class Workspace:

    def __init__(self, client_workspace) -> None:
        cnx = db.DBConnection()
        self.client_workspace_id = client_workspace[0]
        self.project_id = client_workspace[1]
        self.freelancer_id = client_workspace[2]
        self.proposal_id  = client_workspace[3]
        self.project_post = ProjectPost(routes.get_post_by_id(self.project_id, cnx), cnx)
        cnx.close_cnx()

class Message:

    def __init__(self, message):
        self.message_id = message[0]
        self.workspace_id = message[1]
        self.sender_id = message[2]
        self.sent_at = message[3]
        self.content = message[4]

        
