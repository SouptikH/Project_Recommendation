from ..Utils import api
from .mapping import projectIndexName


def getHitsFromResult(res):
    if res["hits"]["total"] == 0:
        return []

    return res["hits"]["hits"]


def checkIfExists(projectId):
    res = api.exists(index=projectIndexName, id=projectId)
    return res["found"]


def queryByVector(indexName, vector, size=5):
    dataQuery = {
        "size": size,
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "0.10*cosineSimilarity(params.query_vector, doc['title_feature']) + 0.30*cosineSimilarity(params.query_vector, doc['description_feature']) + 0.60*cosineSimilarity(params.query_vector, doc['tags_feature']) + 3",
                    "params": {"query_vector": vector},
                },
            }
        },
    }
    res = api.client.search(index=indexName, body=dataQuery)
    return getHitsFromResult(res)


def queryByVectorWithProjectIds(indexName, vector, projectIds, size=5):
    dataQuery = {
        "size": size,
        "query": {
            "bool": {
                "must": [
                    {
                        "terms": {
                            "id": projectIds
                        }
                    },
                    {
                        "script_score": {
                            "query": {"match_all": {}},
                            "script": {
                                "source": "0.10*cosineSimilarity(params.query_vector, doc['title_feature']) + 0.30*cosineSimilarity(params.query_vector, doc['description_feature']) + 0.60*cosineSimilarity(params.query_vector, doc['tags_feature']) + 3",
                                "params": {"query_vector": vector},
                            },
                        }
                    }
                ]
            }
        },
    }
    res = api.client.search(index=indexName, body=dataQuery)
    return getHitsFromResult(res)
