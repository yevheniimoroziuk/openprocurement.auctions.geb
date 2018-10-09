# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from openprocurement.auctions.core.tests.base import (
    test_organization,
)

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
test_transfer_token = "f8d93b3cd541e545927e511c215d9c21d19d14e73945ee5726e0b02b9c1474dba89375fd0dfa2245a248e76f11144b0672afb2e18afa6f27995df2bc3f57873f"
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

test_auctionParameters = {
       "type": "texas"
   }
test_registrationFee = {
    "amount": 700.87,
    "currency": "UAH"
}
test_registrationFee_created = {
    "currency": "UAH",
    "amount": 700.87,
    "valueAddedTaxIncluded": True
   }

test_auction_value = {
        "amount": 100,
        "currency": u"UAH"
}

test_auction_value_created = {
    "amount": 100,
    "currency": u"UAH",
    "valueAddedTaxIncluded": True
}

test_auction_minimalStep = {
    "amount": 35,
    "currency": u"UAH"
}

test_auction_minimalStep_created = {
    "amount": 35,
    "currency": u"UAH",
    "valueAddedTaxIncluded": True

}
test_auctionPeriod = {
    "startDate": (now.date() + timedelta(days=14)).isoformat()
}

test_auction_budgetSpent = {
    "amount": 35,
    "currency": u"UAH"
}
test_auction_budgetSpent_created = {
       "currency": "UAH",
       "amount": 35,
       "valueAddedTaxIncluded": True
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

test_document_service_url = 'http://localhost/get/6f63b414f958418082d22ec971424ca4?KeyID=172d32c8&Signature=2RWdpnpuy95Gn7E2vIDsHPPeRrtZUgtS75FsMxZBllnUUXNx%2BK7WvGeTtPvxHhcFAeW6UNfGtexCH2pNPPuzCA%3D%3D'

test_document = {
    "hash": "md5:00000000000000000000000000000000",
    "format": "application/msword",
    "url": "http://localhost/get/3ed16c4e58964858a170d38719b76996?KeyID=172d32c8&Signature=qQwkBqe5hs4MLTzh3dv7mcLRPK6JQ9O2FvXhnNzyFjyNitoOlJ%2FNvKYl9MaqExLwk1tZ9kH5aBI6Od90uPmdBw%253D%253D",
    "title": "укр.doc",
    "documentOf": "auction",
    "datePublished": now.isoformat(),
    "id": "08ced2084fdf44dc856859d478063a41",
    "dateModified": now.isoformat()
}
