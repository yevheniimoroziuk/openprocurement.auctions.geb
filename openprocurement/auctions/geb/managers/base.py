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

from openprocurement.auctions.geb.managers.representers.managers import (
    AuctionRepresentationManager,
    BidRepresentationManager,
    CancellationRepresentationManager,
    ItemRepresentationManager
)

from openprocurement.auctions.geb.managers.changers.managers import (
    AuctionChangionManager,
    AuctionDocumentChangionManager,
    BidChangionManager,
    BidDocumentChangionManager,
    CancellationChangionManager,
    ItemChangionManager,
    QuestionChangionManager
)
from openprocurement.auctions.geb.managers.creators.managers import (
    AuctionCreationManager,
    BidCreationManager,
    CancellationCreationManager

)
from openprocurement.auctions.geb.managers.deleters.managers import (
    BidDeletionManager
)

from openprocurement.auctions.geb.managers.loggers.loggers import (
    AuctionLogger,
    BidLogger,
    CancellationLogger,
    ItemLogger,
    CancellationDocumentLogger
)


class AuctionManager(AuctionManager):
    creation_manager = AuctionCreationManager
    changion_manager = AuctionChangionManager
    representation_manager = AuctionRepresentationManager
    log = AuctionLogger


class BidManager(BidManager):
    changion_manager = BidChangionManager
    creation_manager = BidCreationManager
    deletion_manager = BidDeletionManager
    representation_manager = BidRepresentationManager
    log = BidLogger


class BidDocumentManager(BidDocumentManager):
    changion_manager = BidDocumentChangionManager


class QuestionManager(QuestionManager):
    changion_manager = QuestionChangionManager


class ItemManager(ItemManager):
    changion_manager = ItemChangionManager
    representation_manager = ItemRepresentationManager
    log = ItemLogger


class CancellationManager(CancellationManager):
    creation_manager = CancellationCreationManager
    changion_manager = CancellationChangionManager
    representation_manager = CancellationRepresentationManager
    log = CancellationLogger


class CancellationDocumentManager(CancellationDocumentManager):
    log = CancellationDocumentLogger


class AuctionDocumentManager(DocumentManager):
    changion_manager = AuctionDocumentChangionManager


class AuctionPartialManager(AuctionManagerAdapter):
    pass
