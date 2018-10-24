# -*- coding: utf-8 -*-
from zope.interface import implementedBy
from openprocurement.auctions.core.utils import (
    APIResource,
    json_view,
    opresource
)
from openprocurement.auctions.core.interfaces import (
    IAuctionManager,
    ICancellationManager
)
from openprocurement.auctions.core.validation import (
    validate_cancellation_data,
)
from openprocurement.auctions.geb.validation import (
    validate_patch_auction_data
)


@opresource(name='geb:Auction Cancellations',
            collection_path='/auctions/{auction_id}/cancellations',
            path='/auctions/{auction_id}/cancellations/{cancellation_id}',
            auctionsprocurementMethodType="geb",
            description="Auction cancellations")
class AuctionCancellationResource(APIResource):

    @json_view(content_type="application/json", validators=(validate_cancellation_data,), permission='edit_auction')
    def collection_post(self):
        """
        Auction Cancellations
        """
        save = None

        manager = self.request.registry.queryMultiAdapter((self.request, self.context), IAuctionManager)

        applicant = self.request.validated['cancellation']
        cancellation = manager.create(applicant)
        save = manager.save()

        if save:
            msg = 'Create auction cancellation {}'.format(cancellation['id'])
            manager.log_action('auction_cancellation_create', msg)
            return manager.represent_subresource_created(cancellation)

    @json_view(permission='view_auction')
    def collection_get(self):
        """Auction Cancellations List"""

        manager = self.request.registry.queryMultiAdapter((self.request, self.context), IAuctionManager)
        cancellation_type = type(manager.context).cancellations.model_class
        return manager.represent_subresources_listing(implementedBy(cancellation_type))

    @json_view(permission='view_auction')
    def get(self):
        """
        Auction Cancellation Get
        """
        manager = self.request.registry.queryMultiAdapter((self.request, self.context), ICancellationManager)
        return manager.represent(self.request.method)

    @json_view(content_type="application/json", validators=(validate_patch_auction_data,),
               permission='edit_auction')
    def patch(self):
        """
        Patch the cancellation
        """
        manager = self.request.registry.queryMultiAdapter((self.request, self.context), ICancellationManager)

        manager.change()
        save = manager.save()

        if save:
            msg = 'Updated auction cancellation {}'.format(manager.context.id)
            manager.log_action('auction_cancellation_patch', msg)
            return manager.represent(self.request.method)
