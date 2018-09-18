from zope.interface import implementer

from openprocurement.auctions.core.interfaces import (
    IBidDeleter
)

from openprocurement.auctions.geb.validation import (
    check_auction_status_for_deleting_bids
)


@implementer(IBidDeleter)
class BidDeleter(object):
    name = 'Bid Deleter'
    validators = [check_auction_status_for_deleting_bids]

    def __init__(self, request, context):
        self._request = request
        self._context = context
        self._auction = context.__parent__

    def validate(self):
        for validator in self.validators:
            if not validator(self._request):
                return
        return True

    def delete(self):
        self._auction.bids.remove(self._context)
        return self._context
