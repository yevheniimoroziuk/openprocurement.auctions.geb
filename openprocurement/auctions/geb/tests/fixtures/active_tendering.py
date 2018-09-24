from copy import deepcopy
from openprocurement.auctions.core.utils import get_now
from openprocurement.auctions.geb.tests.fixtures.active_rectification import ACTIVE_RECTIFICATION_AUCTION_DEFAULT_FIXTURE
from openprocurement.auctions.geb.tests.fixtures.questions import (
    TEST_QESTION_IN_TENDERING_PERIOD
)
from openprocurement.auctions.geb.tests.fixtures.bids import (
    TEST_DRAFT_BID
)
from openprocurement.auctions.geb.tests.fixtures.calculator import (
    Calculator
)

now = get_now()
calculator = Calculator(now, 'tenderingPeriod', 'start')

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
ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE["next_check"] = calculator.rectificationPeriod.endDate.isoformat()
ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE["date"] = calculator.auctionDate.date.isoformat()

# auction with questions fixture

ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE_WITH_QUESTION = deepcopy(ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE)
ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE_WITH_QUESTION['questions'] = [TEST_QESTION_IN_TENDERING_PERIOD]
END_ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE = {}


# auction with bids fixture

ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE_WITH_BIDS = deepcopy(ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE)
ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE_WITH_BIDS['bids'] = [TEST_DRAFT_BID]

# end tendering period fixture

END_ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE = {}
