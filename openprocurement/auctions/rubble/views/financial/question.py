# -*- coding: utf-8 -*-

from openprocurement.auctions.core.utils import (
    opresource,
)
from openprocurement.auctions.landlease.views.other.question import (
    AuctionQuestionResource,
)


@opresource(name='landleaseFinancial:Auction Questions',
            collection_path='/auctions/{auction_id}/questions',
            path='/auctions/{auction_id}/questions/{question_id}',
            auctionsprocurementMethodType="landleaseFinancial",
            description="landleaseFinancial:Auction questions")
class FinancialAuctionQuestionResource(AuctionQuestionResource):
    pass
