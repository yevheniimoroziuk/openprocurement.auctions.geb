# -*- coding: utf-8 -*-
from uuid import uuid4
from copy import deepcopy


from openprocurement.auctions.geb.tests.fixtures.common import (
    test_procuringEntity
)

QUESTION = {
    "description": "Просимо додати таблицю потрібної калорійності харчування",
    "title": "Калорійність",
    "author": deepcopy(test_procuringEntity),
    "id": uuid4().hex,
    "questionOf": "tender"
}
