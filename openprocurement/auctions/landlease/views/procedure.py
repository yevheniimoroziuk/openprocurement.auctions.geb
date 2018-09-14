# -*- coding: utf-8 -*-
from openprocurement.auctions.core.utils import (
    context_unpack,
    json_view,
    opresource
)
from openprocurement.auctions.core.views.mixins import AuctionResource
from openprocurement.auctions.core.interfaces import (
    IAuctionManager
)
from openprocurement.auctions.landlease.interfaces import (
    IAuctionChanger,
    IAuctionChecker
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
        check, change, save = None, None, None
        manager = self.request.registry.queryMultiAdapter((self.request, self.context), IAuctionManager)

        if self.request.authenticated_role == 'chronograph':
            checker = self.request.registry.getAdapter(self.context, IAuctionChecker)
            check = manager.check(checker)
        else:
            changer = self.request.registry.queryMultiAdapter((self.request, self.context), IAuctionChanger)
            change = manager.change(changer)

        if check or change:
            save = manager.save()

        if save:
            extra = context_unpack(self.request, {'MESSAGE_ID': 'auction_patch'})
            self.LOGGER.info('Updated auction {}'.format(self.context.id), extra=extra)
            return {'data': self.context.serialize(self.context.status)}
