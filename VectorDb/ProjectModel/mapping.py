projectIndexName = 'project_index'

featureDims = 256
projectMapping = {
    "properties":{
        "id": {"type": "integer"},
        "title_feature":{
            "type": "dense_vector",
            "dims": featureDims
        },
        "description_feature":{
            "type": "dense_vector",
            "dims": featureDims
        },
        
        "tags_feature":{
            "type": "dense_vector",
            "dims": featureDims
        },
    }
}