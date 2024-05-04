from ..es import esclient
from elasticsearch import helpers
import json
import uuid


client = esclient.getClient()

def getRecordsFromHits(hits):
    records = []
    for hit in hits:
        records.append(hit["_source"])
    return records


# def transferData(indexName):
#     records = getAllRecords(indexName,client=newclient,size=1000)
    
#     records = getRecordsFromHits(records["hits"]["hits"])
#     # print(records)
#     # records = [record["_source"] for record in records]
#     bulkInsert(indexName,records,client=client)

# def transferData():
#     #create indices in new client
#     newesclient.indices.delete(index=appMapping.appIndexName, ignore=[400, 404])
#     newesclient.indices.delete(index=featureMapping.featureIndex, ignore=[400, 404])
#     newesclient.indices.delete(index=rawDataMapping.rawDataIndexName, ignore=[400, 404])
#     newesclient.indices.delete(index=dataMapping.dataIndexName, ignore=[400, 404])
    
#     newesclient.indices.create(index=appMapping.appIndexName)
#     newesclient.indices.put_mapping(index = appMapping.appIndexName,body=appMapping.appMapping)
#     newesclient.indices.create(index=featureMapping.featureIndex)
#     newesclient.indices.put_mapping(index = featureMapping.featureIndex,body=featureMapping.featureMapping)
#     newesclient.indices.create(index=rawDataMapping.rawDataIndexName)
#     newesclient.indices.put_mapping(index = rawDataMapping.rawDataIndexName,body=rawDataMapping.rawDataMapping)
#     newesclient.indices.create(index=dataMapping.dataIndexName)
#     newesclient.indices.put_mapping(index = dataMapping.dataIndexName,body=dataMapping.dataMapping)
    
#     #get all records from old client
#     appRecords = getAllRecords(appMapping.appIndexName,size=1000)
#     featureRecords = getAllRecords(featureMapping.featureIndex,size=1000)
#     rawDataRecords = getAllRecords(rawDataMapping.rawDataIndexName,size=1000)
#     dataRecords = getAllRecords(dataMapping.dataIndexName,size=1000)

    
#     #insert records into new client
#     bulkInsert(appMapping.appIndexName,getRecordsFromHits(appRecords["hits"]["hits"]))
#     bulkInsert(featureMapping.featureIndex,getRecordsFromHits(featureRecords["hits"]["hits"]))
#     bulkInsert(rawDataMapping.rawDataIndexName,getRecordsFromHits(rawDataRecords["hits"]["hits"]))
#     bulkInsert(dataMapping.dataIndexName,getRecordsFromHits(dataRecords["hits"]["hits"]))
    

def createIndex(indexName):
    res=client.indices.create(index=indexName)
    print(res)
    return res


def transferFromIndex(index1,index2):
    records = getAllRecords(index1,client=client,size=1000)
    records = getRecordsFromHits(records["hits"]["hits"])
    bulkInsert(index2,records,client=client)

def getRecord(indexName,id=id):
    try:
        return client.get(index=indexName, doc_type="_doc", id=id)
    except:
        return None

def getAllIndex():
    res=client.indices.get_alias("*")
    print(res)

def deleteAllIndex():
    indices=client.indices.get_alias().keys()
    for name in indices:
        print(f"Deleted {name}")
        client.indices.delete(index=name)

def deleteIndex(indexName):
    client.indices.delete(index=indexName)


def createMapping(indexName,params):
    res = client.indices.put_mapping(index = indexName,body=params)
    return res

def createSetting(indexName,params):
    res = client.indices.put_settings(index=indexName,body=params)

def closeIndex(indexName):
    res = client.indices.close(index=indexName)

def openIndex(indexName):
    res = client.indices.open(index=indexName)

def getMapping(indexName):
    res = client.indices.get_mapping(index = indexName)
    return res

def getAllRecords(indexName, size=1,client=client):
    dataQuery={
      "size":size,
        "query" : {
            "match_all" : {}
        }
    }
    res = client.search(index=indexName, body=dataQuery, ignore=400)
    return res

def deleteAllRecords(indexName):
  data={
        "query": {
            "match_all": {}
        }
    }
  res=client.delete_by_query(index=indexName,doc_type="_doc",body=data)
  return res

def insertRecord(indexName, record):
    if "id" in record:
        return client.index(index=indexName, doc_type="_doc", id = record["id"],body = record)
    else:
        return client.index(index=indexName, doc_type="_doc",body = record)
    
    
def exists(indexName, id):
    return client.exists(index=indexName, id=id)

def updateRecord(indexName, id, record):
    return client.update(index = indexName, id=id, body={"doc": record})

def updateRecordByField(indexName, field, value, record):
    #select record by value of field and update it to record
    return client.update_by_query(index=indexName, body={"query": {"match": {field: value}}, "script": {"source": "ctx._source = params", "params": record}})

#data is a json object
def bulkInsert(indexName, data, saveSize=50,client=client):

    actions = []

    #if id is not present, generate a hash for the id based on timestamp
    for record in data:
        if "id" in record:
            action = {
                "_index": indexName,
                "_id": record["id"],
                "_source": record
            }
        
        else:
            action = {
                "_index": indexName,
                "_source": record,
                "_id": uuid.uuid4()
            }
        actions.append(action)

    helpers.bulk(client, actions, chunk_size=saveSize)
    
def deleteByQuery(indexName, query):
    return client.delete_by_query(index=indexName, body=query)
    