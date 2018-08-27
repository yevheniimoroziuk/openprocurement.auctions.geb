PARTIAL_MOCK_CONFIG = {
    "auctions.landlease.financial":{
        "use_default":True,
        "plugins":{
            "landlease.financial.migration":None
        },
        "migration":False,
        "aliases":[],
        "accreditation": {
            "create": [1],
            "edit": [2]
        }
    },
    "auctions.landlease.other":{
        "use_default":True,
        "plugins":{
            "landlease.other.migration":None
        },
        "migration":False,
        "aliases":[],
        "accreditation": {
            "create": [1],
            "edit": [2]
        }
    }
}
