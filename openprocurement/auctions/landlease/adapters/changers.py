from zope.interface import implementer

from openprocurement.auctions.landlease.interfaces import (
    IAuctionChanger,
    IBidChanger
)

from openprocurement.auctions.core.utils import (
    apply_patch,
    save_auction,
)

from openprocurement.auctions.landlease.validation import (
    validate_change_bid_check_auction_status,
    validate_change_bid_check_status
)


@implementer(IAuctionChanger)
class AuctionChanger(object):
    name = 'Auction Changer'

    def __init__(self, request, context):
        self._request = request
        self._context = context

    def change(self):
        patch = apply_patch(self._request, save=False, src=self._request.validated['auction_src'])
        if patch:
            save_auction(self._request)


@implementer(IBidChanger)
class BidChanger(object):
    name = 'Bid Changer'
    validators = [validate_change_bid_check_auction_status,
                  validate_change_bid_check_status]

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

    def save(self):
        return save_auction(self._request)
