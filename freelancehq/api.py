from freelancehq import app, db
from flask import jsonify, request, session


def is_user_logged():
    logged = False
    if session.get('userid') != None:
        logged = True
    return logged


# API endpoints

@app.route("/api/suggest", methods=['POST'])
def suggest():
    text = request.form.get('text')
    cnx = db.DBConnection()
    cursor = cnx.cursor

    sql = "SELECT * FROM skills where name LIKE %s"
    cursor.execute(sql, ('%{}%'.format(text),))

    suggestions = []
    results = cursor.fetchall()

    if results:
        for s in results:
            suggestions.append(s)
        

    cnx.close_cnx()
    return jsonify({"suggestions": suggestions})

@app.route("/apply/project/<int:projectid>", methods=['POST'])
def apply(projectid):
    if not is_user_logged():
        return jsonify({"message": "Login Required"})
    cnx = db.DBConnection()
    project_id = request.form.get('projectID')
    freelancer_id = request.form.get('freelancerID')

    sql = "SELECT * FROM proposals WHERE freelancer_id=%s and project_id=%s"
    values = (freelancer_id, project_id)
    cnx.execute(sql, values)
    if cnx.cursor.fetchone():
        cnx.close_cnx()
        print("--------------------------------------------------------INNER")
        return jsonify({'status': 'failed', 'message': 'Proposal Already exists'})


    sql = "INSERT INTO proposals(freelancer_id, project_id) VALUES(%s, %s)"
    print("Will req.form succeed", project_id, freelancer_id)
    values = (freelancer_id, project_id)
    cnx.execute(sql, values)
    print("APPLIED")
    cnx.cnx.commit()

    cnx.close_cnx()
    print("UNAPPLIED--------------------------------------------------------------------")
    return jsonify({"status": "success"})


@app.route("/unapply/project/<int:projectid>", methods=['POST'])
def unapply(projectid):
    if not is_user_logged():
        return jsonify({"message": "Login Required"})
    cnx = db.DBConnection()

    project_id = request.form.get('projectID')
    freelancer_id = request.form.get('freelancerID')

    sql = "SELECT * FROM proposals WHERE freelancer_id=%s and project_id=%s"
    values = (freelancer_id, project_id)
    cnx.execute(sql, values)
    if not cnx.cursor.fetchone():
        cnx.close_cnx()
        print("--------------------------------------------------------INNER")
        return jsonify({'status': 'failed', 'message': 'No Proposal exists'})

    sql = "DELETE FROM proposals WHERE freelancer_id=%s AND project_id=%s"
    values = (freelancer_id, project_id)
    cnx.execute(sql, values)

    cnx.cnx.commit()

    cnx.close_cnx()
    print("UNAPPLIED--------------------------------------------------------------------")
    return jsonify({"status": "success"})


@app.route("/api/create_workspace/", methods=['POST'])
def create_workspace():

    project_id = request.form.get('userProjectID')
    freelancer_id=  request.form.get('proposedFreelancerID')
    proposal_id = request.form.get('proposalID')
    cnx = db.DBConnection()

    # Creating a workspace
    sql = "INSERT INTO workspace(project_id, freelancer_id, proposal_id) VALUES(%s, %s, %s)"
    values = (project_id, freelancer_id, proposal_id)
    cnx.execute(sql, values)

    # Deleting all other proposals
    sql = "DELETE FROM proposals WHERE id!=%s AND project_id=%s"
    values = (proposal_id, project_id)
    cnx.execute(sql, values)

    # Closing the project so that no other proposals are taken
    sql = "UPDATE projects SET finished=%s WHERE id=%s"
    values = (True, project_id)
    cnx.execute(sql, values)

    cnx.commit()

    cnx.close_cnx()
    return jsonify({"status": "success"})


@app.route("/api/delete_proposal/", methods=['POST'])
def delete_proposal():
    proposal_id = request.form.get('proposalID')
    cnx = db.DBConnection()

    sql = "DELETE FROM proposals WHERE id=%s"
    values = (proposal_id, )
    cnx.execute(sql, values)

    cnx.cnx.commit()

    cnx.close_cnx
    return jsonify({"status": "success"})

@app.route("/api/message/", methods=['POST'])
def send_message():
    workspace_id = request.form.get('workspaceID')
    message = request.form.get('message')
    sender_id = request.form.get('senderID')
    print("Sender info: ", workspace_id, message, sender_id)
    cnx = db.DBConnection()

    sql = "INSERT INTO messages(workspace_id, sender_id, content) VALUES(%s, %s, %s)"
    values = (workspace_id, sender_id, message)

    try:
        cnx.execute(sql, values)
    except Exception as e:
        print(e)
        return jsonify({'status': 'failed'})
    finally:
        cnx.commit()
        cnx.close_cnx()

    return jsonify({'status': 'success'})

