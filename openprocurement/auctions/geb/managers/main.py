from openprocurement.auctions.core.managers import (
    AuctionManager,
    BidManager,
    BidDocumentManager,
    DocumentManager,
    ItemManager,
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
    QuestionChanger
)
from openprocurement.auctions.geb.managers.documenters import (
    AuctionDocumenter,
    BidDocumenter
)
from openprocurement.auctions.geb.managers.questioners import (
    AuctionQuestioner
)
from openprocurement.auctions.geb.managers.itemers import (
    AuctionItemer
)
from openprocurement.auctions.geb.managers.checkers import (
    AuctionChecker
)

from openprocurement.auctions.geb.managers.representers import (
    ItemRepresenter,
    AuctionSubResourceRepresenter
)

from openprocurement.auctions.geb.managers.creators import (
    AuctionCreator
)
from openprocurement.auctions.geb.managers.auctioneers import (
    Auctioneer
)

from openprocurement.auctions.geb.managers.deleters import (
    BidDeleter
)

from openprocurement.auctions.geb.managers.loggers import (
    ItemLogger
)


class AuctionManager(AuctionManager):
    Auctioneer = Auctioneer
    Changer = AuctionChanger
    Checker = AuctionChecker
    Creator = AuctionCreator
    Documenter = AuctionDocumenter
    Initializator = AuctionInitializator
    Questioner = AuctionQuestioner
    Itemer = AuctionItemer
    # Representer = AuctionRepresenter
    SubResourceRepresenter = AuctionSubResourceRepresenter


class BidManager(BidManager):
    Changer = BidChanger
    Deleter = BidDeleter
    Documenter = BidDocumenter
    Initializator = BidInitializator

class BidDocumentManager(BidDocumentManager):
    Changer = BidDocumentChanger

class QuestionManager(QuestionManager):
    Changer = QuestionChanger


class ItemManager(ItemManager):
    Changer = ItemChanger
    Representer = ItemRepresenter
    Logger = ItemLogger


class DocumentManager(DocumentManager):
    Changer = DocumentChanger
