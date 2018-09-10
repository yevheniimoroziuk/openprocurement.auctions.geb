# -*- coding: utf-8 -*-
from openprocurement.auctions.core.utils import (
    context_unpack,
    json_view,
    opresource,
)
from openprocurement.auctions.core.views.mixins import AuctionResource
from openprocurement.auctions.core.interfaces import (
    IAuctionManager,
    IAuctionChanger
)

from openprocurement.auctions.landlease.validation import (
    validate_patch_auction_data
)


@opresource(name='landlease:Auction',
            path='/auctions/{auction_id}',
            auctionsprocurementMethodType="landlease")
class AuctionResource(AuctionResource):

    @json_view(content_type="application/json",
               validators=(validate_patch_auction_data,),
               permission='edit_auction')
    def patch(self):
        manager = self.request.registry.getAdapter(self.context, IAuctionManager)
        changer = self.request.registry.queryMultiAdapter((self.request, self.context), IAuctionChanger)
        manager.change(changer)
        self.LOGGER.info('Updated auction {}'.format(self.context.id), extra=context_unpack(self.request, {'MESSAGE_ID': 'auction_patch'}))
        return {'data': self.context.serialize(self.context.status)}
