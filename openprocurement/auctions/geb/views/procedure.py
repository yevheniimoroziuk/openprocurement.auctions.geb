# -*- coding: utf-8 -*-
from openprocurement.auctions.core.utils import (
    context_unpack,
    get_auction_route_name,
    json_view,
    opresource
)
from openprocurement.auctions.core.views.mixins import (
    AuctionResource,
    set_ownership
)
from openprocurement.auctions.core.views.auctions import (
    AuctionsResource
)
from openprocurement.auctions.core.interfaces import (
    IAuctionManager
)
from openprocurement.auctions.core.validation import (
    validate_auction_data
)
from openprocurement.auctions.geb.validation import (
    validate_patch_auction_data
)


@opresource(name='geb:Auction', path='/auctions/{auction_id}', auctionsprocurementMethodType="geb")
class AuctionResource(AuctionResource):

    @json_view(content_type="application/json",
               validators=(validate_patch_auction_data,),
               permission='edit_auction')
    def patch(self):
        check, change, save = None, None, None
        manager = self.request.registry.queryMultiAdapter((self.request, self.context), IAuctionManager)

        if self.request.authenticated_role == 'chronograph':
            check = manager.check()
        else:
            change = manager.change()

        if check or change:
            save = manager.save()

        if save:
            extra = context_unpack(self.request, {'MESSAGE_ID': 'auction_patch'})
            self.LOGGER.info('Updated auction {}'.format(self.context.id), extra=extra)
            return {'data': self.context.serialize(self.context.status)}


#@opresource(name='Auctions', path='/auctions')
#class AuctionsResource(AuctionsResource):
#
#    @json_view(content_type="application/json", permission='create_auction', validators=(validate_auction_data,))
#    def post(self):
#        manager = self.request.registry.queryMultiAdapter((self.request, self.request.validated['auction']), IAuctionManager)
#
#        auction = manager.create()
#        if not auction:
#            return
#        manager.initialize()
#        acc = set_ownership(auction, self.request)                              #
#        save = manager.save()
#
#        self.request.validated['auction'] = auction                             # TODO make more verbose
#        self.request.validated['auction_src'] = {}                              #
#
#        if save:
#            extra = context_unpack(self.request,
#                                   {'MESSAGE_ID': 'auction_create'},
#                                   {'auction_id': auction['id'],
#                                    'auctionID': auction.auctionID})
#
#            log = 'Created auction {} ({})'.format(auction['id'], auction.auctionID)
#            self.LOGGER.info(log, extra=extra)
#            self.request.response.status = 201
#            route = get_auction_route_name(self.request, auction)
#            location = self.request.route_url(route_name=route, auction_id=auction['id'])
#            self.request.response.headers['Location'] = location
#            return {'data': auction.serialize(auction.status), 'access': acc}
