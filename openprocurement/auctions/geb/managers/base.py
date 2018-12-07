from openprocurement.auctions.core.managers import (
    AuctionManager,
    BidManager,
    BidDocumentManager,
    CancellationDocumentManager,
    DocumentManager,
    ItemManager,
    CancellationManager,
    QuestionManager
)
from openprocurement.auctions.core.adapters import (
    AuctionManagerAdapter
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
from openprocurement.auctions.geb.managers.representers.representers import (
    ItemRepresenter
)
from openprocurement.auctions.geb.managers.representers.managers import (
    AuctionRepresentationManager,
    BidRepresentationManager,
    CancellationRepresentationManager
)

from openprocurement.auctions.geb.managers.creators.managers import (
    AuctionCreationManager,
    BidCreationManager,
    CancellationCreationManager

)
from openprocurement.auctions.geb.managers.deleters import (
    BidDeleter
)

from openprocurement.auctions.geb.managers.loggers import (
    AuctionLogger,
    BidLogger,
    CancellationLogger,
    ItemLogger,
    CancellationDocumentLogger
)


class AuctionManager(AuctionManager):
    creation_manager = AuctionCreationManager
    representation_manager = AuctionRepresentationManager
    logger = AuctionLogger

    @property
    def changer(self):
        if self.request.authenticated_role == 'auction':
            return ModuleAuctionChanger
        if self.request.authenticated_role == 'chronograph':
            return ChronographChanger
        return AuctionChanger


class BidManager(BidManager):
    changer = BidPatchChanger
    creation_manager = BidCreationManager
    Deleter = BidDeleter
    representation_manager = BidRepresentationManager
    Logger = BidLogger


class BidDocumentManager(BidDocumentManager):
    changer = BidDocumentPatchChanger


class QuestionManager(QuestionManager):
    Changer = QuestionPatchChanger


class ItemManager(ItemManager):
    changer = ItemPatchChanger
    Representer = ItemRepresenter
    Logger = ItemLogger


class CancellationManager(CancellationManager):
    creation_manager = CancellationCreationManager
    changer = CancellationPatchChanger
    log = CancellationLogger
    representation_manager = CancellationRepresentationManager


class CancellationDocumentManager(CancellationDocumentManager):
    logger = CancellationDocumentLogger


class AuctionDocumentManager(DocumentManager):

    @property
    def changer(self):
        if self.request.method == 'PUT':
            return AuctionDocumentPutChanger
        return AuctionDocumentPatchChanger


class AuctionPartialManager(AuctionManagerAdapter):
    pass
