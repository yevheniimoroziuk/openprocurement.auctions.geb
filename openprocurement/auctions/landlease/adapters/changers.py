from zope.interface import implementer

from openprocurement.auctions.landlease.interfaces import (
    IAuctionChanger
)

from openprocurement.auctions.core.utils import (
    apply_patch,
    save_auction,
)


@implementer(IAuctionChanger)
class AuctionChanger(object):
    name = 'Auction Initializator'

    def __init__(self, request, context):
        self._request = request
        self._context = context

    def change(self):
        patch = apply_patch(self._request, save=False, src=self._request.validated['auction_src'])
        if patch:
            save_auction(self._request)
