# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from openprocurement.auctions.core.tests.base import (
    test_organization,
)

from openprocurement.auctions.geb.constants import (
    DEFAULT_PROCUREMENT_METHOD_TYPE
)

PARTIAL_MOCK_CONFIG = {
    "auctions.geb": {
        "use_default": True,
        "plugins": {
            "geb.migration": None
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

test_question_data = {
  "data": {
      "author": test_organization,
      "description": "Просимо додати таблицю потрібної калорійності харчування",
      "title": "Калорійність"
  }
}

test_bid_data = {
    "data": {
        "status": "draft",
        "qualified": True,
        "value": test_auction_value,
        "tenderers": [test_organization]
    }
}
#test_auction_auction_data = {
#    'auctionUrl': u'http://auction-sandbox.openprocurement.org/auctions/{}'.format(self.auction_id),
#    'bids': [
#        {
#            "id": self.initial_bids[1]['id'],
#            "participationUrl": u'http://auction-sandbox.openprocurement.org/auctions/{}?key_for_bid={}'.format( self.auction_id, self.initial_bids[1]['id'])
#        }
#    ]
#}
#
