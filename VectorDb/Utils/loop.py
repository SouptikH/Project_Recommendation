from .vector import getEmbedding
from ..UserModel import insert as userInsert
from ..ProjectModel import insert as projectInsert
from AWS import sqs

def callback(inputJson):
    if inputJson['type']=='user':
        userId = inputJson['id']
        embedding = getEmbedding(inputJson['data']['interests'])
        
        userInsert.insertData({
            "id": userId,
            "interests_feature": embedding
        })
        
        print("User Inserted")
        
    elif inputJson['type']=='project':
        projectId = inputJson['id']
        
        embedding = []
        key = ""
        
        if 'tags' in inputJson['data']:
            embedding = getEmbedding(inputJson['data']['tags'])
            key = 'tags_feature'
        
        elif 'title' in inputJson['data']:
            embedding = getEmbedding(inputJson['data']['title'])
            key = 'title_feature'
        
        elif 'description' in inputJson['data']:
            embedding = getEmbedding(inputJson['data']['description'])
            key = 'description_feature'
            
        projectInsert.insertData({
            "id": projectId,
            key: embedding
        })
        
        print("Project Inserted")
        
        
def runJobProcessor():
    sqs.loop(callback = callback,timeInMinutes=1,delete=True)