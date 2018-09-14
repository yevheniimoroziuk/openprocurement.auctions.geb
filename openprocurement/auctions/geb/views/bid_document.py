# -*- coding: utf-8 -*-
from openprocurement.auctions.core.utils import opresource
from openprocurement.auctions.core.views.mixins import AuctionBidDocumentResource

from openprocurement.auctions.geb.constants import BID_STATUSES_FOR_ADDING_DOCUMENTS


@opresource(name='geb:Auction Bid Documents',
            collection_path='/auctions/{auction_id}/bids/{bid_id}/documents',
            path='/auctions/{auction_id}/bids/{bid_id}/documents/{document_id}',
            auctionsprocurementMethodType="geb",
            description="Auction bidder documents")
class AuctionBidDocumentResource(AuctionBidDocumentResource):

    def validate_bid_document(self, operation):
        auction = self.request.validated['auction']
        if auction.status not in BID_STATUSES_FOR_ADDING_DOCUMENTS:
            err_msg = 'Can\'t {} document in current ({}) auction status'.format(operation, auction.status)
            self.request.errors.add('body', 'data', err_msg)
            self.request.errors.status = 403
            return
        return True
