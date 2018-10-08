# -*- coding: utf-8 -*-
from copy import deepcopy
from openprocurement.auctions.core.utils import get_now
from openprocurement.auctions.geb.tests.fixtures.calculator import (
    Calculator
)
from openprocurement.auctions.geb.tests.fixtures.common import (
    test_auctionParameters,
    test_auction_budgetSpent_created,
    test_auction_minimalStep_created,
    test_auction_value_created,
    test_contractTerms,
    test_item,
    test_lotHolder,
    test_procuringEntity,
    test_registrationFee_created,
    test_transfer_token,
    test_auction_guarantee
)

now = get_now()
calculator = Calculator(now, 'rectificationPeriod', 'start')

ACTIVE_RECTIFICATION_AUCTION_DEFAULT_FIXTURE = {
   "_id": "ae7d7760cfc046b6b8b89e437cb4e761",
   "procurementMethod": "open",
   "auctionID": "UA-EA-2018-09-20-000001",
   "minNumberOfQualifiedBids": 2,
   "enquiryPeriod": {
       "startDate": calculator.enquiryPeriod.startDate.isoformat(),
       "endDate": calculator.enquiryPeriod.endDate.isoformat()
   },
   "submissionMethod": "electronicAuction",
   "next_check": calculator.rectificationPeriod.endDate.isoformat(),
   "awardCriteria": "highestCost",
   "owner": "broker",
   "transfer_token": test_transfer_token,
   "title": "футляри до державних нагород",
   "tenderAttempts": 1,
   "registrationFee": test_registrationFee_created,
   "owner_token": "6f90273c2b66498aac8f66e5d1e8671c",
   "auctionParameters": test_auctionParameters,
   "guarantee": test_auction_guarantee,
   "dateModified": now.isoformat(),
   "status": "active.rectification",
   "lotHolder": test_lotHolder,
   "description": "test procuredure",
   "lotIdentifier": "219560",
   "auctionPeriod": {
       "shouldStartAfter": calculator.auctionPeriod.shouldStartAfter.isoformat()
   },
   "procurementMethodType": "landlease",
   "tenderPeriod": {
       "startDate": calculator.tenderPeriod.startDate.isoformat(),
       "endDate": calculator.tenderPeriod.endDate.isoformat()
   },
   "date": calculator.auctionDate.date.isoformat(),
   "budgetSpent": test_auction_budgetSpent_created,
   "doc_type": "Auction",
   "rectificationPeriod": {
       "startDate": calculator.rectificationPeriod.startDate.isoformat(),
       "endDate": calculator.rectificationPeriod.endDate.isoformat()
   },
   "contractTerms": test_contractTerms,
   "minimalStep": test_auction_minimalStep_created,
   "items": [test_item],
   "value": test_auction_value_created,
   "numberOfBids": 0,
   "procuringEntity": test_procuringEntity
}

calculator = Calculator(now, 'rectificationPeriod', 'end')

END_ACTIVE_RECTIFICATION_AUCTION_DEFAULT_FIXTURE = deepcopy(ACTIVE_RECTIFICATION_AUCTION_DEFAULT_FIXTURE)
END_ACTIVE_RECTIFICATION_AUCTION_DEFAULT_FIXTURE["enquiryPeriod"] = {
                  "startDate": calculator.enquiryPeriod.startDate.isoformat(),
                  "endDate": calculator.enquiryPeriod.endDate.isoformat()
}
END_ACTIVE_RECTIFICATION_AUCTION_DEFAULT_FIXTURE["next_check"] = calculator.rectificationPeriod.endDate.isoformat()
END_ACTIVE_RECTIFICATION_AUCTION_DEFAULT_FIXTURE["auctionPeriod"] = {
    "shouldStartAfter": calculator.auctionPeriod.shouldStartAfter.isoformat()
}
END_ACTIVE_RECTIFICATION_AUCTION_DEFAULT_FIXTURE["tenderPeriod"] = {
    "startDate": calculator.tenderPeriod.startDate.isoformat(),
    "endDate": calculator.tenderPeriod.endDate.isoformat()
}
END_ACTIVE_RECTIFICATION_AUCTION_DEFAULT_FIXTURE["date"] = calculator.auctionDate.date.isoformat()
END_ACTIVE_RECTIFICATION_AUCTION_DEFAULT_FIXTURE["rectificationPeriod"] = {
    "startDate": calculator.rectificationPeriod.startDate.isoformat(),
    "endDate": calculator.rectificationPeriod.endDate.isoformat()
}
