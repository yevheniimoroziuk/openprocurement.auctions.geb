from zope.interface import implementer

from openprocurement.auctions.core.interfaces import (
    IBidDeleter,
)

from openprocurement.auctions.geb.validation import (
    validate_bid_delete_auction_period,
    validate_bid_delete_period
)


@implementer(IBidDeleter)
class BidDeleter(object):
    name = 'Bid Deleter'
    validators = (
        validate_bid_delete_auction_period,
        validate_bid_delete_period
    )

    def __init__(self, request, context):
        self._request = request
        self._context = context
        self._auction = context.__parent__

    def _validate(self, status):
        for validator in self.validators:
            if not validator(self._request, auction=self._auction, bid=self._context):
                return False
        return True

    def delete(self):
        if self._validate(self._context.status):
            self._auction.bids.remove(self._context)
            self._auction.modified = True
            return self._context
