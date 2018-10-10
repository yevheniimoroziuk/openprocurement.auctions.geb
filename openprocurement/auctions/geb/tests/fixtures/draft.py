# -*- coding: utf-8 -*-
from uuid import uuid4
from datetime import timedelta
from openprocurement.auctions.core.utils import get_now
from openprocurement.auctions.geb.tests.fixtures.common import (
    test_auctionParameters,
    test_auction_budgetSpent_created,
    test_auction_minimalStep_created,
    test_auction_value_created,
    test_contractTerms,
    test_lotHolder,
    test_procuringEntity,
    test_registrationFee_created,
    test_transfer_token,
    test_auction_guarantee
)
from openprocurement.auctions.geb.tests.fixtures.items import (
    TEST_ITEM
)

now = get_now()

DRAFT_AUCTION_DEFAULT_FIXTURE = {
   "_id": uuid4().hex,
   "procurementMethod": "open",
   "auctionID": "UA-EA-2018-09-20-000001",
   "minNumberOfQualifiedBids": 2,
   "submissionMethod": "electronicAuction",
   "awardCriteria": "highestCost",
   "owner": "broker",
   "transfer_token": test_transfer_token,
   "title": "футляри до державних нагород",
   "tenderAttempts": 1,
   "registrationFee": test_registrationFee_created,
   "owner_token": uuid4().hex,
   "auctionParameters": test_auctionParameters,
   "guarantee": test_auction_guarantee,
   "dateModified": now.isoformat(),
   "status": "draft",
   "lotHolder": test_lotHolder,
   "description": "test procuredure",
   "lotIdentifier": "219560",
   "auctionPeriod": {
       "startDate": (now + timedelta(days=14)).isoformat()
   },
   "procurementMethodType": "geb",
   "date": now.isoformat(),
   "budgetSpent": test_auction_budgetSpent_created,
   "doc_type": "Auction",
   "contractTerms": test_contractTerms,
   "minimalStep": test_auction_minimalStep_created,
   "items": [TEST_ITEM],
   "value": test_auction_value_created,
   "numberOfBids": 0,
   "procuringEntity": test_procuringEntity
}

DRAFT_AUCTION_DEFAULT_FIXTURE_WITH_INVALID_AUCTON_PERIOD = {
   "_id": uuid4().hex,
   "procurementMethod": "open",
   "auctionID": "UA-EA-2018-09-20-000001",
   "minNumberOfQualifiedBids": 2,
   "submissionMethod": "electronicAuction",
   "awardCriteria": "highestCost",
   "owner": "broker",
   "transfer_token": test_transfer_token,
   "title": u"футляри до державних нагород",
   "tenderAttempts": 1,
   "registrationFee": test_registrationFee_created,
   "owner_token": uuid4().hex,
   "auctionParameters": test_auctionParameters,
   "guarantee": test_auction_guarantee,
   "dateModified": now.isoformat(),
   "status": "draft",
   "lotHolder": test_lotHolder,
   "description": "test procuredure",
   "lotIdentifier": "219560",
   "auctionPeriod": {
       "startDate": (now + timedelta(days=3)).isoformat()
   },
   "procurementMethodType": "geb",
   "date": now.isoformat(),
   "budgetSpent": test_auction_budgetSpent_created,
   "doc_type": "Auction",
   "contractTerms": test_contractTerms,
   "minimalStep": test_auction_minimalStep_created,
   "items": [TEST_ITEM],
   "value": test_auction_value_created,
   "numberOfBids": 0,
   "procuringEntity": test_procuringEntity
}
