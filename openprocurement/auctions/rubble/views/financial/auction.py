# -*- coding: utf-8 -*-
from openprocurement.auctions.core.utils import (
    opresource,
)
from openprocurement.auctions.landlease.views.other.auction import (
    AuctionAuctionResource,
)


@opresource(name='landleaseFinancial:Auction Auction',
            collection_path='/auctions/{auction_id}/auction',
            path='/auctions/{auction_id}/auction/{auction_lot_id}',
            auctionsprocurementMethodType="landleaseFinancial",
            description="Financial auction auction data")
class FinancialAuctionAuctionResource(AuctionAuctionResource):
    pass
