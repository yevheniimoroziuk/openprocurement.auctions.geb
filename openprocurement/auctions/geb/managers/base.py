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

from openprocurement.auctions.geb.managers.representers.representers import (
    ItemRepresenter
)
from openprocurement.auctions.geb.managers.representers.managers import (
    AuctionRepresentationManager,
    BidRepresentationManager,
    CancellationRepresentationManager
)

from openprocurement.auctions.geb.managers.changers.managers import (
    AuctionChangionManager,
    AuctionDocumentChangionManager,
    BidChangionManager,
    BidDocumentChangionManager,
    ItemChangionManager,
    QuestionChangionManager
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
    changion_manager = AuctionChangionManager
    representation_manager = AuctionRepresentationManager
    logger = AuctionLogger


class BidManager(BidManager):
    changion_manager = BidChangionManager
    creation_manager = BidCreationManager
    Deleter = BidDeleter
    representation_manager = BidRepresentationManager
    Logger = BidLogger


class BidDocumentManager(BidDocumentManager):
    changion_manager = BidDocumentChangionManager


class QuestionManager(QuestionManager):
    changion_manager = QuestionChangionManager


class ItemManager(ItemManager):
    changion_manager = ItemChangionManager
    Representer = ItemRepresenter
    Logger = ItemLogger


class CancellationManager(CancellationManager):
    creation_manager = CancellationCreationManager
    log = CancellationLogger
    representation_manager = CancellationRepresentationManager


class CancellationDocumentManager(CancellationDocumentManager):
    logger = CancellationDocumentLogger


class AuctionDocumentManager(DocumentManager):
    changion_manager = AuctionDocumentChangionManager


class AuctionPartialManager(AuctionManagerAdapter):
    pass
