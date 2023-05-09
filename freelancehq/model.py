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