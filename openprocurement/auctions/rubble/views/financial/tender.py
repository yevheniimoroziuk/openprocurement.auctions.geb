# -*- coding: utf-8 -*-

from openprocurement.auctions.core.utils import (
    opresource,
)
from openprocurement.auctions.landlease.views.other.tender import (
    AuctionResource,
)


@opresource(name='landleaseFinancial:Auction',
            path='/auctions/{auction_id}',
            auctionsprocurementMethodType="landleaseFinancial",
            description="Open Contracting compatible data exchange format. See http://ocds.open-contracting.org/standard/r/master/#auction for more info")
class FinancialAuctionResource(AuctionResource):
    pass
