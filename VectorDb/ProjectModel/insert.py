from ..Utils import api
from .mapping import projectIndexName, featureDims

def insertData(projectData):
    id  = projectData["id"]
        
    if(api.exists(indexName=projectIndexName, id=id)):
        api.updateRecord(projectIndexName, id, projectData)
        return
    
    if "title_feature" not in projectData:
        projectData["title_feature"] = [0.0]*featureDims
    
    if "description_feature" not in projectData:
        projectData["description_feature"] = [0.0]*featureDims
        
    if "tags_feature" not in projectData:
        projectData["tags_feature"] = [0.0]*featureDims

    api.insertRecord(projectIndexName, projectData)