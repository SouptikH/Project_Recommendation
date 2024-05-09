from ..ProjectModel import query as projectQuery
from ..UserModel import query as userQuery
from VectorDb.Utils import vector

# def getHitsFromResult(res):
#     if res["hits"]["total"] == 0:
#         return []

#     return res["hits"]["hits"]



def getRecommendationForUser(userId, projectIds, size=5):
    user = userQuery.getById(userId)
    if user is None or len(user) == 0:
        return projectIds

    userVector = user["interests_feature"]
    print("Here")
    output = projectQuery.queryByVectorWithProjectIds(
        projectQuery.projectIndexName, userVector, projectIds, size=size
    )
    print("Here1")
    
    # print(output)
    # print(output)
    return [(x["_source"]['id'],x["_score"]) for x in output]

def getSearched(search,projectIds,size=2):
    
    #extract portion in double quotes (if present)
    
    if(search[0]=='"'):
        search = search[1:]
        search = search[:search.find('"')]
        print(search)
        output =  projectQuery.queryExactByTermAndProjectIds(
            projectQuery.projectIndexName, search, projectIds, size=size
        )
        
        return [(x["_source"]['id'],x["_score"]) for x in output]
        
    searchVector = vector.getEmbedding(search)
    output = projectQuery.queryByVectorAndTermWithProjectIds(
        projectQuery.projectIndexName, search, searchVector, projectIds, size=size
    )
    
    if(len(output)==0):
        output = projectQuery.queryByVectorWithProjectIds(
            projectQuery.projectIndexName, searchVector, projectIds, size=size
        )

    
    return [(x["_source"]['id'],x["_score"]) for x in output]
