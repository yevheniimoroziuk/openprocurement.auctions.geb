from openprocurement.auctions.geb.managers.deleters.base import (
    BaseDeletionManager
)
from openprocurement.auctions.geb.managers.deleters.deleters import (
    BidDeleter
)


class BidDeletionManager(BaseDeletionManager):
    deleter = BidDeleter
