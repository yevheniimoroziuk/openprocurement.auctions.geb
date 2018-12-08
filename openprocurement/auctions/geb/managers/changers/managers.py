
from openprocurement.auctions.geb.managers.changers.base import (
    BaseChangionManager
)
from openprocurement.auctions.geb.managers.changers.changers import (
    AuctionChanger,
    AuctionDocumentChanger,
    AuctionDocumentPutChanger,
    BidChanger,
    BidDocumentChanger,
    ChronographChanger,
    ItemChanger,
    ModuleAuctionChanger,
    QuestionChanger

)


class AuctionChangionManager(BaseChangionManager):

    @property
    def changer(self):
        if self.request.authenticated_role == 'auction':
            return ModuleAuctionChanger
        if self.request.authenticated_role == 'chronograph':
            return ChronographChanger
        return AuctionChanger


class BidChangionManager(BaseChangionManager):
    changer = BidChanger


class BidDocumentChangionManager(BaseChangionManager):
    changer = BidDocumentChanger


class QuestionChangionManager(BaseChangionManager):
    changer = QuestionChanger


class ItemChangionManager(BaseChangionManager):
    changer = ItemChanger


class AuctionDocumentChangionManager(BaseChangionManager):

    @property
    def changer(self):
        if self.request.method == 'PUT':
            return AuctionDocumentPutChanger
        return AuctionDocumentChanger
