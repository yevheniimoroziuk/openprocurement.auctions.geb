# -*- coding: utf-8 -*-

from openprocurement.auctions.core.utils import (
    opresource,
)
from openprocurement.auctions.landlease.views.other.cancellation import (
    AuctionCancellationResource,
)


@opresource(name='landleaseFinancial:Auction Cancellations',
            collection_path='/auctions/{auction_id}/cancellations',
            path='/auctions/{auction_id}/cancellations/{cancellation_id}',
            auctionsprocurementMethodType="landleaseFinancial",
            description="Financial auction cancellations")
class FinancialAuctionCancellationResource(AuctionCancellationResource):
    pass
