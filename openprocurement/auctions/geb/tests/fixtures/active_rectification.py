# -*- coding: utf-8 -*-
from iso8601 import parse_date
from copy import deepcopy
from datetime import timedelta
from uuid import uuid4

from openprocurement.auctions.core.utils import (
    get_now
)

from openprocurement.auctions.geb.tests.fixtures.calculator import (
    Calculator
)
from openprocurement.auctions.geb.tests.fixtures.draft import (
    AUCTION as BASE_AUCTION
)
from openprocurement.auctions.geb.tests.fixtures.documents import (
    DOCUMENT
)
from openprocurement.auctions.geb.tests.fixtures.cancellations import (
    CANCELLATION,
    CANCELLATION_WITH_DOCUMENTS,
    CANCELLATION_ACTIVE_WITH_DOCUMENTS
)
from openprocurement.auctions.geb.tests.fixtures.questions import (
    QUESTION
)

now = get_now()
calculator = Calculator(now, 'rectificationPeriod', 'start')
auction = deepcopy(BASE_AUCTION)
auction["_id"] = uuid4().hex
auction["enquiryPeriod"] = {
    "startDate": calculator.enquiryPeriod.startDate.isoformat(),
    "endDate": calculator.enquiryPeriod.endDate.isoformat()
}
auction["next_check"] = calculator.rectificationPeriod.endDate.isoformat()
auction["dateModified"] = now.isoformat()
auction["status"] = "active.rectification"
auction["auctionPeriod"] = {
    "startDate": calculator.auctionPeriod.startDate.isoformat()
}
auction["tenderPeriod"] = {
    "startDate": calculator.tenderPeriod.startDate.isoformat(),
    "endDate": calculator.tenderPeriod.endDate.isoformat()
}
auction["date"] = calculator.auctionDate.date.isoformat()
auction["rectificationPeriod"] = {
    "startDate": calculator.rectificationPeriod.startDate.isoformat(),
    "endDate": calculator.rectificationPeriod.endDate.isoformat()
}

# auction in 'active.rectification' status.
# description:
# - has item
# - minNumberOfQualifiedBids = 2
# - value.amount = 100
# - owner = 'broker'

AUCTION = auction

# auction without items
auction = deepcopy(AUCTION)
auction['_id'] = uuid4().hex
auction.pop('items')
AUCTION_WITHOUT_ITEMS = auction

# auction with documents
auction = deepcopy(AUCTION)
auction['documents'] = [DOCUMENT]
AUCTION_WITH_DOCUMENTS = auction

# auction with question
auction = deepcopy(AUCTION)
rectificaton_start = parse_date(auction['rectificationPeriod']['startDate'])
question_date = rectificaton_start + timedelta(minutes=42)
QUESTION['date'] = question_date.isoformat()
auction['questions'] = [QUESTION]
AUCTION_WITH_QUESTIONS = auction

# auction with cancellations
auction = deepcopy(AUCTION)
auction['_id'] = uuid4().hex
auction['cancellations'] = [CANCELLATION]
AUCTION_WITH_CANCELLATION = auction

# auction with cancellations with document
auction = deepcopy(AUCTION)
auction['_id'] = uuid4().hex
auction['cancellations'] = [CANCELLATION_WITH_DOCUMENTS]
AUCTION_WITH_CANCELLATION_WITH_DOCUMENTS = auction

# auction with active cancellation
auction = deepcopy(AUCTION)
auction['_id'] = uuid4().hex
auction['cancellations'] = [CANCELLATION_ACTIVE_WITH_DOCUMENTS]
auction['status'] = 'cancelled'
AUCTION_CANCELLED = auction

# auction in 'active.rectification' end
calculator = Calculator(now, 'rectificationPeriod', 'end')
auction = deepcopy(AUCTION)
auction["enquiryPeriod"] = {
    "startDate": calculator.enquiryPeriod.startDate.isoformat(),
    "endDate": calculator.enquiryPeriod.endDate.isoformat()
}
auction["tenderPeriod"] = {
    "startDate": calculator.tenderPeriod.startDate.isoformat(),
    "endDate": calculator.tenderPeriod.endDate.isoformat()
}
auction["rectificationPeriod"] = {
    "startDate": calculator.rectificationPeriod.startDate.isoformat(),
    "endDate": calculator.rectificationPeriod.endDate.isoformat()
}
auction["auctionPeriod"] = {
    "startDate": calculator.auctionPeriod.startDate.isoformat()
}
auction["next_check"] = calculator.rectificationPeriod.endDate.isoformat()
auction["date"] = calculator.auctionDate.date.isoformat()
END_ACTIVE_RECTIFICATION_AUCTION = auction
