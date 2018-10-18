# -*- coding: utf-8 -*-
from copy import deepcopy
from uuid import uuid4

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
    test_lotHolder,
    test_bankAccount,
    test_procuringEntity,
    test_registrationFee_created,
    test_transfer_token,
    test_auction_guarantee,
)

from openprocurement.auctions.geb.tests.fixtures.items import (
    TEST_ITEM
)
from openprocurement.auctions.geb.tests.fixtures.documents import (
    DOCUMENT
)
from openprocurement.auctions.geb.tests.fixtures.questions import (
    TEST_QESTION_IN_RECTIFICATION_PERIOD
)

# active rectification default auction

now = get_now()
calculator = Calculator(now, 'rectificationPeriod', 'start')

ACTIVE_RECTIFICATION_AUCTION_DEFAULT_FIXTURE = {
    "_id": uuid4().hex,
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
    "owner_token": uuid4().hex,
    "auctionParameters": test_auctionParameters,
    "guarantee": test_auction_guarantee,
    "dateModified": now.isoformat(),
    "status": "active.rectification",
    "lotHolder": test_lotHolder,
    'bankAccount': test_bankAccount,
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
    "items": [TEST_ITEM],
    "value": test_auction_value_created,
    "numberOfBids": 0,
    "procuringEntity": test_procuringEntity
}

# end active rectification default fixture

calculator = Calculator(now, 'rectificationPeriod', 'end')

auction = deepcopy(ACTIVE_RECTIFICATION_AUCTION_DEFAULT_FIXTURE)

auction["enquiryPeriod"] = {
    "startDate": calculator.enquiryPeriod.startDate.isoformat(),
    "endDate": calculator.enquiryPeriod.endDate.isoformat()
}
auction["tenderPeriod"] = {
    "startDate": calculator.tenderPeriod.startDate.isoformat(),
    "endDate": calculator.tenderPeriod.endDate.isoformat()
}
auction["rectificationPeriod"] = {
    "startDate": calculator.rectificationPeriod.startDate.isoformat(),
    "endDate": calculator.rectificationPeriod.endDate.isoformat()
}
auction["auctionPeriod"] = {
    "shouldStartAfter": calculator.auctionPeriod.shouldStartAfter.isoformat()
}
auction["next_check"] = calculator.rectificationPeriod.endDate.isoformat()
auction["date"] = calculator.auctionDate.date.isoformat()

END_ACTIVE_RECTIFICATION_AUCTION_DEFAULT_FIXTURE = auction

auction = deepcopy(ACTIVE_RECTIFICATION_AUCTION_DEFAULT_FIXTURE)

auction['documents'] = [DOCUMENT]

ACTIVE_RECTIFICATION_AUCTION_WITH_DOCUMENTS = auction

# auction with questions fixture

auction = deepcopy(ACTIVE_RECTIFICATION_AUCTION_DEFAULT_FIXTURE)
auction['questions'] = [TEST_QESTION_IN_RECTIFICATION_PERIOD]

ACTIVE_RECTIFICATION_AUCTION_FIXTURE_WITH_QUESTION = auction
