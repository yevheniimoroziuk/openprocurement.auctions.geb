from zope.interface import implementer

from openprocurement.auctions.core.interfaces import (
    IAuctioneer
)

from openprocurement.auctions.core.utils import (
    apply_patch,
    get_now
)

from openprocurement.auctions.geb.managers.initializators import (
    AuctionReportInitializator
)
from openprocurement.auctions.geb.validation import (
    validate_auction_auction_status,
    validate_auction_identity_of_bids,
    validate_auction_number_of_bids
)


@implementer(IAuctioneer)
class Auctioneer(object):
    name = 'Auctioneer'
    initializator = AuctionReportInitializator

    validators = [validate_auction_auction_status,
                  validate_auction_number_of_bids,
                  validate_auction_identity_of_bids]

    def __init__(self, request, context):
        self._now = get_now()
        self._request = request
        self._context = context

    def validate(self):
        for validator in self.validators:
            if not validator(self._request):
                return False
        return True

    def initialize(self):
        initializator = self.initializator(self._request, self._context)
        initializator.initialize()

    def update_auction_urls(self):
        if self.validate():
            self._context.modified = apply_patch(self._request, save=False, src=self._context.serialize())

    def report(self):
        if self.validate():
            self._context.auctionPeriod['endDate'] = self._now
            self._context.modified = apply_patch(self._request, save=False, src=self._context.serialize())
        return self._context.modified

    def award(self):
        if self._context.modified:
            if any([bid.status == 'active' for bid in self._context.bids]):
                return True
            else:
                self._context.status = 'unsuccessful'
