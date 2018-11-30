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
from openprocurement.auctions.geb.managers.representers import (
    BidRepresenter,
    CancellationRepresenter,
    ItemRepresenter,
    CancellationDocumentRepresenter,
    CancellationListingRepresenter,
    CancellationCreatedRepresenter
)

from openprocurement.auctions.geb.managers.creators import (
    AuctionCreator,
    CancellationCreator,

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
    creator = AuctionCreator
    logger = AuctionLogger

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


class CancellationManager(CancellationManager):
    creator = CancellationCreator
    changer = CancellationPatchChanger
    Representer = CancellationRepresenter
    log = CancellationLogger
    listing_representer = CancellationListingRepresenter
    created_representer = CancellationCreatedRepresenter


class CancellationDocumentManager(CancellationDocumentManager):
    representer = CancellationDocumentRepresenter
    logger = CancellationDocumentLogger


class AuctionDocumentManager(DocumentManager):

    @property
    def changer(self):
        if self._request.method == 'PUT':
            return AuctionDocumentPutChanger
        return AuctionDocumentPatchChanger


class AuctionPartialManager(AuctionManagerAdapter):
    pass
