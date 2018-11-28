from openprocurement.auctions.core.managers import (
    AuctionManager,
    BidManager,
    BidDocumentManager,
    DocumentManager,
    ItemManager,
    CancellationManager,
    QuestionManager
)

from openprocurement.auctions.geb.managers.changers import (
    AuctionChanger,
    BidPatchChanger,
    BidDocumentPatchChanger,
    CancellationPatchChanger,
    ChronographChanger,
    ItemPatchChanger,
    ModuleAuctionChanger,
    QuestionPatchChanger,
    AuctionDocumentPatchChanger,
    AuctionDocumentPutChanger
)
from openprocurement.auctions.geb.managers.representers import (
    AuctionSubResourceRepresenter,
    BidRepresenter,
    CancellationRepresenter,
    CancellationSubResourceRepresenter,
    ItemRepresenter
)

from openprocurement.auctions.geb.managers.creators import (
    Creator
)
from openprocurement.auctions.geb.managers.deleters import (
    BidDeleter
)

from openprocurement.auctions.geb.managers.loggers import (
    AuctionLogger,
    BidLogger,
    CancellationLogger,
    ItemLogger
)
from openprocurement.auctions.core.adapters import (
    AuctionManagerAdapter
)


class AuctionManager(AuctionManager):
    creator = Creator
    logger = AuctionLogger
    subResourceRepresenter = AuctionSubResourceRepresenter

    @property
    def changer(self):
        if self._request.authenticated_role == 'auction':
            return ModuleAuctionChanger
        if self._request.authenticated_role == 'chronograph':
            return ChronographChanger
        return AuctionChanger


class BidManager(BidManager):
    changer = BidPatchChanger
    Deleter = BidDeleter
    Creator = Creator
    Representer = BidRepresenter
    Logger = BidLogger


class BidDocumentManager(BidDocumentManager):
    changer = BidDocumentPatchChanger


class QuestionManager(QuestionManager):
    Changer = QuestionPatchChanger


class ItemManager(ItemManager):
    changer = ItemPatchChanger
    Representer = ItemRepresenter
    Logger = ItemLogger
    Creator = Creator


class CancellationManager(CancellationManager):
    Creator = Creator
    changer = CancellationPatchChanger
    Representer = CancellationRepresenter
    Logger = CancellationLogger
    SubResourceRepresenter = CancellationSubResourceRepresenter


class AuctionDocumentManager(DocumentManager):

    @property
    def changer(self):
        if self._request.method == 'PUT':
            return AuctionDocumentPutChanger
        return AuctionDocumentPatchChanger


class AuctionPartialManager(AuctionManagerAdapter):
    pass
