from VectorDb.Utils import api
from VectorDb.UserModel import mapping as userMapping
from VectorDb.ProjectModel import mapping as projectMapping
from VectorDb.Utils import loop,vector
from multiprocessing import Process
from app import runApp
from VectorDb.Recommendation import api as recommendationApi

if  __name__ == "__main__":
    processes = []
    
    try:
        p1 = Process(target=runApp)
        p1.start()
        processes.append(p1)
        print("App started")
        
        p2 = Process(target=loop.runJobProcessor)
        p2.start()
        processes.append(p2)
        print("Job Processor started")
        
    except KeyboardInterrupt:
        for p in processes:
            p.terminate()
            p.join()
            
        print("All processes terminated")
        exit(0)
    
    # api.deleteAllRecords(projectMapping.projectIndexName)
    # print(api.getAllRecords(projectMapping.projectIndexName))
    # print(recommendationApi.getRecommendationForUser(1,[1,2]))
    # print(api.getAllRecords(projectMapping.projectIndexName))