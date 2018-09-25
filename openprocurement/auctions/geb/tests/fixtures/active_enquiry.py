from copy import deepcopy
from openprocurement.auctions.geb.tests.fixtures.active_tendering import (
    END_ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE_WITH_TWO_BIDS
)
from openprocurement.auctions.geb.tests.fixtures.questions import (
    TEST_QESTION_IN_TENDERING_PERIOD
)
from openprocurement.auctions.geb.tests.fixtures.bids import (
    TEST_PENDING_BID
)
from openprocurement.auctions.core.utils import get_now
from openprocurement.auctions.geb.tests.fixtures.calculator import (
    Calculator
)

now = get_now()
calculator = Calculator(now, 'enquiryPeriod', 'start')

# auction with tow active bids

ACTIVE_ENQUIRY_AUCTION_DEFAULT_FIXTURE = deepcopy(END_ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE_WITH_TWO_BIDS)
ACTIVE_ENQUIRY_AUCTION_DEFAULT_FIXTURE['status'] = 'active.enquiry'
ACTIVE_ENQUIRY_AUCTION_DEFAULT_FIXTURE["rectificationPeriod"] = {
    "startDate": calculator.rectificationPeriod.startDate.isoformat(),
    "endDate": calculator.rectificationPeriod.endDate.isoformat()
}
ACTIVE_ENQUIRY_AUCTION_DEFAULT_FIXTURE["tenderPeriod"] = {
    "startDate": calculator.tenderPeriod.startDate.isoformat(),
    "endDate": calculator.tenderPeriod.endDate.isoformat()
}
ACTIVE_ENQUIRY_AUCTION_DEFAULT_FIXTURE["enquiryPeriod"] = {
                  "startDate": calculator.enquiryPeriod.startDate.isoformat(),
                  "endDate": calculator.enquiryPeriod.endDate.isoformat()
}
ACTIVE_ENQUIRY_AUCTION_DEFAULT_FIXTURE["auctionPeriod"] = {
    "shouldStartAfter": calculator.auctionPeriod.shouldStartAfter.isoformat()
}
ACTIVE_ENQUIRY_AUCTION_DEFAULT_FIXTURE["next_check"] = calculator.rectificationPeriod.endDate.isoformat()
ACTIVE_ENQUIRY_AUCTION_DEFAULT_FIXTURE["date"] = calculator.auctionDate.date.isoformat()

# end tendering period fixtures

END_ACTIVE_ENQUIRY_AUCTION_DEFAULT_FIXTURE = {}


# auction with questions fixture

ACTIVE_ENQUIRY_AUCTION_DEFAULT_FIXTURE_WITH_QUESTION = deepcopy(END_ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE_WITH_TWO_BIDS)
ACTIVE_ENQUIRY_AUCTION_DEFAULT_FIXTURE_WITH_QUESTION['questions'] = [TEST_QESTION_IN_TENDERING_PERIOD]

# auction with bids

ACTIVE_ENQUIRY_AUCTION_DEFAULT_FIXTURE_WITH_NOT_ACTIVE_BID = deepcopy(ACTIVE_ENQUIRY_AUCTION_DEFAULT_FIXTURE)
ACTIVE_ENQUIRY_AUCTION_DEFAULT_FIXTURE_WITH_NOT_ACTIVE_BID['bids'].append(TEST_PENDING_BID)
