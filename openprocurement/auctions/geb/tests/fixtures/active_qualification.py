from datetime import timedelta
from copy import deepcopy
from openprocurement.auctions.geb.tests.fixtures.active_enquiry import (
    AUCTION as ACTIVE_ENQUIRY_AUCTION
)

from openprocurement.auctions.core.utils import get_now
from openprocurement.auctions.geb.tests.fixtures.calculator import (
    Calculator
)
from openprocurement.auctions.geb.tests.fixtures.awards import (
    AWARD_PENDING,
    AWARD_PENDING_WITH_PROTOCOL
)
from openprocurement.auctions.geb.tests.fixtures.bids import (
    ACTIVE_BID_FIRST
)
from openprocurement.auctions.geb.utils import (
    calculate_certainly_business_date as ccbd
)


qualification_period_start = ccbd(get_now(), -timedelta(days=1), specific_hour=16)

calculator = Calculator(qualification_period_start, 'qualificationPeriod', 'start')

auction = deepcopy(ACTIVE_ENQUIRY_AUCTION)

auction['status'] = 'active.qualification'
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
    "startDate": calculator.auctionPeriod.startDate.isoformat(),
    "endDate": calculator.auctionPeriod.endDate.isoformat()
}
auction["awardPeriod"] = {
    "startDate": calculator.awardPeriod.startDate.isoformat(),
}

auction["next_check"] = None
auction['bids'] = [ACTIVE_BID_FIRST]
auction["awards"] = [AWARD_PENDING]
auction["awards"][0]['bid_id'] = auction['bids'][0]['id']
auction["date"] = calculator.auctionDate.date.isoformat()

AUCTION = auction

# auction with award with protocol

auction = deepcopy(AUCTION)
auction["awards"] = [AWARD_PENDING_WITH_PROTOCOL]
auction["awards"][0]['bid_id'] = auction['bids'][0]['id']

AUCTION_WITH_AWARD_WITH_PROTOCOL = auction
