# -*- coding: utf-8 -*-
from zope.interface import implementedBy
from openprocurement.auctions.core.utils import (
    json_view
)
from openprocurement.auctions.core.validation import (
    validate_file_upload
)
from openprocurement.auctions.core.interfaces import (
    ICancellationManager
)
from openprocurement.auctions.core.utils import opresource
from openprocurement.auctions.core.views.mixins import (
    AuctionCancellationDocumentResource
)


@opresource(name='geb:Auction Cancellation Documents',
            collection_path='/auctions/{auction_id}/cancellations/{cancellation_id}/documents',
            path='/auctions/{auction_id}/cancellations/{cancellation_id}/documents/{document_id}',
            auctionsprocurementMethodType="geb",
            description="Auction cancellation documents")
class AuctionCancellationDocumentResource(AuctionCancellationDocumentResource):

    @json_view(permission='view_auction')
    def collection_get(self):
        """Auction Cancellation Documents List"""

        manager = self.request.registry.queryMultiAdapter((self.request, self.context), ICancellationManager)
        document_type = type(manager.context).documents.model_class
        return manager.represent_subresources_listing(implementedBy(document_type))

        collection_data = [i.serialize("view") for i in self.context.documents]
        return {'data': collection_data}

    @json_view(validators=(validate_file_upload,), permission='edit_auction')
    def collection_post(self):
        """
        Auction Cancellation Document Upload
        """
        save = None

        manager = self.request.registry.queryMultiAdapter((self.request, self.context), ICancellationManager)
        document = manager.upload_document()
        save = manager.save()

        if save:
            msg = 'Create auction cancellation document {}'.format(document['id'])
            manager.log_action('auction_cancellation_document_create', msg)
            return manager.represent_subresource_created(document)
