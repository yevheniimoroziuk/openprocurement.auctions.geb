# -*- coding: utf-8 -*-

from openprocurement.auctions.core.utils import (
    opresource,
)
from openprocurement.auctions.landlease.views.other.lot import (
    AuctionLotResource,
)


@opresource(name='landleaseFinancial:Auction Lots',
            collection_path='/auctions/{auction_id}/lots',
            path='/auctions/{auction_id}/lots/{lot_id}',
            auctionsprocurementMethodType="landleaseFinancial",
            description="Financial auction lots")
class FinancialAuctionLotResource(AuctionLotResource):
    pass
