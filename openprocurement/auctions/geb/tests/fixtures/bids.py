# -*- coding: utf-8 -*-
from uuid import uuid4
from copy import deepcopy

from openprocurement.auctions.core.utils import get_now
from openprocurement.auctions.geb.tests.fixtures.common import (
    test_procuringEntity
)
from openprocurement.auctions.geb.tests.fixtures.documents import (
    ELIGIBILITY_DOCUMENT,
    BID_DOCUMENT
)
from openprocurement.auctions.geb.tests.fixtures.calculator import (
    Calculator
)

now = get_now()
calculator = Calculator(now, 'tenderingPeriod', 'start')

DRAFT_BID = {
    "status": "draft",
    "value": {
        "currency": "UAH",
        "amount": 100,
        "valueAddedTaxIncluded": True
    },
    "owner_token": uuid4().hex,
    "tenderers": [
        deepcopy(test_procuringEntity)
    ],
    "owner": "broker",
    "qualified": False,
    "id": uuid4().hex
}

bid = deepcopy(DRAFT_BID)
bid['id'] = uuid4().hex
bid['documents'] = [BID_DOCUMENT]

DRAFT_BID_WITH_DOCUMENT = bid

# pending bids
bid = deepcopy(DRAFT_BID)
bid['status'] = 'pending'
bid['id'] = uuid4().hex

PENDING_BID_FIRST = bid

bid = deepcopy(PENDING_BID_FIRST)
bid['id'] = uuid4().hex
bid['documents'] = [BID_DOCUMENT]

PENDING_BID_FIRST_WITH_DOCUMENT = bid

bid = deepcopy(PENDING_BID_FIRST)
bid['id'] = uuid4().hex

PENDING_BID_SECOND = bid

auction = deepcopy(PENDING_BID_FIRST)
auction['id'] = uuid4().hex
auction['status'] = 'active'
auction['bidNumber'] = 1
auction['qualified'] = True
auction['documents'] = [ELIGIBILITY_DOCUMENT]

ACTIVE_BID_FIRST = auction


auction = deepcopy(ACTIVE_BID_FIRST)
auction['id'] = uuid4().hex
auction['bidNumber'] = 2
ACTIVE_BID_SECOND = auction

bid = deepcopy(ACTIVE_BID_FIRST)
bid['id'] = uuid4().hex
bid['documents'] = [BID_DOCUMENT]

ACTIVE_BID_FIRST_WITH_DOCUMENT = bid
