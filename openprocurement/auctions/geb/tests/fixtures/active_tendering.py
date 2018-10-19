from uuid import uuid4
from copy import deepcopy
from openprocurement.auctions.core.utils import get_now
from openprocurement.auctions.geb.tests.fixtures.active_rectification import (
    AUCTION as ACTIVE_RECTIFICATION_AUCTION,
)
from openprocurement.auctions.geb.tests.fixtures.questions import (
    TEST_QESTION_IN_TENDERING_PERIOD
)
from openprocurement.auctions.geb.tests.fixtures.bids import (
    DRAFT_BID,
    PENDING_BID_FIRST,
    ACTIVE_BID_FIRST,
    ACTIVE_BID_SECOND,
    DRAFT_BID_WITH_DOCUMENT,
    PENDING_BID_FIRST_WITH_DOCUMENT,
    ACTIVE_BID_FIRST_WITH_DOCUMENT
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

# blank auction fixture

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
    "shouldStartAfter": calculator.auctionPeriod.shouldStartAfter.isoformat()
}
auction["next_check"] = calculator.tenderPeriod.endDate.isoformat()
auction["date"] = calculator.auctionDate.date.isoformat()

AUCTION = auction

# auction with questions fixture

auction = deepcopy(AUCTION)
auction['questions'] = [TEST_QESTION_IN_TENDERING_PERIOD]

AUCTION_WITH_QUESTIONS = auction


# auction with bids

auction = deepcopy(AUCTION)
auction['bids'] = [DRAFT_BID]

AUCTION_WITH_DRAFT_BID = auction

auction = deepcopy(AUCTION)
auction['bids'] = [PENDING_BID_FIRST]

AUCTION_WITH_PENDING_BID = auction

auction = deepcopy(AUCTION)
auction['bids'] = [ACTIVE_BID_FIRST]

AUCTION_WITH_ACTIVE_BID = auction

# auction with bids with document

auction = deepcopy(AUCTION)
auction['bids'] = [DRAFT_BID_WITH_DOCUMENT]

AUCTION_WITH_DRAFT_BID_WITH_DOCUMENT = auction

auction = deepcopy(AUCTION)
auction['bids'] = [PENDING_BID_FIRST_WITH_DOCUMENT]

AUCTION_WITH_PENDING_BID_WITH_DOCUMENT = auction

auction = deepcopy(AUCTION)
auction['bids'] = [ACTIVE_BID_FIRST_WITH_DOCUMENT]

AUCTION_WITH_ACTIVE_BID_WITH_DOCUMENT = auction


# end tendering period fixtures

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
    "shouldStartAfter": calculator.auctionPeriod.shouldStartAfter.isoformat()
}
auction["next_check"] = calculator.enquiryPeriod.endDate.isoformat()
auction["date"] = calculator.auctionDate.date.isoformat()

END_ACTIVE_TENDERING_AUCTION = auction


# end tendering period with one bid fixture

auction = deepcopy(END_ACTIVE_TENDERING_AUCTION)
auction['bids'] = [ACTIVE_BID_FIRST]

END_ACTIVE_TENDERING_AUCTION_WITH_ONE_BID = auction

# end tendering period with two bid fixture

auction = deepcopy(END_ACTIVE_TENDERING_AUCTION)
auction['bids'] = [ACTIVE_BID_FIRST, ACTIVE_BID_SECOND]

END_ACTIVE_TENDERING_AUCTION_WITH_TWO_BIDS = auction

# end tendering period with two bids and one draft bid

auction = deepcopy(END_ACTIVE_TENDERING_AUCTION)
auction['bids'] = [ACTIVE_BID_FIRST, ACTIVE_BID_SECOND, DRAFT_BID]

END_ACTIVE_TENDERING_AUCTION_WITH_TWO_BIDS_AND_ONE_DRAFT = auction


# auction with cancellations fixture

auction = deepcopy(AUCTION)
auction['_id'] = uuid4().hex
auction['cancellations'] = [
    CANCELLATION
]
AUCTION_WITH_CANCELLATION = auction

# auction with bids and cancellation

auction = deepcopy(AUCTION)
auction['_id'] = uuid4().hex
auction['cancellations'] = [
    CANCELLATION
]
auction['bids'] = [ACTIVE_BID_FIRST, ACTIVE_BID_SECOND]

AUCTION_WITH_BIDS_WITH_CANCELLATION = auction

# auction with cancellations with document fixture

auction = deepcopy(AUCTION)
auction['_id'] = uuid4().hex
auction['cancellations'] = [
    CANCELLATION_WITH_DOCUMENTS
]
AUCTION_WITH_CANCELLATION_WITH_DOCUMENTS = auction
