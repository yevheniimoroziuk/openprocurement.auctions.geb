from openprocurement.auctions.geb.managers.creators.base import (
    BaseAuctionCreationManager,
    BaseSubAuctionCreationManager
)

from openprocurement.auctions.geb.managers.creators.creators import (
    AuctionCreator,
    AuctionDocumentCreator,
    CancellationCreator,
    CancellationDocumentCreator,
    ItemCreator,
    QuestionCreator
)


class AuctionCreationManager(BaseAuctionCreationManager):
    creators = (
        AuctionCreator,
        AuctionDocumentCreator,
        CancellationCreator,
        ItemCreator,
        QuestionCreator
    )


class CancellationCreationManager(BaseSubAuctionCreationManager):

    creators = (CancellationDocumentCreator, )
