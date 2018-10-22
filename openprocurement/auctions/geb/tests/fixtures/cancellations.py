# -*- coding: utf-8 -*-
from uuid import uuid4
from openprocurement.auctions.core.utils import get_now

now = get_now()

CANCELLATION = {
    "date": "2018-10-18T20:16:42.428581+03:00",
    "status": "pending",
    "reason": "Cancel reason",
    "cancellationOf": "tender",
    "id": uuid4().hex
}
