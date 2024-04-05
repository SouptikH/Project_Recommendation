from ..Utils import api
from .mapping import userIndexName, featureDims

def insertData(userData):
    id  = userData["id"]
        
    if(api.exists(indexName=userIndexName, id=id)):
        api.updateRecord(userIndexName, id, userData)
        return
    
    if "interests_feature" not in userData:
        userData["interests_feature"] = [0.0]*featureDims

    api.insertRecord(userIndexName, userData)
    