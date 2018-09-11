from openprocurement.auctions.core.utils import (
    save_auction,
    apply_patch
)


class AuctionManager(object):
    name = 'Auction Manager'

    def __inti__(self, request, context):
        self._request = request
        self._context = context

    def initialize(self, initializator):
        self._initializator = initializator
        self._initializator.initialize()

    def change(self, changer):
        self._changer = changer
        if self._changer.change():
            self.save()

    def check(self, checker):
        apply_patch(self._request, save=False, src=self._request.validated['auction_src'])
        self._checker = checker
        self._checker.check()
        self.save()

    def save(self):
        save_auction(self._request)


class BidManager(object):
    name = 'Bid Manager'

    def __init__(self, request, context):
        self._request = request
        self._context = context

    def initialize(self, initializator):
        if self._request.validated['json_data'].get('status') == 'pending':
            initializator.initialize()

    def change(self, changer):
        self._changer = changer
        return self._changer.change()

    def save(self):
        save_auction(self._request)
