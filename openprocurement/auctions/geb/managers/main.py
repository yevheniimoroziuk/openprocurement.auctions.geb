from openprocurement.auctions.core.managers import (
    AuctionManager,
    BidManager,
    QuestionManager
)
from openprocurement.auctions.geb.managers.initializators import (
    AuctionInitializator,
    BidInitializator
)
from openprocurement.auctions.geb.managers.changers import (
    AuctionChanger,
    BidChanger,
    QuestionChanger
)
from openprocurement.auctions.geb.managers.documenters import (
    AuctionDocumenter,
    BidDocumenter
)
from openprocurement.auctions.geb.managers.questioners import (
    AuctionQuestioner
)
from openprocurement.auctions.geb.managers.checkers import (
    AuctionChecker
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


class AuctionManager(AuctionManager):
    Auctioneer = Auctioneer
    Changer = AuctionChanger
    Checker = AuctionChecker
    Creator = AuctionCreator
    Documenter = AuctionDocumenter
    Initializator = AuctionInitializator
    Questioner = AuctionQuestioner


class BidManager(BidManager):
    Changer = BidChanger
    Deleter = BidDeleter
    Documenter = BidDocumenter
    Initializator = BidInitializator


class QuestionManager(QuestionManager):
    Changer = QuestionChanger
