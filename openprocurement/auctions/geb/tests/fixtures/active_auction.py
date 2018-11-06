from uuid import uuid4
from copy import deepcopy
from openprocurement.auctions.geb.tests.fixtures.active_enquiry import (
    AUCTION as ACTIVE_ENQUIRY_AUCTION
)

from openprocurement.auctions.geb.tests.fixtures.cancellations import (
    CANCELLATION,
    CANCELLATION_WITH_DOCUMENTS
)
from openprocurement.auctions.geb.tests.fixtures.bids import (
    BID_ACTIVE_FIRST
)
from openprocurement.auctions.core.utils import get_now
from openprocurement.auctions.geb.tests.fixtures.calculator import (
    Calculator
)

now = get_now()
calculator = Calculator(now, 'auctionPeriod', 'start')
auction = deepcopy(ACTIVE_ENQUIRY_AUCTION)
auction['status'] = 'active.auction'
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

# auction in 'active.auction' status.
# description:
# - has item
# - two bids in status 'active'
# - minNumberOfQualifiedBids = 2
# - value.amount = 100
# - minimalStep.amount = 42
# - owner = 'broker'
AUCTION = auction

auction = deepcopy(AUCTION)
auction['auctionUrl'] = 'http://auction-sandbox.openprocurement.org/auctions/{}'.format(auction['_id'])
for bid in auction['bids']:
    bid['participationUrl'] = "http://auction-sandbox.openprocurement.org/auctions/{}?key_for_bid={}".format(auction['_id'], bid['id'])

# auction in 'active.auction' with module auction urls.
AUCTION_WITH_URLS = auction

# auction in end 'active.auction'
END_ACTIVE_AUCTION_AUCTION = {}

# auction with cancellations
auction = deepcopy(AUCTION)
auction['_id'] = uuid4().hex
auction['cancellations'] = [CANCELLATION]
AUCTION_WITH_CANCELLATION = auction

# auction with bid in status 'active' and cancellation
auction = deepcopy(AUCTION)
auction['_id'] = uuid4().hex
auction['cancellations'] = [CANCELLATION]
auction['bids'] = [BID_ACTIVE_FIRST]
AUCTION_WITH_BIDS_WITH_CANCELLATION = auction

# auction with cancellations with document fixture
auction = deepcopy(AUCTION)
auction['_id'] = uuid4().hex
auction['cancellations'] = [CANCELLATION_WITH_DOCUMENTS]
AUCTION_WITH_CANCELLATION_WITH_DOCUMENTS = auction
