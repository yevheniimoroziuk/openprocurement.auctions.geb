from copy import deepcopy
from openprocurement.auctions.core.utils import get_now
from openprocurement.auctions.geb.tests.fixtures.active_rectification import (
    ACTIVE_RECTIFICATION_AUCTION_DEFAULT_FIXTURE
)
from openprocurement.auctions.geb.tests.fixtures.questions import (
    TEST_QESTION_IN_TENDERING_PERIOD
)
from openprocurement.auctions.geb.tests.fixtures.bids import (
    TEST_DRAFT_BID,
    TEST_ACTIVE_BID_FIRST,
    TEST_ACTIVE_BID_SECOND
)
from openprocurement.auctions.geb.tests.fixtures.calculator import (
    Calculator
)

now = get_now()
calculator = Calculator(now, 'tenderPeriod', 'start')

# blank auction fixture

auction = deepcopy(ACTIVE_RECTIFICATION_AUCTION_DEFAULT_FIXTURE)

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

ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE = auction

# auction with questions fixture

auction = deepcopy(ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE)
auction['questions'] = [TEST_QESTION_IN_TENDERING_PERIOD]

ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE_WITH_QUESTION = auction


# auction with bids fixture

auction = deepcopy(ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE)
auction['bids'] = [TEST_DRAFT_BID]

ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE_WITH_BIDS = auction

# end tendering period fixtures

calculator = Calculator(now, 'tenderPeriod', 'end')

auction = deepcopy(ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE)

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

END_ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE = auction


# end tendering period with one bid fixture

auction = deepcopy(END_ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE)
auction['bids'] = [TEST_ACTIVE_BID_FIRST]

END_ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE_WITH_ONE_BID = auction

# end tendering period with two bid fixture

auction = deepcopy(END_ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE)
auction['bids'] = [TEST_ACTIVE_BID_FIRST, TEST_ACTIVE_BID_SECOND]

END_ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE_WITH_TWO_BIDS = auction

# end tendering period with two bids and one draft bid

auction = deepcopy(END_ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE)
auction['bids'] = [TEST_ACTIVE_BID_FIRST, TEST_ACTIVE_BID_SECOND, TEST_DRAFT_BID]

END_ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE_WITH_TWO_BIDS_AND_ONE_DRAFT = auction
