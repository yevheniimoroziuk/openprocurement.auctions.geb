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

ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE = deepcopy(ACTIVE_RECTIFICATION_AUCTION_DEFAULT_FIXTURE)
ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE['status'] = 'active.tendering'
ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE["rectificationPeriod"] = {
    "startDate": calculator.rectificationPeriod.startDate.isoformat(),
    "endDate": calculator.rectificationPeriod.endDate.isoformat()
}
ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE["tenderPeriod"] = {
    "startDate": calculator.tenderPeriod.startDate.isoformat(),
    "endDate": calculator.tenderPeriod.endDate.isoformat()
}
ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE["enquiryPeriod"] = {
                  "startDate": calculator.enquiryPeriod.startDate.isoformat(),
                  "endDate": calculator.enquiryPeriod.endDate.isoformat()
}
ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE["auctionPeriod"] = {
    "shouldStartAfter": calculator.auctionPeriod.shouldStartAfter.isoformat()
}
ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE["next_check"] = calculator.tenderPeriod.endDate.isoformat()
ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE["date"] = calculator.auctionDate.date.isoformat()

# auction with questions fixture

ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE_WITH_QUESTION = deepcopy(ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE)
ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE_WITH_QUESTION['questions'] = [TEST_QESTION_IN_TENDERING_PERIOD]


# auction with bids fixture

ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE_WITH_BIDS = deepcopy(ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE)
ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE_WITH_BIDS['bids'] = [TEST_DRAFT_BID]

# end tendering period fixtures

calculator = Calculator(now, 'tenderPeriod', 'end')

END_ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE = deepcopy(ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE)

END_ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE["rectificationPeriod"] = {
    "startDate": calculator.rectificationPeriod.startDate.isoformat(),
    "endDate": calculator.rectificationPeriod.endDate.isoformat()
}
END_ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE["tenderPeriod"] = {
    "startDate": calculator.tenderPeriod.startDate.isoformat(),
    "endDate": calculator.tenderPeriod.endDate.isoformat()
}
END_ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE["enquiryPeriod"] = {
                  "startDate": calculator.enquiryPeriod.startDate.isoformat(),
                  "endDate": calculator.enquiryPeriod.endDate.isoformat()
}
END_ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE["auctionPeriod"] = {
    "shouldStartAfter": calculator.auctionPeriod.shouldStartAfter.isoformat()
}
END_ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE["next_check"] = calculator.enquiryPeriod.endDate.isoformat()
END_ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE["date"] = calculator.auctionDate.date.isoformat()


# end tendering period with bids fixture

END_ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE_WITH_ONE_BID = deepcopy(END_ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE)
END_ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE_WITH_ONE_BID['bids'] = [TEST_ACTIVE_BID_FIRST]

END_ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE_WITH_TWO_BIDS = deepcopy(END_ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE)
END_ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE_WITH_TWO_BIDS['bids'] = [TEST_ACTIVE_BID_FIRST, TEST_ACTIVE_BID_SECOND]

END_ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE_WITH_TWO_BIDS_AND_ONE_DRAFT = deepcopy(END_ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE)
END_ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE_WITH_TWO_BIDS_AND_ONE_DRAFT['bids'] = [TEST_ACTIVE_BID_FIRST, TEST_ACTIVE_BID_SECOND, TEST_DRAFT_BID]
