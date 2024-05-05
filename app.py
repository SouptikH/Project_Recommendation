from flask import Flask, jsonify, request
from schema import User,Project
from VectorDb.Recommendation import api as recommendationApi


app = Flask("Projcet_Recommendation")


def sort_projects_by_score(projectList,idScoreList):
  indexList=list(range(len(projectList)))
  idScoreMappa=dict()
  for idScore in idScoreList:
    idScoreMappa[int(idScore['id'])]=idScore['similarity']
  indexList=sorted(indexList,key=lambda x:idScoreMappa[int(projectList[x]['proj_id'])],reverse=True)

  newProjectList=[]
  for i in indexList:
    newProjectList.append(projectList[i])
  
  return newProjectList

@app.route('/recommendation',methods=['POST'])
def get_sorted_proj_ids():
  full_data=request.get_json()
  
  try:
    userId = full_data['user_id']
    projectIds = full_data['project_ids']
    size = 5
    
    recommendedProjectIds = recommendationApi.getRecommendationForUser(userId,projectIds,size)
    return jsonify(recommendedProjectIds)
      

  except Exception as e:
    return jsonify({
      "error_message":{
        "args":e.args,
      }
    })

@app.route('/search',methods=['POST'])
def get_search_proj_ids():
    full_data = request.get_json()
    
    try:
        searchQuery = full_data['search']
        projectIds = full_data['project_ids']
        size = 2
        searchProjects = recommendationApi.getSearched(searchQuery,projectIds,size)
        print(searchProjects)
        return jsonify(searchProjects)
    
    except Exception as e:
        print(e)
        return jsonify({
            "error_message":{
                "args":e.args,
            }
        })
        
    

def runApp():
    app.run(port=9000,host='0.0.0.0')

if __name__ == "__main__":
    runApp()



"""
SAMPLE REQUEST

{
    "User":{
        "id":"1",
        "name":"Souptik",
        "professional_interest":[
            "Web Development",
            "Natural Language Processing",
            "Machine Learning"
        ]
    },
    "Projects":[
        {
            "proj_id": 1,
            "title":"Building an E-Commerce Website",
            "description":"The Online Marketplace Platform project aims to create a comprehensive online marketplace where users can buy and sell various products and services in a secure and user-friendly environment. The platform will provide a convenient marketplace for both individual sellers and businesses to reach a wide audience of potential customers.",
            "tags":[
                {
                    "name":"Web Development",
                    "id":1
                }
            ]
        },
        { 
            "proj_id": 2,
            "title":"AI Chatbot",
            "description":"This project focuses on developing an advanced conversational AI chatbot capable of engaging users in natural language conversations and providing helpful responses and assistance. The chatbot will leverage artificial intelligence and natural language processing techniques to understand user queries, generate appropriate responses, and offer personalized assistance across various domains.",
            "tags":[
                {
                    "name":"Deep Learning",
                    "id":2
                },
                {
                    "name":"Natural Language Processing",
                    "id":3
                }
            ]
        },
        { 
            "proj_id": 3,
            "title":"Renewable Energy Research Project",
            "description":"Conduct research on renewable energy sources such as solar, wind, and hydroelectric power. Analyze the feasibility and potential benefits of implementing renewable energy solutions in various industries",
            "tags":[
                {
                    "name":"Renewable Energy",
                    "id":4
                },
                {
                    "name":"Survey",
                    "id":5
                }
            ]
        }
    ]
}

"""