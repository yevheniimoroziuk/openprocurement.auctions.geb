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
from openprocurement.auctions.geb.managers.documenters import (
    AuctionDocumenter,
    BidDocumenter,
    CancellationDocumenter
)
from openprocurement.auctions.geb.managers.questioners import (
    AuctionQuestioner
)
from openprocurement.auctions.geb.managers.itemers import (
    AuctionItemer
)
from openprocurement.auctions.geb.managers.cancellers import (
    AuctionCanceller
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
    AuctionCreator
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
    Creator = AuctionCreator
    Documenter = AuctionDocumenter
    Initializator = AuctionInitializator
    Questioner = AuctionQuestioner
    Itemer = AuctionItemer
    Logger = AuctionLogger
    Canceller = AuctionCanceller
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


class CancellationManager(CancellationManager):
    Changer = CancellationChanger
    Representer = CancellationRepresenter
    Logger = CancellationLogger
    Documenter = CancellationDocumenter
    SubResourceRepresenter = CancellationSubResourceRepresenter


class DocumentManager(DocumentManager):
    Changer = DocumentChanger
