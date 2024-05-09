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
                    {"terms": {"id": projectIds}},
                    {
                        "script_score": {
                            "query": {"match_all": {}},
                            "script": {
                                "source": """
                                def title_sim = cosineSimilarity(params.query_vector, 'title_feature');
                                def description_sim = cosineSimilarity(params.query_vector, 'description_feature');
                                def tags_sim = cosineSimilarity(params.query_vector, 'tags_feature');
                                
                                if (title_sim.isNaN()) {
                                    title_sim = 0; // Set title_sim to zero if it is NaN
                                }
                                if (description_sim.isNaN()) {
                                    description_sim = 0; // Set description_sim to zero if it is NaN
                                }
                                if (tags_sim.isNaN()) {
                                    tags_sim = 0; // Set tags_sim to zero if it is NaN
                                }
                                
                                return 0.10 * title_sim + 0.30 * description_sim + 0.60 * tags_sim + 3;
                            """,
                                "params": {"query_vector": vector},
                            },
                        }
                    },
                ]
            }
        },
    }
    res = api.client.search(index=indexName, body=dataQuery)
    return getHitsFromResult(res)


def queryExactByTermAndProjectIds(indexName, query, projectIds, size=5):
    dataQuery = {
        "size": size,
        "query": {
            "bool": {
                "must": [
                    {"terms": {"id": projectIds}},
                    {
                        "script_score": {
                            "query": {
                                "multi_match": {
                                    "query": query,
                                    "fields": [
                                        "title_content",
                                        "description_content",
                                        "tags_content",
                                    ],
                                    "type": "cross_fields",
                                }
                            },
                            "script": {
                                "source": """
                                return _score;
                            """
                            },
                        }
                    },
                ]
            }
        },
    }
    
    res = api.client.search(index=indexName, body=dataQuery)
    return getHitsFromResult(res)

def queryByVectorAndTermWithProjectIds(indexName, query, vector, projectIds, size=5):
    # dataQuery = {
    #     "size": size,
    #     "query": {
    #         "bool": {
    #             "must": [
    #                 {"terms": {"id": projectIds}},
    #                 {
    #                     "script_score": {
    #                         "query": {
    #                             "multi_match": {
    #                                 "query": query,
    #                                 "fields": [
    #                                     "title_content",
    #                                     "description_content",
    #                                     "tags_content",
    #                                 ],
    #                                 "type": "best_fields",
    #                                 "fuzziness": "2",
    #                             }
    #                         },
    #                         "script": {
    #                             "source": """
    #                             def title_sim = cosineSimilarity(params.query_vector, 'title_feature');
    #                             def description_sim = cosineSimilarity(params.query_vector, 'description_feature');
    #                             def tags_sim = cosineSimilarity(params.query_vector, 'tags_feature');
                                
    #                             if (title_sim.isNaN()) {
    #                                 title_sim = 0; // Set title_sim to zero if it is NaN
    #                             }
    #                             if (description_sim.isNaN()) {
    #                                 description_sim = 0; // Set description_sim to zero if it is NaN
    #                             }
    #                             if (tags_sim.isNaN()) {
    #                                 tags_sim = 0; // Set tags_sim to zero if it is NaN
    #                             }
                                
    #                             return 0.10 * title_sim + 0.30 * description_sim + 0.60 * tags_sim + 3 + (2 * _score);
    #                         """,
    #                             "params": {
    #                                 "query_vector": vector,
    #                                 "query_string": query,
    #                             },
    #                         },
    #                         "min_score": "0.0",
    #                     }
    #                 },
    #             ]
    #         }
    #     },
    # }
    dataQuery = {
        "size": size,
        "query": {
            "function_score": {
                "query": {
                    "bool": {
                        "must": [
                            {"terms": {"id": projectIds}}
                        ]
                    }
                },
                "functions": [
                    {
                        "filter": {
                            "match": {
                                "title_content": {
                                    "query": query,
                                    "fuzziness": "1"
                                }
                            }
                        },
                        "weight": 5  # Boost for the title match
                    },
                    {
                        "filter": {
                            "match": {
                                "description_content": {
                                    "query": query,
                                    "fuzziness": "1"
                                }
                            }
                        },
                        "weight": 2  # Boost for the description match
                    },
                    {
                        "filter": {
                            "match": {
                                "tags_content": {
                                    "query": query,
                                    "fuzziness": "1"
                                }
                            }
                        },
                        "weight": 1  # Boost for the tags match
                    },
                    {
                        "script_score": {
                            "script": {
                                "source": """
                                def title_sim = cosineSimilarity(params.query_vector, 'title_feature');
                                def description_sim = cosineSimilarity(params.query_vector, 'description_feature');
                                def tags_sim = cosineSimilarity(params.query_vector, 'tags_feature');
                                
                                if (title_sim.isNaN()) {
                                    title_sim = 0; // Set title_sim to zero if it is NaN
                                }
                                if (description_sim.isNaN()) {
                                    description_sim = 0; // Set description_sim to zero if it is NaN
                                }
                                if (tags_sim.isNaN()) {
                                    tags_sim = 0; // Set tags_sim to zero if it is NaN
                                }
                                
                                return 0.10 * title_sim + 0.30 * description_sim + 0.60 * tags_sim + 3;
                                """,
                                "params": {
                                    "query_vector": vector,
                                    "query_string": query,
                                },
                            }
                        }
                    }
                ],
                "score_mode": "sum",  # Aggregate the results by summing up the scores
                "boost_mode": "replace"  # Replace the original query score with the function score
            }
        }
    }
    res = api.client.search(index=indexName, body=dataQuery)
    return getHitsFromResult(res)
