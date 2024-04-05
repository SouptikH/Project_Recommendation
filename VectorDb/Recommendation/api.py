from ..ProjectModel import query as projectQuery
from ..UserModel import query as userQuery
from VectorDb.Utils import vector

# def getHitsFromResult(res):
#     if res["hits"]["total"] == 0:
#         return []

#     return res["hits"]["hits"]



def getRecommendationForUser(userId, projectIds, size=5):
    user = userQuery.getById(userId)
    print(user)
    if user is None or len(user) == 0:
        return projectIds

    userVector = user["interests_feature"]

    output = projectQuery.queryByVectorWithProjectIds(
        projectQuery.projectIndexName, userVector, projectIds, size=size
    )
    
    # print(output)
    
    return [x["_source"]['id'] for x in output]

def getSearched(search,projectIds,size=2):
    searchVector = vector.getEmbedding(search)

    output = projectQuery.queryByVectorWithProjectIds(
        projectQuery.projectIndexName, searchVector, projectIds, size=size
    )

    
    return [x["_source"]['id'] for x in output]
