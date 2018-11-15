# -*- coding: utf-8 -*-
from uuid import uuid4
from copy import deepcopy
from datetime import timedelta
from openprocurement.auctions.core.utils import (
    get_now,
    SANDBOX_MODE
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
    test_auction_guarantee
)
from openprocurement.auctions.geb.tests.fixtures.items import (
    TEST_ITEM
)
from openprocurement.auctions.geb.tests.fixtures.cancellations import (
    CANCELLATION,
    CANCELLATION_WITH_DOCUMENTS
)

now = get_now()

# draft default auction
AUCTION = {
    "_id": uuid4().hex,
    "auctionID": "UA-EA-2018-09-20-000001",
    "auctionParameters": test_auctionParameters,
    "auctionPeriod": {"startDate": (now + timedelta(days=14)).isoformat()},
    "awardCriteria": "highestCost",
    "budgetSpent": test_auction_budgetSpent_created,
    "contractTerms": test_contractTerms,
    "date": now.isoformat(),
    "dateModified": now.isoformat(),
    "description": "test procuredure",
    "doc_type": "Auction",
    "guarantee": test_auction_guarantee,
    "items": [TEST_ITEM],
    "lotHolder": test_lotHolder,
    "lotIdentifier": "219560",
    "minNumberOfQualifiedBids": 2,
    "minimalStep": test_auction_minimalStep_created,
    "numberOfBids": 0,
    "owner": "broker",
    "owner_token": uuid4().hex,
    "procurementMethod": "open",
    "procurementMethodType": "landlease",
    "procuringEntity": test_procuringEntity,
    "registrationFee": test_registrationFee_created,
    "status": "draft",
    "submissionMethod": "electronicAuction",
    "tenderAttempts": 1,
    "title": "футляри до державних нагород",
    "transfer_token": test_transfer_token,
    "value": test_auction_value_created,
    'bankAccount': test_bankAccount,
}

if SANDBOX_MODE:
    AUCTION['procurementMethodDetails'] = 'quick, accelerator=14400'
    AUCTION['submissionMethodDetails'] = 'test submissionMethodDetails'

# auction with invalid auction period
auction = deepcopy(AUCTION)
auction['_id'] = uuid4().hex
auction['auctionPeriod'] = {
    "startDate": (now + timedelta(days=3)).isoformat()
}
AUCTION_WITH_INVALID_AUCTON_PERIOD = auction

# auction without items
auction = deepcopy(AUCTION)
auction['_id'] = uuid4().hex
auction.pop('items')
AUCTION_WITHOUT_ITEMS = auction

# auction with cancellation
auction = deepcopy(AUCTION)
auction['_id'] = uuid4().hex
auction['cancellations'] = [CANCELLATION]
AUCTION_WITH_CANCELLATION = auction

# auction with cancellation with documents
auction = deepcopy(AUCTION_WITH_CANCELLATION)
auction['_id'] = uuid4().hex
auction['cancellations'] = [CANCELLATION_WITH_DOCUMENTS]
AUCTION_WITH_CANCELLATION_WITH_DOCUMENTS = auction
