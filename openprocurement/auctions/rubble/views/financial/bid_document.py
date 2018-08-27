# -*- coding: utf-8 -*-

from openprocurement.auctions.core.utils import (
    opresource,
)
from openprocurement.auctions.landlease.views.other.bid_document import (
    AuctionBidDocumentResource,
)


@opresource(name='landleaseFinancial:Auction Bid Documents',
            collection_path='/auctions/{auction_id}/bids/{bid_id}/documents',
            path='/auctions/{auction_id}/bids/{bid_id}/documents/{document_id}',
            auctionsprocurementMethodType="landleaseFinancial",
            description="Financial auction bidder documents")
class FinancialAuctionBidDocumentResource(AuctionBidDocumentResource):
    pass
