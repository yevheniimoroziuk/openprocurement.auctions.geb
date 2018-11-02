from datetime import timedelta
from copy import deepcopy
from openprocurement.auctions.geb.tests.fixtures.active_qualification import (
    AUCTION as ACTIVE_QUALIFICATION_AUCTION
)

from openprocurement.auctions.core.utils import get_now
from openprocurement.auctions.geb.tests.fixtures.calculator import (
    Calculator
)
from openprocurement.auctions.geb.tests.fixtures.awards import (
    AWARD_ACTIVE
)
from openprocurement.auctions.geb.tests.fixtures.contracts import (
    CONTRACT_PENDING,
    CONTRACT_PENDING_WITH_DOCUMENT
)
from openprocurement.auctions.geb.utils import (
    calculate_certainly_business_date as ccbd
)


awarded_period_start = ccbd(get_now(), -timedelta(days=1), specific_hour=17)
calculator = Calculator(awarded_period_start, 'awardPeriod', 'end')

auction = deepcopy(ACTIVE_QUALIFICATION_AUCTION)

auction['status'] = 'active.awarded'
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
    "endDate": calculator.awardPeriod.endDate.isoformat(),
}

auction["next_check"] = None
auction["awards"] = [AWARD_ACTIVE]
auction["awards"][0]['bid_id'] = auction['bids'][0]['id']
auction["contracts"] = [CONTRACT_PENDING]
auction["contracts"][0]['awardID'] = auction['awards'][0]['id']

auction["date"] = calculator.auctionDate.date.isoformat()

AUCTION = auction

# auction with contract with document

auction = deepcopy(AUCTION)
auction["contracts"] = [CONTRACT_PENDING_WITH_DOCUMENT]
auction["contracts"][0]['awardID'] = auction['awards'][0]['id']

AUCTION_WITH_CONTRACT_WITH_DOCUMENT = auction
