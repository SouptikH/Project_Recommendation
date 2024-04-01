import openai
import numpy as np
import schema


client = openai.OpenAI(
    base_url = "https://api.fireworks.ai/inference/v1",
    api_key="fTb1o4CH2WWCEPf2wYeqZDxrnCmjzYuc3IADAP8lMZ8MMkgc",
)

# Generate Embedding for a given Text 

def generate_embedding(text):  
    if not isinstance(text, str):  # Ensure text is a string
        text = str(text)
    response = client.embeddings.create(
        model="nomic-ai/nomic-embed-text-v1.5",
        input=[text]
    )
    return response.data[0].embedding


# Given two texts, compute how similar they are:

def calculate_similarity(text1,text2):
   
   emb_txt1 = generate_embedding(text1)
   emb_txt2 = generate_embedding(text2)
   dot_product = np.dot(emb_txt1, emb_txt2)
   norm_1 = np.linalg.norm(emb_txt1)
   norm_2 = np.linalg.norm(emb_txt2)
   similarity = dot_product / (norm_1 * norm_2)
   
   return similarity



#text1 = "Cat"
#text2 = "Dog"
#text3 = "apple"
#text4 = "Puppy"
#text5 = "Lion"
#text6 = "Cub"
#
#print(calculate_similarity(text1,text2))
#print(calculate_similarity(text1,text3))
#print(calculate_similarity(text2,text4))
#print(calculate_similarity(text1,text4))
#print(calculate_similarity(text1,text6))
#print(calculate_similarity(text5,text6))
#
#text7 = "Black Cat"
#text8 = "Wild Animal"
#print(calculate_similarity(text7,text5))
#print(calculate_similarity(text7,text1))
#print(calculate_similarity(text5,text8))
#print(calculate_similarity(text1,text8))    

# Compute similarity score for given user with project database 
# Output ordered list of project id and similarity score

# def order_by_similarity_score(user_id):
def order_by_similarity_score(user,projects):

    interests = user.professional_interest
    skills = user.professional_skills

    project_similarity = []

    for project in projects:
        project_title = project.title
        project_description = project.description
        project_tags = project.tags

        count = 0
        intp_sum = 0
        intd_sum = 0
        intt_sum = 0

        for interest in interests:
            intp_sim = calculate_similarity(project_title,interest)
            intd_sim = calculate_similarity(project_description,interest)
            intp_sum = intp_sim + intp_sum
            intd_sum = intd_sim + intd_sum 
            count = count+1

        
        t_sim = intp_sum/count # similarity between title and user_interest
        d_sim = intd_sum/count # similarity between description and  user_interest

        count = 0
        for tag in project_tags:
            
            intt_sim = calculate_similarity(tag,interest)
            intt_sum = intt_sum + intt_sim
            count = count + 1

        tag_sim = intt_sum/count #similarity between tags and user interest

        similarity_score = (0.32*t_sim + 0.30*d_sim + 0.38*tag_sim)*100
        project_similarity.append({"id": project.proj_id, "similarity": similarity_score})        
    
    ordered_project_ids = sorted(project_similarity, key=lambda x: x["similarity"], reverse=True)
    return ordered_project_ids



if __name__=="__main__":

  user1 = schema.User(1,"Souptik")
  user1.add_interest("Web Development")
  user1.add_interest("Natural Language Processing")
  user1.add_interest("Machine Learning")


  project1 = schema.Project(1,"Building an E-Commerce Website","The Online Marketplace Platform project aims to create a comprehensive online marketplace where users can buy and sell various products and services in a secure and user-friendly environment. The platform will provide a convenient marketplace for both individual sellers and businesses to reach a wide audience of potential customers.")
  project1.add_tags("Web Development")
  project2 = schema.Project(2,"AI Chatbot","This project focuses on developing an advanced conversational AI chatbot capable of engaging users in natural language conversations and providing helpful responses and assistance. The chatbot will leverage artificial intelligence and natural language processing techniques to understand user queries, generate appropriate responses, and offer personalized assistance across various domains." )
  project2.add_tags("Deep Learning")
  project2.add_tags("Natural Language Processing")
  project3 = schema.Project(3,"Renewable Energy Research Project","Conduct research on renewable energy sources such as solar, wind, and hydroelectric power. Analyze the feasibility and potential benefits of implementing renewable energy solutions in various industries")
  project3.add_tags("Renewable Energy")
  project3.add_tags("Survey")

  user_id = 1
  project_similarity = order_by_similarity_score(user_id)
  if project_similarity:
      print("Project IDs and their respective similarity scores:")
      for project in project_similarity:
          print(f"Project ID: {project['id']}, Similarity Score: {project['similarity']}")
  else:
      print("User profile not found or no professional interests.")



