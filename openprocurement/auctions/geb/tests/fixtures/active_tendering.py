from iso8601 import parse_date
from datetime import timedelta
from uuid import uuid4
from copy import deepcopy

from openprocurement.auctions.core.utils import get_now

from openprocurement.auctions.geb.tests.fixtures.active_rectification import (
    AUCTION as ACTIVE_RECTIFICATION_AUCTION,
)
from openprocurement.auctions.geb.tests.fixtures.questions import (
    QUESTION
)
from openprocurement.auctions.geb.tests.fixtures.bids import (
    BID_ACTIVE_FIRST,
    BID_ACTIVE_FIRST_WITH_DOCUMENT,
    BID_ACTIVE_SECOND,
    BID_DRAFT,
    BID_DRAFT_WITH_DOCUMENT,
    BID_PENDING_FIRST,
    BID_PENDING_FIRST_WITH_DOCUMENT
)
from openprocurement.auctions.geb.tests.fixtures.documents import (
    DOCUMENT,
    OFFLINE_DOCUMENT
)
from openprocurement.auctions.geb.tests.fixtures.cancellations import (
    CANCELLATION,
    CANCELLATION_WITH_DOCUMENTS
)
from openprocurement.auctions.geb.tests.fixtures.calculator import (
    Calculator
)

now = get_now()
calculator = Calculator(now, 'tenderPeriod', 'start')
auction = deepcopy(ACTIVE_RECTIFICATION_AUCTION)
auction['status'] = 'active.tendering'
auction["rectificationPeriod"] = {
    "startDate": calculator.rectificationPeriod.startDate.isoformat(),
    "endDate": calculator.rectificationPeriod.endDate.isoformat()
}
auction["tenderPeriod"] = {
    "startDate": calculator.tenderPeriod.startDate.isoformat(),
    "endDate": calculator.tenderPeriod.endDate.isoformat()
}
auction["enquiryPeriod"] = {
                  "startDate": calculator.enquiryPeriod.startDate.isoformat(),
                  "endDate": calculator.enquiryPeriod.endDate.isoformat()
}
auction["auctionPeriod"] = {
    "startDate": calculator.auctionPeriod.startDate.isoformat()
}
auction["next_check"] = calculator.tenderPeriod.endDate.isoformat()
auction["date"] = calculator.auctionDate.date.isoformat()

# auction in 'active.tendering' status.
# description:
# - has item
# - minNumberOfQualifiedBids = 2
# - value.amount = 100
# - minimalStep.amount = 42
# - owner = 'broker'
AUCTION = auction

# auction with question
auction = deepcopy(AUCTION)
tendering_start = parse_date(auction['tenderPeriod']['startDate'])
question_date = tendering_start + timedelta(minutes=42)
QUESTION['date'] = question_date.isoformat()
auction['questions'] = [QUESTION]
AUCTION_WITH_QUESTIONS = auction

# auction with documents
auction = deepcopy(AUCTION)
auction['documents'] = [DOCUMENT]
AUCTION_WITH_DOCUMENTS = auction

# auction with offline_documents
auction = deepcopy(AUCTION)
auction['documents'] = [OFFLINE_DOCUMENT]
AUCTION_WITH_OFFLINE_DOCUMENTS = auction

# auction with cancellation
auction = deepcopy(AUCTION)
auction['_id'] = uuid4().hex
auction['cancellations'] = [CANCELLATION]
AUCTION_WITH_CANCELLATION = auction

# auction with cancellation with document
auction = deepcopy(AUCTION)
auction['_id'] = uuid4().hex
auction['cancellations'] = [CANCELLATION_WITH_DOCUMENTS]
AUCTION_WITH_CANCELLATION_WITH_DOCUMENTS = auction

# auctions with bids

# auction with bid in 'draft'
auction = deepcopy(AUCTION)
auction['bids'] = [BID_DRAFT]
AUCTION_WITH_BID_DRAFT = auction

# auction with bid in 'pending'
auction = deepcopy(AUCTION)
auction['bids'] = [BID_PENDING_FIRST]
AUCTION_WITH_BID_PENDING = auction

# auction with bid in 'active'
auction = deepcopy(AUCTION)
auction['bids'] = [BID_ACTIVE_FIRST]
AUCTION_WITH_BID_ACTIVE = auction

# auctions with bid with document

# auction with bid in status 'draft' with document
auction = deepcopy(AUCTION)
auction['bids'] = [BID_DRAFT_WITH_DOCUMENT]
AUCTION_WITH_BID_DRAFT_WITH_DOCUMENT = auction

# auction with bid in status 'pending' with document
auction = deepcopy(AUCTION)
auction['bids'] = [BID_PENDING_FIRST_WITH_DOCUMENT]
AUCTION_WITH_BID_PENDING_WITH_DOCUMENT = auction

# auction with bid in status 'active' with document
auction = deepcopy(AUCTION)
auction['bids'] = [BID_ACTIVE_FIRST_WITH_DOCUMENT]
AUCTION_WITH_BID_ACTIVE_WITH_DOCUMENT = auction

# auction with two bids in status 'active' and cancellation
auction = deepcopy(AUCTION)
auction['_id'] = uuid4().hex
auction['cancellations'] = [CANCELLATION]
auction['bids'] = [BID_ACTIVE_FIRST, BID_ACTIVE_SECOND]
AUCTION_WITH_BIDS_WITH_CANCELLATION = auction

# auctions in 'active.tendering' end

# auction in 'active.tendering' end
calculator = Calculator(now, 'tenderPeriod', 'end')
auction = deepcopy(AUCTION)
auction["rectificationPeriod"] = {
    "startDate": calculator.rectificationPeriod.startDate.isoformat(),
    "endDate": calculator.rectificationPeriod.endDate.isoformat()
}
auction["tenderPeriod"] = {
    "startDate": calculator.tenderPeriod.startDate.isoformat(),
    "endDate": calculator.tenderPeriod.endDate.isoformat()
}
auction["enquiryPeriod"] = {
    "startDate": calculator.enquiryPeriod.startDate.isoformat(),
    "endDate": calculator.enquiryPeriod.endDate.isoformat()
}
auction["auctionPeriod"] = {
    "startDate": calculator.auctionPeriod.startDate.isoformat()
}
auction["next_check"] = calculator.enquiryPeriod.endDate.isoformat()
auction["date"] = calculator.auctionDate.date.isoformat()
END_ACTIVE_TENDERING_AUCTION = auction


# auction in end 'active.tendering' with one bid in status 'active'
auction = deepcopy(END_ACTIVE_TENDERING_AUCTION)
auction['bids'] = [BID_ACTIVE_FIRST]
END_ACTIVE_TENDERING_AUCTION_WITH_ONE_BID = auction

# auction in end 'active.tendering' with two bid in status 'active'
auction = deepcopy(END_ACTIVE_TENDERING_AUCTION)
auction['bids'] = [BID_ACTIVE_FIRST, BID_ACTIVE_SECOND]
END_ACTIVE_TENDERING_AUCTION_WITH_TWO_BIDS = auction

# auction in end 'active.tendering' with
# two bid in status 'active' and one bid in status 'draft'
auction = deepcopy(END_ACTIVE_TENDERING_AUCTION)
auction['bids'] = [BID_ACTIVE_FIRST, BID_ACTIVE_SECOND, BID_DRAFT]
END_ACTIVE_TENDERING_AUCTION_WITH_TWO_BIDS_AND_ONE_DRAFT = auction
