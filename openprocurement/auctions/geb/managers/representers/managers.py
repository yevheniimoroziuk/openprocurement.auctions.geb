
from openprocurement.auctions.geb.managers.representers.base import (
    BaseRepresentationManager
)
from openprocurement.auctions.geb.managers.representers.representers import (
    AuctionDocumentCreatedRepresenter,
    AuctionListingCancellationRepresenter,
    AuctionListingItemRepresenter,
    BidRepresenter,
    CancellationCreatedRepresenter,
    CancellationDocumentCreatedRepresenter,
    CancellationListingDocumentRepresenter,
    CancellationRepresenter,
    ItemCreatedRepresenter,
    ItemRepresenter
)

# listing representers


class AuctionRepresentationManager(BaseRepresentationManager):

    listing_representers = (
        AuctionListingItemRepresenter,
        AuctionListingCancellationRepresenter,
    )
    created_representers = (
        AuctionDocumentCreatedRepresenter,
        CancellationCreatedRepresenter,
        ItemCreatedRepresenter
    )


class BidRepresentationManager(BaseRepresentationManager):
    representer = BidRepresenter


class CancellationRepresentationManager(BaseRepresentationManager):

    listing_representers = (
        CancellationListingDocumentRepresenter,
    )
    created_representers = (
        CancellationDocumentCreatedRepresenter,
    )
    representer = CancellationRepresenter


class ItemRepresentationManager(BaseRepresentationManager):

    representer = ItemRepresenter
