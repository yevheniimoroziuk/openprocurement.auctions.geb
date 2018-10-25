# -*- coding: utf-8 -*-
from uuid import uuid4
from copy import deepcopy

INITIAL_TEST_ITEM = {
    "description": u"Земля для військовослужбовців",
    "classification": {
        "scheme": u"CAV-PS",
        "id": "06110000-6",
        "description": u"Земельні ділянки"
    },
    "additionalClassifications": [
            {
                "scheme": u"kvtspz",
                "id": "01.04",
                "description": "Test"
            },
            {
                "scheme": "cadastralNumber",
                "id": "42",
                "description": "Test"
            }
    ],
    "unit": {
        "name": u"item",
        "code": u"44617100-9"
    },
    "quantity": 5.0001,
    "address": {
        "countryName": u"Україна",
        "postalCode": "79000",
        "region": u"м. Київ",
        "locality": u"м. Київ",
        "streetAddress": u"вул. Банкова 1"
    }
}


item = deepcopy(INITIAL_TEST_ITEM)
item['id'] = uuid4().hex
TEST_ITEM = item
