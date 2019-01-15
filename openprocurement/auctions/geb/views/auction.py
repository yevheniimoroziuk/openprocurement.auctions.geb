# -*- coding: utf-8 -*-
from openprocurement.auctions.core.utils import (
    json_view,
    context_unpack,
    opresource
)
from openprocurement.auctions.core.views.mixins import (
    APIResource
)
from openprocurement.auctions.geb.validation import (
    validate_patch_resource_data
)
from openprocurement.auctions.core.interfaces import (
    IAuctionManager
)


@opresource(name='geb:Auction Auction',
            path='/auctions/{auction_id}/auction',
            auctionsprocurementMethodType="geb")
class AuctionAuctionResource(APIResource):

    @json_view(content_type="application/json", permission='auction', validators=(validate_patch_resource_data))
    def post(self):
        manager = self.request.registry.queryMultiAdapter((self.request, self.context), IAuctionManager)

        manager.auction_report()
        manager.award()

        save = manager.save()
        if save:
            extra = context_unpack(self.request, {'MESSAGE_ID': 'auction_auction_post'})
            self.LOGGER.info('Report auction results', extra=extra)
            return {'data': self.request.validated['auction'].serialize("auction_view")}

    @json_view(permission='auction')
    def get(self):
        if self.request.validated['auction_status'] not in ('active.auction', 'active.qualification'):
            self.request.errors.add('body', 'data', 'Can\'t get auction info in current ({}) auction status'.format(
                self.request.validated['auction_status']))
            self.request.errors.status = 403
            return
        return {'data': self.request.validated['auction'].serialize("auction_view")}

    @json_view(content_type="application/json", permission='auction', validators=(validate_patch_resource_data,))
    def patch(self):
        manager = self.request.registry.queryMultiAdapter((self.request, self.context), IAuctionManager)

        manager.update_auction_urls()
        save = manager.save()

        if save:
            extra = context_unpack(self.request, {'MESSAGE_ID': 'auction_auction_patch'})
            self.LOGGER.info('Updated auction urls', extra=extra)
            return {'data': self.request.validated['auction'].serialize("auction_view")}
