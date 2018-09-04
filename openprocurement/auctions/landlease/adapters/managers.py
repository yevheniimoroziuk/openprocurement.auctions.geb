from openprocurement.auctions.core.adapters import (
    AuctionManagerAdapter as BaseAuctionManagerAdapter
)


class AuctionManagerAdapter(BaseAuctionManagerAdapter):

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
