# -*- coding: utf-8 -*-
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
    "owner_token": "eda1899ff5d246d9893b6bf2bf5b29cf",
    "tenderers": [
        deepcopy(test_procuringEntity)
    ],
    "owner": "broker",
    "id": "c59e79cd06cd4163a2f2999d6a5cf1dc"
}
