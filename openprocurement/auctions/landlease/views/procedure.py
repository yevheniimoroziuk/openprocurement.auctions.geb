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
        """Auction Edit (partial)

        For example here is how procuring entity can change number of items to be procured and total Value of a auction:

        .. sourcecode:: http

            PATCH /auctions/4879d3f8ee2443169b5fbbc9f89fa607 HTTP/1.1
            Host: example.com
            Accept: application/json

            {
                "data": {
                    "value": {
                        "amount": 600
                    },
                    "itemsToBeProcured": [
                        {
                            "quantity": 6
                        }
                    ]
                }
            }

        And here is the response to be expected:

        .. sourcecode:: http

            HTTP/1.0 200 OK
            Content-Type: application/json

            {
                "data": {
                    "id": "4879d3f8ee2443169b5fbbc9f89fa607",
                    "auctionID": "UA-64e93250be76435397e8c992ed4214d1",
                    "dateModified": "2014-10-27T08:12:34.956Z",
                    "value": {
                        "amount": 600
                    },
                    "itemsToBeProcured": [
                        {
                            "quantity": 6
                        }
                    ]
                }
            }

        """
        manager = self.request.registry.getAdapter(self.context, IAuctionManager)
        changer = self.request.registry.queryMultiAdapter((self.request, self.context), IAuctionChanger)
        manager.change(changer)
        self.LOGGER.info('Updated auction {}'.format(self.context.id), extra=context_unpack(self.request, {'MESSAGE_ID': 'auction_patch'}))
        return {'data': self.context.serialize(self.context.status)}
