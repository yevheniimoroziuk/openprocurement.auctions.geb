# -*- coding: utf-8 -*-
from uuid import uuid4
from copy import deepcopy

from openprocurement.auctions.core.utils import (
    get_now
)

from openprocurement.auctions.geb.tests.fixtures.common import (
    test_procuringEntity
)
from openprocurement.auctions.geb.tests.fixtures.documents import (
    ELIGIBILITY_DOCUMENT,
    BID_DOCUMENT
)
now = get_now()

# bid in 'draft' status
# description:
# - value.amount = 100
# - owner = 'broker'
BID_DRAFT = {
    "status": "draft",
    "value": {
        "currency": "UAH",
        "amount": 100,
        "valueAddedTaxIncluded": True
    },
    "owner_token": uuid4().hex,
    "tenderers": [deepcopy(test_procuringEntity)],
    "owner": "broker",
    "qualified": False,
    "id": uuid4().hex,
    "date": now.isoformat()
}

# bid in 'draft' status with document
bid = deepcopy(BID_DRAFT)
bid['id'] = uuid4().hex
bid['documents'] = [BID_DOCUMENT]
BID_DRAFT_WITH_DOCUMENT = bid

# pending bids

# bid in 'pending' status
bid = deepcopy(BID_DRAFT)
bid['status'] = 'pending'
bid['id'] = uuid4().hex
BID_PENDING_FIRST = bid

# bid in 'pending' status with document
bid = deepcopy(BID_PENDING_FIRST)
bid['id'] = uuid4().hex
bid['documents'] = [BID_DOCUMENT]
BID_PENDING_FIRST_WITH_DOCUMENT = bid

# bid in 'pending' status
bid = deepcopy(BID_PENDING_FIRST)
bid['id'] = uuid4().hex
BID_PENDING_SECOND = bid

# active bids

# bid in 'active' status
auction = deepcopy(BID_PENDING_FIRST)
auction['id'] = uuid4().hex
auction['status'] = 'active'
auction['bidNumber'] = 1
auction['qualified'] = True
auction['documents'] = [ELIGIBILITY_DOCUMENT]
BID_ACTIVE_FIRST = auction

# bid in 'active' status
auction = deepcopy(BID_ACTIVE_FIRST)
auction['id'] = uuid4().hex
auction['bidNumber'] = 2
BID_ACTIVE_SECOND = auction

# bid in 'active' status with documents
bid = deepcopy(BID_ACTIVE_FIRST)
bid['id'] = uuid4().hex
bid['documents'] = [BID_DOCUMENT]
BID_ACTIVE_FIRST_WITH_DOCUMENT = bid
