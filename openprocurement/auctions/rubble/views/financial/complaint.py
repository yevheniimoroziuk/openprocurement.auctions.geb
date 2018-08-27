# -*- coding: utf-8 -*-

from openprocurement.auctions.core.utils import (
    opresource,
)
from openprocurement.auctions.landlease.views.other.complaint import (
    AuctionComplaintResource,
)


@opresource(name='landleaseFinancial:Auction Complaints',
            collection_path='/auctions/{auction_id}/complaints',
            path='/auctions/{auction_id}/complaints/{complaint_id}',
            auctionsprocurementMethodType="landleaseFinancial",
            description="Financial auction complaints")
class FinancialAuctionComplaintResource(AuctionComplaintResource):
    pass
