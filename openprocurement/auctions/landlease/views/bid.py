# -*- coding: utf-8 -*-
from openprocurement.auctions.core.utils import (
    opresource,
    json_view,
    context_unpack
)
from openprocurement.auctions.core.views.mixins import AuctionBidResource
from openprocurement.auctions.core.validation import (
    validate_patch_bid_data
)
from openprocurement.auctions.landlease.interfaces import (
    IBidManager,
    IBidChanger,
    IBidInitializator
)


@opresource(name='landlease:Auction Bids',
            collection_path='/auctions/{auction_id}/bids',
            path='/auctions/{auction_id}/bids/{bid_id}',
            auctionsprocurementMethodType="landlease",
            description="Auction bids")
class AuctionBidResource(AuctionBidResource):
    pass

    @json_view(content_type="application/json", permission='edit_bid', validators=(validate_patch_bid_data,))
    def patch(self):

        manager = self.request.registry.queryMultiAdapter((self.request, self.context), IBidManager)
        changer = self.request.registry.queryMultiAdapter((self.request, self.context), IBidChanger)
        initializator = self.request.registry.getAdapter(self.context, IBidInitializator)

        if manager.change(changer, initializator):
            manager.initialize(initializator)
            manager.save()

            extra = context_unpack(self.request, {'MESSAGE_ID': 'auction_bid_patch'})
            self.LOGGER.info('Updated auction bid {}'.format(self.request.context.id), extra=extra)
            return {'data': self.request.context.serialize(self.request.context.status)}
