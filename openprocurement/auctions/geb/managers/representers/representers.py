from openprocurement.auctions.geb.constants import (
    AUCTION_STATUSES_FOR_FORBIDDEN_GET_BIDS
)
from openprocurement.auctions.geb.interfaces import (
    IAuctionDocument,
    IBid,
    ICancellation,
    ICancellationDocument,
    IItem,
    IQuestion
)
from openprocurement.auctions.geb.managers.representers.base import (
    BaseCreatedRepresenter,
    BaseListingRepresenter,
    BaseResourceRepresenter
)

# resources representers


class ItemRepresenter(BaseResourceRepresenter):

    def get_representation_role(self):
        return "view"


class BidRepresenter(BaseResourceRepresenter):

    def get_representation_role(self):
        if self.request.method == 'PATCH':
            return self.context.status
        elif self.request.method == 'GET':

            # bid owner always get bid
            if self.request.authenticated_role == 'bid_owner':
                return 'view'

            # only after auction is over, anybody can get bid
            auction = self.request.auction
            if auction.status in AUCTION_STATUSES_FOR_FORBIDDEN_GET_BIDS:
                err_msg = 'Can\'t view bid in current ({}) auction status'.format(auction.status)
                self.request.errors.add('body', 'data', err_msg)
                self.request.errors.status = 403

            return auction.status

        return 'view'


class CancellationRepresenter(BaseResourceRepresenter):

    def get_representation_role(self):
        return "view"

# created representers


class CancellationDocumentCreatedRepresenter(BaseCreatedRepresenter):
    resource_interface = ICancellationDocument

    def represent(self, document):
        self.request.response.status = 201
        route = self.request.matched_route.name.replace("collection_", "")
        location = self.request.current_route_url(_route_name=route, document_id=document['id'], _query={})
        self.request.response.headers['Location'] = location

        return {'data': self.context.serialize('view')}


class CancellationCreatedRepresenter(BaseCreatedRepresenter):
    resource_interface = ICancellation

    def represent(self, cancellation):
        self.request.response.status = 201
        route = self.request.matched_route.name.replace("collection_", "")
        location = self.request.current_route_url(_route_name=route, cancellation_id=cancellation['id'], _query={})
        self.request.response.headers['Location'] = location

        return {'data': self.context.serialize('view')}


class ItemCreatedRepresenter(BaseCreatedRepresenter):
    resource_interface = IItem

    def represent(self, item):
        self.request.response.status = 201
        route = self.request.matched_route.name.replace("collection_", "")
        location = self.request.current_route_url(_route_name=route, item_id=item['id'], _query={})
        self.request.response.headers['Location'] = location

        return {'data': self.context.serialize('view')}


class AuctionDocumentCreatedRepresenter(BaseCreatedRepresenter):
    resource_interface = IAuctionDocument

    def represent(self, document):
        self.request.response.status = 201
        route = self.request.matched_route.name.replace("collection_", "")
        location = self.request.current_route_url(_route_name=route, document_id=document['id'], _query={})
        self.request.response.headers['Location'] = location

        return {'data': self.context.serialize('view')}


class BidCreatedRepresenter(BaseCreatedRepresenter):
    resource_interface = IBid

    def represent(self, bid):
        self.request.response.status = 201
        route = self.request.matched_route.name.replace("collection_", "")
        location = self.request.current_route_url(_route_name=route, bid_id=bid['id'], _query={})
        self.request.response.headers['Location'] = location

        return {'data': self.context.serialize('view')}


class QuestionCreatedRepresenter(BaseCreatedRepresenter):
    resource_interface = IQuestion

    def represent(self, question):
        self.request.response.status = 201
        route = self.request.matched_route.name.replace("collection_", "")
        location = self.request.current_route_url(_route_name=route, question_id=question['id'], _query={})
        self.request.response.headers['Location'] = location

        return {'data': self.context.serialize('view')}

# listing representers


class AuctionListingItemRepresenter(BaseListingRepresenter):
    """
        Auction Items listing representer
    """
    resource_interface = IItem

    def represent(self):
        collection_data = [item.serialize("view") for item in self.context.items]
        return {'data': collection_data}


class AuctionListingCancellationRepresenter(BaseListingRepresenter):
    """
        Auction Cancellations listing representer
    """
    resource_interface = ICancellation

    def represent(self):
        collection_data = [cancellation.serialize("view") for cancellation in self.context.cancellations]
        return {'data': collection_data}


class CancellationListingDocumentRepresenter(BaseListingRepresenter):
    """
        Cancellation Document listing representer
    """
    resource_interface = ICancellationDocument

    def represent(self):
        collection_data = [document.serialize("view") for document in self.context.documents]
        return {'data': collection_data}
