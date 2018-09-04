# -*- coding: utf-8 -*-
from copy import deepcopy
from datetime import datetime, timedelta

from openprocurement.auctions.core.tests.base import (
    test_organization,
    base_test_bids,
)
from openprocurement.auctions.core.utils import (
    SANDBOX_MODE
)

from openprocurement.auctions.landlease.constants import (
    DEFAULT_PROCUREMENT_METHOD_TYPE
)

PARTIAL_MOCK_CONFIG = {
    "auctions.landlease": {
        "use_default": True,
        "plugins": {
            "landlease.migration": None
        },
        "migration": False,
        "aliases": [],
        "accreditation": {
            "create": [1],
            "edit": [2]
        }
    }
}

test_bankAccount = {
    "bankName": "Test bank name",
    "description": u"Test Bank Account",
    "accountIdentification": [{
        "scheme": u'UA-EDR',
        "id": u"66113000-5",
        "description": u"Test"
    }]
}

now = datetime.now()
test_procuringEntity = test_organization.copy()
test_lotHolder = test_organization.copy()

test_item = {
    "description": u"Земля для військовослужбовців",
    "classification": {
        "scheme": u"CPV",
        "id": u"66113000-5",
        "description": u"Земельні ділянки"
    },
    "unit": {
        "name": u"item",
        "code": u"44617100-9"
    },
    "quantity": 5.001,
    "address": {
        "countryName": u"Україна",
        "postalCode": "79000",
        "region": u"м. Київ",
        "locality": u"м. Київ",
        "streetAddress": u"вул. Банкова 1"
    }
}

test_registrationFee = {
    "amount": 700.87,
    "currency": "UAH"
}

test_auction_value = {
        "amount": 100,
        "currency": u"UAH"
}
test_auction_minimalStep = {
    "amount": 35,
    "currency": u"UAH"
}

test_auctionPeriod = {
    "startDate": (now.date() + timedelta(days=14)).isoformat()
}

test_auction_budgetSpent = {
    "amount": 35,
    "currency": u"UAH"
}
test_auction_guarantee = {
    "amount": 35,
    "currency": u"UAH"
}
test_contractTerms = {
    "type": "lease",
    "leaseTerms": {
        "leaseDuration": "P10Y",
    }
}

test_auction_data = {
    "auctionPeriod": test_auctionPeriod,
    "budgetSpent": test_auction_budgetSpent,
    "minNumberOfQualifiedBids":  2,
    "description": "test procuredure",
    "tenderAttempts": 1,
    "guarantee": test_auction_guarantee,
    "items": [test_item],
    "lotHolder": test_lotHolder,
    "contractTerms": test_contractTerms,
    "lotIdentifier": u"219560",
    "minimalStep": test_auction_minimalStep,
    "procurementMethodType": DEFAULT_PROCUREMENT_METHOD_TYPE,
    "procuringEntity": test_procuringEntity,
    "registrationFee": test_registrationFee,
    "title": u"футляри до державних нагород",
    "value": test_auction_value,
}

DEFAULT_ACCELERATION = 1440

if SANDBOX_MODE:
    test_auction_data['procurementMethodDetails'] = 'quick, accelerator={}'.format(DEFAULT_ACCELERATION)

test_auction_maximum_data = deepcopy(test_auction_data)
test_auction_maximum_data.update({
    "title_en": u"Cases with state awards",
    "title_ru": u"футляры к государственным наградам",
    "description": u"футляри до державних нагород",
    "description_en": u"Cases with state awards",
    "description_ru": u"футляры к государственным наградам"
})
test_auction_maximum_data["items"][0].update({
    "description_en": u"Cases with state awards",
    "description_ru": u"футляры к государственным наградам"
})

test_features_auction_data = test_auction_data.copy()
test_features_item = test_features_auction_data['items'][0].copy()
test_features_item['id'] = "1"
test_features_auction_data['items'] = [test_features_item]
test_features_auction_data["features"] = [
    {
        "code": "OCDS-123454-AIR-INTAKE",
        "featureOf": "item",
        "relatedItem": "1",
        "title": u"Потужність всмоктування",
        "title_en": "Air Intake",
        "description": u"Ефективна потужність всмоктування пилососа, в ватах (аероватах)",
        "enum": [
            {
                "value": 0.1,
                "title": u"До 1000 Вт"
            },
            {
                "value": 0.15,
                "title": u"Більше 1000 Вт"
            }
        ]
    },
    {
        "code": "OCDS-123454-YEARS",
        "featureOf": "tenderer",
        "title": u"Років на ринку",
        "title_en": "Years trading",
        "description": u"Кількість років, які організація учасник працює на ринку",
        "enum": [
            {
                "value": 0.05,
                "title": u"До 3 років"
            },
            {
                "value": 0.1,
                "title": u"Більше 3 років, менше 5 років"
            },
            {
                "value": 0.15,
                "title": u"Більше 5 років"
            }
        ]
    }
]

test_bids = []
for i in base_test_bids:
    i = deepcopy(i)
    i.update({'qualified': True})
    test_bids.append(i)

test_lots = [
    {
        'title': 'lot title',
        'description': 'lot description',
        'value': test_auction_data['value'],
        'minimalStep': test_auction_data['minimalStep'],
    }
]

test_features = [
    {
        "code": "code_item",
        "featureOf": "item",
        "relatedItem": "1",
        "title": u"item feature",
        "enum": [
            {
                "value": 0.01,
                "title": u"good"
            },
            {
                "value": 0.02,
                "title": u"best"
            }
        ]
    },
    {
        "code": "code_tenderer",
        "featureOf": "tenderer",
        "title": u"tenderer feature",
        "enum": [
            {
                "value": 0.01,
                "title": u"good"
            },
            {
                "value": 0.02,
                "title": u"best"
            }
        ]
    }
]
