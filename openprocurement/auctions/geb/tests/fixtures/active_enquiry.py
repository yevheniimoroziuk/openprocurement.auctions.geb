from copy import deepcopy
from openprocurement.auctions.geb.tests.fixtures.active_tendering import (
    END_ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE_WITH_TWO_BIDS
)
from openprocurement.auctions.geb.tests.fixtures.questions import (
    TEST_QESTION_IN_TENDERING_PERIOD
)
from openprocurement.auctions.geb.tests.fixtures.bids import (
    TEST_PENDING_BID_FIRST,
    TEST_PENDING_BID_SECOND,
    TEST_ACTIVE_BID_FIRST
)
from openprocurement.auctions.core.utils import get_now
from openprocurement.auctions.geb.tests.fixtures.calculator import (
    Calculator
)

now = get_now()
calculator = Calculator(now, 'enquiryPeriod', 'start')

# auction with tow active bids

auction = deepcopy(END_ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE_WITH_TWO_BIDS)
auction['status'] = 'active.enquiry'
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

ACTIVE_ENQUIRY_AUCTION_DEFAULT_FIXTURE = auction

# auction with questions fixture

auction = deepcopy(ACTIVE_ENQUIRY_AUCTION_DEFAULT_FIXTURE)
auction['questions'] = [TEST_QESTION_IN_TENDERING_PERIOD]

ACTIVE_ENQUIRY_AUCTION_DEFAULT_FIXTURE_WITH_QUESTION = auction

# auction with bids

auction = deepcopy(ACTIVE_ENQUIRY_AUCTION_DEFAULT_FIXTURE)
auction['bids'].append(TEST_PENDING_BID_FIRST)

ACTIVE_ENQUIRY_AUCTION_DEFAULT_FIXTURE_WITH_NOT_ACTIVE_BID = auction

# end tendering period fixtures

now = get_now()
calculator = Calculator(now, 'enquiryPeriod', 'end')

auction = deepcopy(END_ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE_WITH_TWO_BIDS)

auction['status'] = 'active.enquiry'

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
auction["next_check"] = None
auction["date"] = calculator.auctionDate.date.isoformat()

END_ACTIVE_ENQUIRY_AUCTION_DEFAULT_FIXTURE = auction

auction = deepcopy(END_ACTIVE_ENQUIRY_AUCTION_DEFAULT_FIXTURE)

auction['bids'] = [TEST_PENDING_BID_FIRST, TEST_PENDING_BID_SECOND]

END_ACTIVE_ENQUIRY_UNSUCCESSFUL_NO_ACTIVE_BIDS = auction

auction = deepcopy(END_ACTIVE_ENQUIRY_AUCTION_DEFAULT_FIXTURE)
auction['bids'] = [TEST_ACTIVE_BID_FIRST]
auction['minNumberOfQualifiedBids'] = 1


END_ACTIVE_ENQUIRY_AUCTION_QUALIFICATION = auction
