from copy import deepcopy
from openprocurement.auctions.geb.tests.fixtures.active_enquiry import (
    ACTIVE_ENQUIRY_AUCTION_DEFAULT_FIXTURE
)

from openprocurement.auctions.core.utils import get_now
from openprocurement.auctions.geb.tests.fixtures.calculator import (
    Calculator
)

now = get_now()
calculator = Calculator(now, 'auctionPeriod', 'shouldStartAfter')

auction = deepcopy(ACTIVE_ENQUIRY_AUCTION_DEFAULT_FIXTURE)

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
    "shouldStartAfter": calculator.auctionPeriod.shouldStartAfter.isoformat()
}
auction["next_check"] = calculator.enquiryPeriod.endDate.isoformat()
auction["date"] = calculator.auctionDate.date.isoformat()

ACTIVE_AUCTION_DEFAULT_FIXTURE = auction

auction = deepcopy(ACTIVE_AUCTION_DEFAULT_FIXTURE)
auction['auctionUrl'] = 'http://auction-sandbox.openprocurement.org/auctions/{}'.format(auction['_id'])
for bid in auction['bids']:
    bid['participationUrl'] = "http://auction-sandbox.openprocurement.org/auctions/{}?key_for_bid={}".format(auction['_id'], bid['id'])

ACTIVE_AUCTION_DEFAULT_FIXTURE_WITH_URLS = auction

# end auction
END_AUCTION_AUCTION_DEFAULT_FIXTURE = {}
