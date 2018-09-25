# -*- coding: utf-8 -*-
from uuid import uuid4
from copy import deepcopy

from openprocurement.auctions.core.utils import get_now
from openprocurement.auctions.geb.tests.fixtures.common import (
    test_procuringEntity
)
from openprocurement.auctions.geb.tests.fixtures.calculator import (
    Calculator
)

now = get_now()
calculator = Calculator(now, 'tenderingPeriod', 'start')

TEST_DRAFT_BID = {
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
    "id": uuid4().hex
}

TEST_ACTIVE_BID_FIRST = {
    "status": "active",
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
    "id": uuid4().hex
}

TEST_ACTIVE_BID_SECOND = {
    "status": "active",
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
    "id": uuid4().hex
}

TEST_PENDING_BID = {
    "status": "pending",
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
    "id": uuid4().hex
}
