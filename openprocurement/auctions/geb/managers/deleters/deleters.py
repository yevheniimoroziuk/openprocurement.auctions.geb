from openprocurement.auctions.geb.managers.deleters.base import (
    BaseResourceDeleter
)
from openprocurement.auctions.geb.validation import (
    validate_bid_delete
)


class BidDeleter(BaseResourceDeleter):
    validators = (
        validate_bid_delete,
    )

    def _delete(self):
        auction = self.request.auction
        auction.bids.remove(self.context)
        return self.context

    def delete(self):
        if self.validate():
            return self._delete()
        return False
