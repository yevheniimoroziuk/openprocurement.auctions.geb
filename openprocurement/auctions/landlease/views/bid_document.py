# -*- coding: utf-8 -*-
from openprocurement.auctions.core.utils import opresource
from openprocurement.auctions.core.views.mixins import AuctionBidDocumentResource


@opresource(name='landlease:Auction Bid Documents',
            collection_path='/auctions/{auction_id}/bids/{bid_id}/documents',
            path='/auctions/{auction_id}/bids/{bid_id}/documents/{document_id}',
            auctionsprocurementMethodType="landlease",
            description="Auction bidder documents")
class AuctionBidDocumentResource(AuctionBidDocumentResource):

    def validate_bid_document(self, operation):
        auction = self.request.validated['auction']
        if auction.status not in ['active.tendering', 'active.qualification']:
            self.request.errors.add('body', 'data', 'Can\'t {} document in current ({}) auction status'.format(operation, auction.status))
            self.request.errors.status = 403
            return
        return True
