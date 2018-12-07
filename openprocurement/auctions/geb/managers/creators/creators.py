from uuid import uuid4

from openprocurement.auctions.core.utils import (
    generate_auction_id,
    get_now
)

from openprocurement.auctions.geb.utils import (
    upload_file
)
from openprocurement.auctions.geb.interfaces import (
    IAuction,
    IAuctionDocument,
    IBidDocument,
    ICancellation,
    ICancellationDocument,
    IItem,
    IQuestion,
)
from openprocurement.auctions.geb.validation import (
    validate_auction_post,
    validate_auction_document_post,
    validate_bid_document_post,
    validate_question_post
)
from openprocurement.auctions.geb.managers.creators.base import (
    BaseCreator
)
from openprocurement.auctions.geb.constants import (
    AUCTION_PARAMETERS_TYPE
)


class AuctionCreator(BaseCreator):
    """
       Auction Creator
    """
    resource_interface = IAuction
    validators = [validate_auction_post]

    def _create(self, auction):
        auction_id = uuid4().hex
        now = get_now()
        db = self._request.registry.db
        server_id = self.request.registry.server_id

        auction.id = auction_id
        auction.auctionID = generate_auction_id(get_now(), db, server_id)
        auction.modified = True
        auction.auctionParameters = {'type': AUCTION_PARAMETERS_TYPE}
        auction.date = now

        return auction


class AuctionDocumentCreator(BaseCreator):
    """
        Auction Document Creator
    """

    resource_interface = IAuctionDocument
    validators = [validate_auction_document_post]

    def _create(self, document):
        uploaded_document = upload_file(self.request, document)
        self.context.documents.append(uploaded_document)
        self.context.modified = True
        return document


class BidDocumentCreator(BaseCreator):
    """
        Bid Document Creator
    """

    resource_interface = IBidDocument
    validators = [validate_bid_document_post]

    def _create(self, document):
        uploaded_document = upload_file(self.request, document)
        self.context.documents.append(uploaded_document)
        self.context.modified = True
        return document


class CancellationDocumentCreator(BaseCreator):
    """
        Cancellation Document Creator
    """

    resource_interface = ICancellationDocument

    def _create(self, document):
        uploaded_document = upload_file(self.request, document)
        self.context.documents.append(uploaded_document)
        self.context.modified = True
        return document


class ItemCreator(BaseCreator):
    """
        Item Creator
    """

    resource_interface = IItem

    def _create(self, item):
        self.context.items.append(item)
        self.context.modified = True
        return item


class QuestionCreator(BaseCreator):
    """
        Question Creator
    """

    resource_interface = IQuestion
    validators = [validate_question_post]

    def create(self, question):
        self.context.questions.append(question)
        self.context.modified = True
        return question


class CancellationCreator(BaseCreator):
    """
        Cancellation Creator
    """

    resource_interface = ICancellation

    def create(self, cancellation):
        self.context.cancellations.append(cancellation)
        self.context.modified = True
        return cancellation
