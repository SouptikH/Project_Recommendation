projectIndexName = "project_index_3"

featureDims = 256
projectMapping = {
    "properties": {
        "id": {"type": "integer"},
        "title_feature": {"type": "dense_vector", "dims": featureDims},
        "description_feature": {"type": "dense_vector", "dims": featureDims},
        "tags_feature": {"type": "dense_vector", "dims": featureDims},
        "description_content": {
            "type": "text",
            "analyzer": "english",
            "search_analyzer": "search_term_analyzer",
        },
        "title_content": {
            "type": "text",
            "analyzer": "english",
            "search_analyzer": "search_term_analyzer",
        },
        "tags_content": {
            "type": "text",
            "analyzer": "english",
            "search_analyzer": "search_term_analyzer",
        },
    }
}

# projectSetting = {
#   "settings": {
#     "analysis": {
#             "analyzer": {
#                 "search_term_analyzer": {
#                     "type": "custom",
#                     "stopwords": "_none_",
#                     "filter": [
#                         "lowercase",
#                         "asciifolding",
#                         "no_stop"
#                     ],
#                     "tokenizer": "whitespace"
#                 },
#                 "ngram_token_analyzer": {
#                     "type": "custom",
#                     "stopwords": "_none_",
#                     "filter": [
#                         "lowercase",
#                         "asciifolding",
#                         "no_stop",
#                         "ngram_filter"
#                     ],
#                     "tokenizer": "whitespace"
#                 }
#             },
#             "filter": {
#                 "no_stop": {
#                     "type": "stop",
#                     "stopwords": "_none_"
#                 },
#                 "ngram_filter": {
#                     "type": "nGram",
#                     "min_gram": "2",
#                     "max_gram": "3"
#                 }
#             }
#         }
#     }
# }

projectSetting = {
    "settings": {
        "analysis": {
            "filter": {
                "english_stop": {"type": "stop", "stopwords": "_english_"},
                "no_stop": {"type": "stop", "stopwords": "_none_"},
            },
            "analyzer": {
                "english": {
                    "tokenizer": "standard",
                    "filter": ["lowercase", "asciifolding", "english_stop"],
                },
                "search_term_analyzer": {
                    "type": "custom",
                    "stopwords": "_none_",
                    "filter": ["lowercase", "asciifolding", "no_stop"],
                    "tokenizer": "standard",
                },
            },
        }
    }
}
