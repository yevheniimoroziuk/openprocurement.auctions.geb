from uuid import uuid4

from openprocurement.auctions.core.utils import (
    generate_auction_id,
    get_now,
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
    BaseAuctionCreator,
    BaseSubAuctionCreator
)
from openprocurement.auctions.geb.constants import (
    AUCTION_PARAMETERS_TYPE
)


class AuctionCreator(BaseAuctionCreator):
    """
       Auction Creator
    """
    resource_interface = IAuction
    validators = [validate_auction_post]

    def _create(self, auction):
        auction_id = uuid4().hex
        db = self._request.registry.db
        server_id = self._request.registry.server_id

        auction.id = auction_id
        auction.auctionID = generate_auction_id(get_now(), db, server_id)
        auction.modified = True

        now = get_now()

        # initialize auctionParameters
        auction.auctionParameters = {'type': AUCTION_PARAMETERS_TYPE}

        # initialize date
        auction.date = now
        return auction


class AuctionDocumentCreator(BaseAuctionCreator):
    """
        Auction Document Creator
    """

    resource_interface = IAuctionDocument
    validators = [validate_auction_document_post]

    def _create(self, document):
        uploaded_document = upload_file(self._request, document)
        self.context.documents.append(uploaded_document)
        self.context.modified = True
        return document


class BidDocumentCreator(BaseSubAuctionCreator):
    """
        Bid Document Creator
    """

    resource_interface = IBidDocument
    validators = [validate_bid_document_post]

    def _create(self, document):
        uploaded_document = upload_file(self._request, document)
        self.context.documents.append(uploaded_document)
        self.context.modified = True
        return document


class CancellationDocumentCreator(BaseSubAuctionCreator):
    """
        Cancellation Document Creator
    """

    resource_interface = ICancellationDocument

    def _create(self, document):
        uploaded_document = upload_file(self.request, document)
        self.context.documents.append(uploaded_document)
        self.context.modified = True
        return document


class ItemCreator(BaseAuctionCreator):
    """
        Item Creator
    """

    resource_interface = IItem

    def _create(self, item):
        self.auction.items.append(item)
        self.auction.modified = True
        return item


class QuestionCreator(BaseAuctionCreator):
    """
        Question Creator
    """

    resource_interface = IQuestion
    validators = [validate_question_post]

    def create(self, question):
        self.auction.questions.append(question)
        self.auction.modified = True
        return question


class CancellationCreator(BaseAuctionCreator):
    """
        Cancellation Creator
    """

    resource_interface = ICancellation

    def create(self, cancellation):
        self.auction.cancellations.append(cancellation)
        self.auction.modified = True
        return cancellation
