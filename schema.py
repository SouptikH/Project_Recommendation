



User_Db = []
Project_Db = []


class User:

    def __init__(self,id,name):
        self.name = name
        self.id = id
        self.professional_interest = []
        self.professional_skills = []
        User_Db.append(self)

    def add_interest(self, interest):
        self.professional_interest.append(interest)

    def add_skills(self,skill):
        self.professional_skills.append(skill)


class Project:

    def __init__(self,proj_id,title,description):
        self.proj_id = proj_id
        self.title = title
        self.description = description
        self.tags = []
        Project_Db.append(self)

    def add_tags(self,tag):
        self.tags.append(tag)    

