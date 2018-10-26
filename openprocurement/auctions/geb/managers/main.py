from openprocurement.auctions.core.managers import (
    AuctionManager,
    BidManager,
    BidDocumentManager,
    DocumentManager,
    ItemManager,
    CancellationManager,
    QuestionManager
)

from openprocurement.auctions.geb.managers.initializators import (
    AuctionInitializator,
    BidInitializator
)
from openprocurement.auctions.geb.managers.changers import (
    AuctionChanger,
    BidChanger,
    BidDocumentChanger,
    DocumentChanger,
    ItemChanger,
    CancellationChanger,
    QuestionChanger
)
from openprocurement.auctions.geb.managers.awarding import (
    Awarding
)
from openprocurement.auctions.geb.managers.checkers import (
    AuctionChecker
)

from openprocurement.auctions.geb.managers.representers import (
    ItemRepresenter,
    CancellationRepresenter,
    AuctionSubResourceRepresenter,
    CancellationSubResourceRepresenter,
)

from openprocurement.auctions.geb.managers.creators import (
    Creator
)
from openprocurement.auctions.geb.managers.auctioneers import (
    Auctioneer
)

from openprocurement.auctions.geb.managers.deleters import (
    BidDeleter
)

from openprocurement.auctions.geb.managers.loggers import (
    AuctionLogger,
    CancellationLogger,
    ItemLogger
)


class AuctionManager(AuctionManager):
    Auctioneer = Auctioneer
    Changer = AuctionChanger
    Checker = AuctionChecker
    Creator = Creator
    Initializator = AuctionInitializator
    Logger = AuctionLogger
    Awarding = Awarding
    SubResourceRepresenter = AuctionSubResourceRepresenter


class BidManager(BidManager):
    Changer = BidChanger
    Deleter = BidDeleter
    Initializator = BidInitializator
    Creator = Creator


class BidDocumentManager(BidDocumentManager):
    Changer = BidDocumentChanger


class QuestionManager(QuestionManager):
    Changer = QuestionChanger


class ItemManager(ItemManager):
    Changer = ItemChanger
    Representer = ItemRepresenter
    Logger = ItemLogger
    Creator = Creator


class CancellationManager(CancellationManager):
    Creator = Creator
    Changer = CancellationChanger
    Representer = CancellationRepresenter
    Logger = CancellationLogger
    SubResourceRepresenter = CancellationSubResourceRepresenter


class DocumentManager(DocumentManager):
    Changer = DocumentChanger
