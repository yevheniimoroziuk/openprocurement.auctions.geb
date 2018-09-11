from zope.interface import implementer

from openprocurement.auctions.landlease.interfaces import (
    IAuctionChanger,
    IBidChanger
)

from openprocurement.auctions.core.utils import (
    apply_patch,
)

from openprocurement.auctions.landlease.validation import (
    validate_change_bid_check_auction_status,
    validate_change_bid_check_status,
    validate_make_active_status_bid
)


@implementer(IAuctionChanger)
class AuctionChanger(object):
    name = 'Auction Changer'

    def __init__(self, request, context):
        self._request = request
        self._context = context

    def change(self):
        return apply_patch(self._request, save=False, src=self._request.validated['auction_src'])


@implementer(IBidChanger)
class BidChanger(object):
    name = 'Bid Changer'
    validators = [validate_change_bid_check_auction_status,
                  validate_change_bid_check_status,
                  validate_make_active_status_bid]

    def __init__(self, request, context):
        self._request = request
        self._context = context

    def validate(self):
        for validator in self.validators:
            if not validator(self._request):
                return
        return True

    def change(self):
        if self.validate():
            return apply_patch(self._request, save=False, src=self._context.serialize())
