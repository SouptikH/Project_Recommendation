import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()
password = os.getenv("password")
domainName = os.getenv("domainName")
username = os.getenv("username1")

def connectToEs():
    es = Elasticsearch(timeout=12000, max_retries=10,
        hosts = [{'host': domainName, 'port': 443}],
        http_auth = [username, password],
        use_ssl = True)
    print("Es connected successfully")
    print(es.ping)
    return es

class ESclient:
    def __init__(self) -> None:
        self.client = None
        self.aws_auth_client = None
    
    def getClient(self):
        if self.client is None:
            self.client  = connectToEs()
        return self.client
    
esclient = ESclient()

if __name__ == "__main__":
    esclient = ESclient()
    esclient.getClient()
    print("Connected to ES")
