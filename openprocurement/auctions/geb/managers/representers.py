from zope.interface import implementer

from openprocurement.auctions.core.interfaces import (
    IItemRepresenter,
    IAuctionSubResourcesRepresenter,
    IAuctionSubResourceItemRepresenter,
    IAuctionSubResourcesRepresentersFactory
)

from openprocurement.auctions.geb.interfaces import (
    IItem
)


@implementer(IItemRepresenter)
class ItemRepresenter(object):
    name = 'Auction Representer'

    def __init__(self, context):
        self._context = context

    def _represent_patch(self):
        return {'data': self._context.serialize("view")}

    def _represent_get(self):
        return {'data': self._context.serialize("view")}

    def represent(self, method, listing=False):
        if method == 'PATCH':
            return self._represent_patch()
        elif method == 'GET':
                return self._represent_get()


@implementer(IAuctionSubResourceItemRepresenter)
class AuctionSubResourceItemRepresenter(object):
    resource_type = 'item'

    def represent_created(self, request, item):
        request.response.status = 201
        route = self.request.matched_route.name.replace("collection_", "")
        location = self.request.current_route_url(_route_name=route, item_id=item['id'], _query={})
        self.request.response.headers['Location'] = location
        return {'data': item.serialize("view")}

    def represent_listing(self, auction):
        collection_data = [item.serialize("view") for item in auction.items]
        return {'data': collection_data}


@implementer(IAuctionSubResourcesRepresentersFactory)
class AuctionSubResourcesRepresentersFactory():
    representers = (AuctionSubResourceItemRepresenter,)

    def __call__(self, resource_type):
        for Representer in self.representers:
            if IItem.implementedBy(resource_type):
                return Representer()


@implementer(IAuctionSubResourcesRepresenter)
class AuctionSubResourceRepresenter(object):
    name = 'Auction SubResource Representer'
    factory = AuctionSubResourcesRepresentersFactory

    def __init__(self, request, context):
        self._request = request
        self._context = context

    def represent_created(self, resource):
        factory = self.factory()
        representer = factory(type(self.resource))
        return representer.represent_created(self._reuqest, resource)

    def represent_listing(self, resource_type):
        factory = self.factory()
        representer = factory(resource_type)
        return representer.represent_listing(self._context)
