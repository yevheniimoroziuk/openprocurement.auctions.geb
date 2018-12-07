
from openprocurement.auctions.geb.managers.representers.base import (
    BaseRepresentationManager
)
from openprocurement.auctions.geb.managers.representers.representers import (
    AuctionDocumentCreatedRepresenter,
    AuctionListingCancellationRepresenter,
    AuctionListingItemRepresenter,
    BidRepresenter,
    CancellationDocumentCreatedRepresenter,
    CancellationListingDocumentRepresenter,
    CancellationRepresenter
)

# listing representers


class AuctionRepresentationManager(BaseRepresentationManager):
    """
        Auction listings representer
    """
    listing_representers = (
        AuctionListingItemRepresenter,
        AuctionListingCancellationRepresenter,
    )
    created_representers = (
        AuctionDocumentCreatedRepresenter,
    )


class BidRepresentationManager(BaseRepresentationManager):
    """
        Bid representer
    """
    representer = BidRepresenter


class CancellationRepresentationManager(BaseRepresentationManager):
    """
        Cancellation listings representer
    """
    listing_representers = (
        CancellationListingDocumentRepresenter,
    )
    created_representers = (
        CancellationDocumentCreatedRepresenter,
    )
    representer = CancellationRepresenter
