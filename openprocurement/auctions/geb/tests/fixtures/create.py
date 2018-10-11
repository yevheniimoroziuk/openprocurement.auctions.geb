# -*- coding: utf-8 -*-

from openprocurement.auctions.geb.constants import (
    DEFAULT_PROCUREMENT_METHOD_TYPE
)
from openprocurement.auctions.geb.tests.fixtures.common import (
    test_auctionPeriod,
    test_auction_budgetSpent,
    test_auction_guarantee,
    test_auction_minimalStep,
    test_auction_value,
    test_contractTerms,
    test_lotHolder,
    test_procuringEntity,
    test_registrationFee
)
from openprocurement.auctions.geb.tests.fixtures.items import (
    INITIAL_TEST_ITEM
)

CREATE_AUCTION_DEFAULT_FIXTURE = {
        "status": "draft",
        "auctionPeriod": test_auctionPeriod,
        "budgetSpent": test_auction_budgetSpent,
        "description": "test procuredure",
        "tenderAttempts": 1,
        "guarantee": test_auction_guarantee,
        "items": [INITIAL_TEST_ITEM],
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
