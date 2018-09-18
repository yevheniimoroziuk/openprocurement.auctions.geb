# -*- coding: utf-8 -*-
from openprocurement.auctions.core.utils import (
    json_view,
    context_unpack,
    save_auction,
    apply_patch,
    opresource,
    cleanup_bids_for_cancelled_lots
)
from openprocurement.auctions.core.validation import (
    validate_auction_auction_data,
)
from openprocurement.auctions.core.views.mixins import APIResource

from openprocurement.auctions.geb.utils import (
    invalidate_bids_under_threshold
)


@opresource(name='geb:Auction Auction',
            path='/auctions/{auction_id}/auction',
            auctionsprocurementMethodType="geb",
            description="auction auction data")
class AuctionAuctionResource(APIResource):

    @json_view(content_type="application/json", permission='auction', validators=(validate_auction_auction_data))
    def post(self):
        apply_patch(self.request, save=False, src=self.request.validated['auction_src'])
        auction = self.request.validated['auction']
        invalidate_bids_under_threshold(auction)
        if any([i.status == 'active' for i in auction.bids]):
            self.request.content_configurator.start_awarding()
        else:
            auction.status = 'unsuccessful'
        if save_auction(self.request):
            self.LOGGER.info('Report auction results', extra=context_unpack(self.request, {'MESSAGE_ID': 'auction_auction_post'}))
            return {'data': self.request.validated['auction'].serialize(self.request.validated['auction'].status)}

    @json_view(permission='auction')
    def get(self):
        if self.request.validated['auction_status'] != 'active.auction':
            self.request.errors.add('body', 'data', 'Can\'t get auction info in current ({}) auction status'.format(
                self.request.validated['auction_status']))
            self.request.errors.status = 403
            return
        return {'data': self.request.validated['auction'].serialize("auction_view")}

    @json_view(content_type="application/json", permission='auction', validators=(validate_auction_auction_data))
    def patch(self):
        import ipdb; ipdb.set_trace()  # XXX BREAKPOINT
        if apply_patch(self.request, src=self.request.validated['auction_src']):
            self.LOGGER.info('Updated auction urls',
                             extra=context_unpack(self.request, {'MESSAGE_ID': 'auction_auction_patch'}))
            return {'data': self.request.validated['auction'].serialize("auction_view")}
