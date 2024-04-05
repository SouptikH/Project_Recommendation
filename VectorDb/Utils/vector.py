from dotenv import load_dotenv
import os
import openai
load_dotenv()

fireWorksApiKey = os.getenv("fireWorksApiKey")

client = openai.OpenAI(
    base_url = "https://api.fireworks.ai/inference/v1",
    api_key=fireWorksApiKey,
    
)
def getEmbedding(text):
    if not isinstance(text, str):  # Ensure text is a string
        text = str(text)
    response = client.embeddings.create(
        model="nomic-ai/nomic-embed-text-v1.5",
        input=[text],
        dimensions=256
    )
    return response.data[0].embedding