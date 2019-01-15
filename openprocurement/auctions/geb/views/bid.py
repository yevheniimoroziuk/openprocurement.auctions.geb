# -*- coding: utf-8 -*-
from openprocurement.auctions.core.utils import (
    opresource,
    json_view
)
from openprocurement.auctions.core.views.mixins import AuctionBidResource
from openprocurement.auctions.core.validation import (
    validate_patch_bid_data
)
from openprocurement.auctions.core.interfaces import (
    IBidManager
)


@opresource(name='geb:Auction Bids',
            collection_path='/auctions/{auction_id}/bids',
            path='/auctions/{auction_id}/bids/{bid_id}',
            auctionsprocurementMethodType="geb",
            description="Auction bids")
class AuctionBidResource(AuctionBidResource):

    @json_view(content_type="application/json", permission='edit_bid', validators=(validate_patch_bid_data,))
    def patch(self):
        save = None

        manager = self.request.registry.queryMultiAdapter((self.request, self.context), IBidManager)

        manager.change()
        manager.initialize()
        save = manager.save()

        if save:
            msg = 'Updated auction bid {}'.format(manager.context.id)
            manager.log_action('auction_bid_patch', msg)
            return manager.represent(self.request.method)

    @json_view(permission='view_auction')
    def get(self):
        """
        Auction Bid Get
        """
        manager = self.request.registry.queryMultiAdapter((self.request, self.context), IBidManager)
        return manager.represent(self.request.method)

    @json_view(permission='edit_bid')
    def delete(self):
        save = None

        manager = self.request.registry.queryMultiAdapter((self.request, self.context), IBidManager)

        manager.delete()
        save = manager.save()

        if save:
            msg = 'Delete auction bid {}'.format(manager.context.id)
            manager.log_action('auction_bid_delete', msg)
            return manager.represent(self.request.method)
