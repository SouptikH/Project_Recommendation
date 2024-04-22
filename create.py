from VectorDb.ProjectModel import mapping as projectMapping
from VectorDb.UserModel import mapping as userMapping
from VectorDb.Utils import api


if __name__ == "__main__":
    api.createIndex(projectMapping.projectIndexName)
    api.createMapping(projectMapping.projectIndexName, projectMapping.projectMapping)
    
    # api.closeIndex(projectMapping.projectIndexName)
    api.createIndex(userMapping.userIndexName)
    api.createMapping(userMapping.userIndexName, userMapping.userMapping)