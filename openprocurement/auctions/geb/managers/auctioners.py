from zope.interface import implementer

from openprocurement.auctions.core.interfaces import (
    IAuctionAuctioneer
)

from openprocurement.auctions.core.utils import (
    apply_patch,
)

from openprocurement.auctions.geb.validation import (
    validate_auction_number_of_bids
)


@implementer(IAuctionAuctioneer)
class Auctioneer(object):
    name = 'Auction Auctioner'
    validators = [validate_auction_number_of_bids]

    def __init__(self, request, context):
        self._request = request
        self._context = context

    def validate(self):
        for validator in self.validators:
            if not validator(self._request):
                return
        return True

    def update_auction_url(self):
        if self.validate():
            self._context.modified = apply_patch(self._request, save=False, src=self._request.validated['auction_src'])
