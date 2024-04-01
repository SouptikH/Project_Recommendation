



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

    @classmethod
    def get_User_from_json(cls,mappa:dict):
      id=mappa.get('id',-1)
      name=mappa.get('name',"")
      professional_interest=mappa.get('professional_interest',[])
      professional_skills=mappa.get('professional_skills',[])
      
      user=User(id,name)
      for interest in professional_interest:
          user.add_interest(interest)
      for skill in professional_skills:
          user.add_skills(skill)
      
      return user

    def __str__(self):
        return f"""
        name:{self.name}
        id:{self.id}
        professional_interest:{self.professional_interest}
        professional_skills:{self.professional_skills}
                """


class Project:

    def __init__(self,proj_id,title,description):
        self.proj_id = proj_id
        self.title = title
        self.description = description
        self.tags = []
        Project_Db.append(self)

    def add_tags(self,tag):
        self.tags.append(tag)    

    @classmethod
    def get_Project_from_json(cls,listOfMappa:list):
      listOfProjects=[]
      for mappa in listOfMappa:
        proj_id=mappa.get('proj_id',-1)
        title=mappa.get('title',"")
        description=mappa.get('description',"")
        tags=mappa.get('tags',[])

        project=Project(proj_id,title,description)
        for tag in tags:
            project.add_tags(tag["name"])
        listOfProjects.append(project)
        
      return listOfProjects

    def __str__(self):
        return f"""
        proj_id:{self.proj_id}
        title:{self.title}
        description:{self.description}
        tags:{self.tags}
                """
    
    def __repr__(self):
        return self.__str__()

