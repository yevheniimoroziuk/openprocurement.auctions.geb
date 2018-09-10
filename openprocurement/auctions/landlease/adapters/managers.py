from openprocurement.auctions.core.adapters import (
    AuctionManagerAdapter as BaseAuctionManagerAdapter
)


class AuctionManager(BaseAuctionManagerAdapter):

    def create_auction(self, request):
        pass

    def change_auction(self, request):
        pass

    def initialize(self, initializator):
        self._initializator = initializator
        self._initializator.initialize()

    def change(self, changer):
        self._changer = changer
        self._changer.change()


class BidManager(object):
    name = 'Bid Manager'

    def __init__(self, context):
        self._context = context

    def change(self, changer, initializator):
        self._changer = changer
        change = self._changer.change()
        if change:
            initializator.initialize()
            return self._changer.save()
