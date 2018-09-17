# -*- coding: utf-8 -*-
from openprocurement.auctions.core.utils import (
    opresource,
    json_view,
    context_unpack
)
from openprocurement.auctions.core.views.mixins import AuctionBidDocumentResource
from openprocurement.auctions.core.validation import (
    validate_file_upload
)

from openprocurement.auctions.core.interfaces import (
    IBidManager
)


@opresource(name='geb:Auction Bid Documents',
            collection_path='/auctions/{auction_id}/bids/{bid_id}/documents',
            path='/auctions/{auction_id}/bids/{bid_id}/documents/{document_id}',
            auctionsprocurementMethodType="geb",
            description="Auction bidder documents")
class AuctionBidDocumentResource(AuctionBidDocumentResource):

    @json_view(validators=(validate_file_upload,), permission='edit_bid')
    def collection_post(self):
        """Auction Bid Document Upload
        """
        save = None

        manager = self.request.registry.queryMultiAdapter((self.request, self.context), IBidManager)

        document = manager.upload_document()

        if document:
            save = manager.save()

        if save:
            msg = 'Created auction bid document {}'.format(document.id)
            extra = context_unpack(self.request, {'MESSAGE_ID': 'auction_bid_document_create'}, {'document_id': document['id']})
            self.LOGGER.info(msg, extra=extra)

            self.request.response.status = 201

            route = self.request.matched_route.name.replace("collection_", "")
            locations = self.request.current_route_url(_route_name=route, document_id=document.id, _query={})
            self.request.response.headers['Location'] = locations
            return {'data': document.serialize("view")}
