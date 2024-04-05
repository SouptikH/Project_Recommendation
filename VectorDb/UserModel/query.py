from .mapping import userIndexName
from ..Utils import api

def getHitsFromResult(res):
    if res["hits"]["total"] == 0:
        return []

    return res["hits"]["hits"]

def checkIfExists(userId):
    res = api.exists(index=userIndexName, id=userId)
    return res["found"]


def getById(userId):
    res = api.getRecord(indexName=userIndexName, id=userId)
    
    if res is None:
        return None
    
    return res["_source"] if res["found"] else None