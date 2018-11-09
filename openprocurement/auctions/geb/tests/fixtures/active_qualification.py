from datetime import timedelta
from copy import deepcopy
from openprocurement.auctions.geb.tests.fixtures.active_auction import (
    AUCTION as ACTIVE_AUCTION_AUCTION
)

from openprocurement.auctions.core.utils import get_now

from openprocurement.auctions.geb.tests.fixtures.calculator import (
    Calculator
)
from openprocurement.auctions.geb.tests.fixtures.awards import (
    AWARD_PENDING,
    AWARD_PENDING_WITH_PROTOCOL
)
from openprocurement.auctions.geb.tests.fixtures.documents import (
    AUCTION_DOCUMENT_AUDIT
)
from openprocurement.auctions.geb.utils import (
    calculate_certainly_business_date as ccbd
)


qualification_period_start = ccbd(get_now(), -timedelta(days=1), specific_hour=16)
calculator = Calculator(qualification_period_start, 'qualificationPeriod', 'start')
auction = deepcopy(ACTIVE_AUCTION_AUCTION)
auction['status'] = 'active.qualification'
auction['documents'] = [AUCTION_DOCUMENT_AUDIT]
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
auction['bids'][1]['status'] = 'invalid'
auction["awards"] = [AWARD_PENDING]
auction["awards"][0]['bid_id'] = auction['bids'][0]['id']
auction["date"] = calculator.auctionDate.date.isoformat()
participation_url_pattern = 'http://auction-sandbox.openprocurement.org/auctions/{}?key_for_bid={}'

url = participation_url_pattern.format(auction['_id'], auction['bids'][0]['id'])
auction['bids'][0]['participationUrl'] = url

url = participation_url_pattern.format(auction['_id'], auction['bids'][1]['id'])
auction['bids'][1]['participationUrl'] = url

# auction in 'active.qualification' status.
# description:
# - has item
# - first bid is winner and has status 'active'
# - second bid is loser and has status 'invalid'
# - has award for first bid
# - minNumberOfQualifiedBids = 2
# - value.amount = 100
# - minimalStep.amount = 42
# - owner = 'broker'
AUCTION = auction

# auction with award with protocol
auction = deepcopy(AUCTION)
auction["awards"] = [AWARD_PENDING_WITH_PROTOCOL]
auction["awards"][0]['bid_id'] = auction['bids'][0]['id']
AUCTION_WITH_AWARD_WITH_PROTOCOL = auction
