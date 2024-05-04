import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()
password = os.getenv("password")
domainName = os.getenv("domainName")
username = os.getenv("username1")

# newPassword = os.getenv("newPassword")
# newDomainName = os.getenv("newDomainName")
# newUsername = os.getenv("username1")


def connectToEs(username,password,domainName):
    es = Elasticsearch(timeout=12000, max_retries=10,
        hosts = [{'host': domainName, 'port': 443}],
        http_auth = [username, password],
        use_ssl = True)
    print("Es connected successfully")
    print(es.ping)
    return es

class ESclient:
    def __init__(self,username,password,domainName) -> None:
        self.client = None
        self.aws_auth_client = None
        self.username = username
        self.password = password
        self.domainName = domainName
    
    def getClient(self):
        if self.client is None:
            self.client  = connectToEs(self.username,self.password,self.domainName)
        return self.client
    
esclient = ESclient(username,password,domainName)

if __name__ == "__main__":
    esclient = ESclient()
    esclient.getClient()
    print("Connected to ES")
