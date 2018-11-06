from zope.interface import implementedBy
from openprocurement.auctions.core.utils import (
    json_view,
    opresource,
    APIResource
)

from openprocurement.auctions.core.validation import (
    validate_item_data,
    validate_patch_item_data
)

from openprocurement.auctions.core.interfaces import (
    IAuctionManager,
    IItemManager
)


@opresource(name='geb:Auction Items',
            collection_path='/auctions/{auction_id}/items',
            path='/auctions/{auction_id}/items/{item_id}',
            description="Auction items")
class AuctionItemResource(APIResource):

    @json_view(permission='view_auction')
    def collection_get(self):
        """Auction Item List"""

        manager = self.request.registry.queryMultiAdapter((self.request, self.context), IAuctionManager)
        item_type = type(manager.context).items.model_class
        return manager.represent_subresources_listing(implementedBy(item_type))

    @json_view(content_type="application/json", permission='create_item', validators=(validate_item_data))
    def collection_post(self):
        """
        Auction Item Upload
        """
        save = None

        applicant = self.request.validated['item']
        manager = self.request.registry.queryMultiAdapter((self.request, self.context), IAuctionManager)
        item = manager.create(applicant)
        save = manager.save()

        if save:
            msg = 'Create auction item {}'.format(item['id'])
            manager.log_action('auction_item_create', msg)
            return manager.represent_subresource_created(item)

    @json_view(permission='view_auction')
    def get(self):
        """
        Auction Item Read
        """
        manager = self.request.registry.queryMultiAdapter((self.request, self.context), IItemManager)
        return manager.represent(self.request.method)

    @json_view(content_type="application/json", permission='edit_auction', validators=(validate_patch_item_data))
    def patch(self):
        """
        Auction Item Change
        """
        manager = self.request.registry.queryMultiAdapter((self.request, self.context), IItemManager)

        manager.change()
        save = manager.save()

        if save:
            msg = 'Updated auction item {}'.format(manager.context.id)
            manager.log_action('auction_item_patch', msg)
            return manager.represent(self.request.method)
