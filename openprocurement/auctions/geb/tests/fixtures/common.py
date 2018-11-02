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
    "amount": 42,
    "currency": u"UAH"
}

test_auction_minimalStep_created = {
    "amount": 42,
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
