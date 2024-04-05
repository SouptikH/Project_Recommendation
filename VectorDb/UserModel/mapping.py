userIndexName = 'user_index'

featureDims = 256
userMapping = {
    "properties":{
        "id": {"type": "integer"},
        "interests_feature":{
            "type": "dense_vector",
            "dims": featureDims
        },
    }
}