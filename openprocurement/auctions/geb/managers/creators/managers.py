from openprocurement.auctions.geb.managers.creators.base import (
    BaseCreationManager,
)

from openprocurement.auctions.geb.managers.creators.creators import (
    AuctionCreator,
    AuctionDocumentCreator,
    BidDocumentCreator,
    CancellationCreator,
    CancellationDocumentCreator,
    ItemCreator,
    QuestionCreator
)


class AuctionCreationManager(BaseCreationManager):
    creators = (
        AuctionCreator,
        AuctionDocumentCreator,
        CancellationCreator,
        ItemCreator,
        QuestionCreator
    )


class CancellationCreationManager(BaseCreationManager):

    creators = (CancellationDocumentCreator, )


class BidCreationManager(BaseCreationManager):
    creators = (BidDocumentCreator, )
