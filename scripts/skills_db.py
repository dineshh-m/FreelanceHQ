import mysql.connector

# Create a MySQL database connection
cnx = mysql.connector.connect(user='root', password='Pallavan$2', host='localhost', database='freelancehq')

# Define the table schema and create the skills table if it doesn't already exist
create_table_query = """
CREATE TABLE IF NOT EXISTS skills (
  skill_id INT PRIMARY KEY AUTO_INCREMENT,
  skill_name VARCHAR(255)
);
"""
cursor = cnx.cursor()
cursor.execute(create_table_query)

# Read the skills from a file into a list
with open("pl.txt", "r") as f:
    skills_list = []
    for line in f:
        skills = line.strip().split(",")
        for skill in skills:
            skills_list.append(skill.strip())

# Insert the skills into the MySQL skills table
i = 251
for skill_name in skills_list:
    insert_query = "INSERT INTO skills (id, name) VALUES (%s, %s)"
    cursor.execute(insert_query, (i, skill_name))
    cnx.commit()
    print(f"Inserted skill: {skill_name}")
    i = i + 1

# Close the MySQL database connection
cursor.close()
cnx.close()

