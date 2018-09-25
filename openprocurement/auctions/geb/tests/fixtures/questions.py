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

TEST_QESTION_IN_TENDERING_PERIOD = {
    "description": "Просимо додати таблицю потрібної калорійності харчування",
    "title": "Калорійність",
    "author": deepcopy(test_procuringEntity),
    "date": calculator.tenderPeriod.startDate.isoformat(),
    "id": "a10f5d8afefd4d8594a59775e8c59867",
    "questionOf": "tender"
}
