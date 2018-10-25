# -*- coding: utf-8 -*-
from uuid import uuid4
from openprocurement.auctions.core.utils import get_now
from openprocurement.auctions.geb.tests.fixtures.documents import (
    CANCELLATION_DOCUMENT
)

now = get_now()

CANCELLATION = {
    "date": "2018-10-18T20:16:42.428581+03:00",
    "status": "pending",
    "reason": "Cancel reason",
    "cancellationOf": "tender",
    "id": uuid4().hex
}

CANCELLATION_WITH_DOCUMENTS = {
    "date": "2018-10-18T20:16:42.428581+03:00",
    "status": "pending",
    "reason": "Cancel reason",
    "documents": [CANCELLATION_DOCUMENT],
    "cancellationOf": "tender",
    "id": uuid4().hex
}

CANCELLATION_ACTIVE_WITH_DOCUMENTS = {
    "date": "2018-10-18T20:16:42.428581+03:00",
    "status": "active",
    "reason": "Cancel reason",
    "documents": [CANCELLATION_DOCUMENT],
    "cancellationOf": "tender",
    "id": uuid4().hex
}
