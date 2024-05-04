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
        description_key = 'description_content'
        title_key = 'title_content'
        tags_key = 'tags_content'
        dict = {}
        
        # dict[description_key] = ""
        # dict[title_key] = ""
        # dict[tags_key] = ""
        
        if 'tags' in inputJson['data']:
            embedding = getEmbedding(inputJson['data']['tags'])
            key = 'tags_feature'

            dict[key] = embedding
            dict[tags_key]  = inputJson['data']['tags']
            
        if 'title' in inputJson['data']:
            embedding = getEmbedding(inputJson['data']['title'])
            key = 'title_feature'
            
            dict[key] = embedding
            dict[title_key] = inputJson['data']['title']
        
        if 'description' in inputJson['data']:
            embedding = getEmbedding(inputJson['data']['description'])
            key = 'description_feature'
            
            dict[key] = embedding
            dict[description_key] = inputJson['data']['description']
        
        dict['id'] = projectId
        print("Sqs message fetched")
        projectInsert.insertData(dict)
        
        print("Project Inserted")
        
        
def runJobProcessor():
    sqs.loop(callback = callback,timeInMinutes=0.2,delete=True)