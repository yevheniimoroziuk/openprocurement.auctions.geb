from zope.interface import implementer, providedBy

from openprocurement.auctions.core.interfaces import (
    IAuctionSubResourceCancellationRepresenter,
    IAuctionSubResourceItemRepresenter,
    IAuctionSubResourcesRepresenter,
    IAuctionSubResourcesRepresentersFactory,
    IBidRepresenter,
    ICancellationRepresenter,
    ICancellationSubResourceDocumentRepresenter,
    ICancellationSubResourcesRepresenter,
    ICancellationSubResourcesRepresentersFactory,
    IItemRepresenter
)

from openprocurement.auctions.geb.interfaces import (
    IItem,
    ICancellation,
    ICancellationDocument
)

from openprocurement.auctions.geb.constants import (
    AUCTION_STATUSES_FOR_FORBIDDEN_GET_BIDS
)
# resources representers

# Item resource representer


@implementer(IItemRepresenter)
class ItemRepresenter(object):
    name = 'Item Representer'

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

# Bid resource representer


@implementer(IBidRepresenter)
class BidRepresenter(object):
    name = 'Bid Representer'

    def __init__(self, request, context):
        self._request = request
        self._context = context

    def _represent_patch(self):
        return {'data': self._context.serialize(self._context.status)}

    def _represent_get(self):
        # bid owner always get bid
        if self._request.authenticated_role == 'bid_owner':
            return {'data': self._context.serialize('view')}

        auction_status = self._request.validated['auction_status']

        # only after auction is over, anybody can get bid
        if auction_status in AUCTION_STATUSES_FOR_FORBIDDEN_GET_BIDS:
            err_msg = 'Can\'t view bid in current ({}) auction status'.format(auction_status)
            self._request.errors.add('body', 'data', err_msg)
            self._request.errors.status = 403

        return {'data': self._context.serialize(auction_status)}

    def _represent_delete(self):
        return {'data': self._context.serialize("view")}

    def represent(self, method, listing=False):
        if method == 'PATCH':
            return self._represent_patch()
        elif method == 'GET':
                return self._represent_get()
        elif method == 'DELETE':
                return self._represent_delete()


@implementer(ICancellationRepresenter)
class CancellationRepresenter(object):
    name = 'Cancellatin Representer'

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

# auction sub-resources representers


@implementer(IAuctionSubResourceItemRepresenter)
class AuctionSubResourceItemRepresenter(object):
    resource_interface = IItem

    def represent_created(self, request, item):
        request.response.status = 201
        route = request.matched_route.name.replace("collection_", "")
        location = request.current_route_url(_route_name=route, item_id=item['id'], _query={})
        request.response.headers['Location'] = location
        return {'data': item.serialize("view")}

    def represent_listing(self, auction):
        collection_data = [item.serialize("view") for item in auction.items]
        return {'data': collection_data}


@implementer(IAuctionSubResourceCancellationRepresenter)
class AuctionSubResourceCancellationRepresenter(object):
    resource_interface = ICancellation

    def represent_created(self, request, cancellation):
        request.response.status = 201
        route = request.matched_route.name.replace("collection_", "")
        location = request.current_route_url(_route_name=route, cancellation_id=cancellation['id'], _query={})
        request.response.headers['Location'] = location
        return {'data': cancellation.serialize("view")}

    def represent_listing(self, auction):
        collection_data = [cancellation.serialize("view") for cancellation in auction.cancellations]
        return {'data': collection_data}

# auction sub-resource representer factory


@implementer(IAuctionSubResourcesRepresentersFactory)
class AuctionSubResourcesRepresentersFactory():
    representers = (
        AuctionSubResourceItemRepresenter,
        AuctionSubResourceCancellationRepresenter,

    )

    def __call__(self, implamented):
        for Representer in self.representers:
            if Representer.resource_interface in implamented:
                return Representer()

# cancellation sub-resources representers


@implementer(ICancellationSubResourceDocumentRepresenter)
class CancellationSubResourceDocumentRepresenter(object):
    resource_interface = ICancellationDocument

    def represent_created(self, request, document):
        request.response.status = 201
        route = request.matched_route.name.replace("collection_", "")
        locations = request.current_route_url(_route_name=route, document_id=document.id, _query={})
        request.response.headers['Location'] = locations
        return {'data': document.serialize("view")}

    def represent_listing(self, cancellation):
        collection_data = [document.serialize("view") for document in cancellation.documents]
        return {'data': collection_data}

# cancellation sub-resource representer factory


@implementer(ICancellationSubResourcesRepresentersFactory)
class CancellationSubResourcesRepresentersFactory():
    representers = (
        CancellationSubResourceDocumentRepresenter,
    )

    def __call__(self, implamented):
        for Representer in self.representers:
            if Representer.resource_interface in implamented:
                return Representer()

# auction sub-resource representer


@implementer(IAuctionSubResourcesRepresenter)
class AuctionSubResourceRepresenter(object):
    name = 'Auction SubResource Representer'
    factory = AuctionSubResourcesRepresentersFactory

    def __init__(self, request, context):
        self._request = request
        self._context = context

    def represent_created(self, resource):
        factory = self.factory()
        representer = factory(providedBy(resource))
        return representer.represent_created(self._request, resource)

    def represent_listing(self, resource_implamented):
        factory = self.factory()
        representer = factory(resource_implamented)
        return representer.represent_listing(self._context)


# cancellation sub-resource representer

@implementer(ICancellationSubResourcesRepresenter)
class CancellationSubResourceRepresenter(object):
    name = 'Cancellation SubResource Representer'
    factory = CancellationSubResourcesRepresentersFactory

    def __init__(self, request, context):
        self._request = request
        self._context = context

    def represent_created(self, resource):
        factory = self.factory()
        representer = factory(providedBy(resource))
        return representer.represent_created(self._request, resource)

    def represent_listing(self, resource_implamented):
        factory = self.factory()
        representer = factory(resource_implamented)
        return representer.represent_listing(self._context)
