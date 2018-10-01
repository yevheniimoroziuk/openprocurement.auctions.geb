from zope.interface import implementer

from openprocurement.auctions.core.interfaces import (
    IAuctioneer
)

from openprocurement.auctions.core.utils import (
    apply_patch,
    get_now
)

from openprocurement.auctions.geb.validation import (
    validate_auction_auction_status,
    validate_auction_identity_of_bids,
    validate_auction_number_of_bids
)


@implementer(IAuctioneer)
class Auctioneer(object):
    name = 'Auctioneer'
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
                return
        return True

    def update_auction_urls(self):
        if self.validate():
            self._context.modified = apply_patch(self._request, save=False, src=self._context.serialize())

    def bring_auction_result(self):
        if self.validate():
            self._context.auctionPeriod = {'endDate': self._now}
            self._context.modified = apply_patch(self._request, save=False, src=self._context.serialize())

    def decide_procedure(self):
        if self._context.modified:
            if any([bid.status == 'active' for bid in self._context.bids]):
                self._request.content_configurator.start_awarding()
            else:
                self._context.status = 'unsuccessful'
