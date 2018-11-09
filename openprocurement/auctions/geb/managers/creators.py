from uuid import uuid4
from zope.interface import implementer

from openprocurement.auctions.core.interfaces import (
    IAuctionCreator,
    IAuctionDocumentCreator,
    IAuctionItemCreator,
    IAuctionQuestionCreator,
    IAuctionCancellationCreator,
    IBidDocumentCreator,
    ICancellationDocumentCreator,
    ICreator
)
from openprocurement.auctions.geb.validation import (
    validate_auctionPeriod,
    validate_auction_status_for_adding_bid_document,
    validate_bid_status_for_adding_bid_document,
    validate_document_adding_period,
    validate_first_auction_status,
    validate_question_adding_period
)
from openprocurement.auctions.core.utils import (
    generate_auction_id,
    get_now
)
from openprocurement.auctions.geb.utils import (
    upload_file
)
from openprocurement.auctions.geb.interfaces import (
    IDocument,
    IBidDocument,
    ICancellationDocument,
    IAuction,
    IItem,
    IQuestion,
    ICancellation
)

# resource creators


@implementer(IAuctionDocumentCreator)
class AuctionDocumentCreator(object):
    resource_interface = IDocument
    name = 'Auction Document Creator'
    validators = [validate_document_adding_period]

    def __init__(self, request, context):
        self._request = request
        self._context = context

    def validate(self):
        for validator in self.validators:
            if not validator(self._request):
                return False
        return True

    def create(self, document):
        if self.validate():
            document = upload_file(self._request, document)
            self._context.documents.append(document)
            self._context.modified = True
            return document


@implementer(IBidDocumentCreator)
class BidDocumentCreator(object):
    name = 'Bid Document Creator'
    resource_interface = IBidDocument
    validators = [validate_auction_status_for_adding_bid_document,
                  validate_bid_status_for_adding_bid_document]

    def __init__(self, request, context):
        self._request = request
        self._context = context
        self._auction = context.__parent__

    def validate(self):
        for validator in self.validators:
            if not validator(self._request, auction=self._auction, bid=self._context):
                return False
        return True

    def create(self, document):
        if self.validate():
            document = upload_file(self._request, document)
            self._context.documents.append(document)
            self._auction.modified = True
            return document


@implementer(ICancellationDocumentCreator)
class CancellationDocumentCreator(object):
    name = 'Cancellation Document Creator'
    resource_interface = ICancellationDocument

    def __init__(self, request, context):
        self._request = request
        self._context = context
        self._auction = context.__parent__

    def validate(self):
        return True

    def create(self, document):
        if self.validate():
            document = upload_file(self._request, document)
            self._context.documents.append(document)
            self._auction.modified = True
            return document


@implementer(IAuctionCreator)
class AuctionCreator(object):
    name = 'Auction Creator'
    resource_interface = IAuction
    validators = [validate_first_auction_status, validate_auctionPeriod]

    def __init__(self, request, context):
        self._request = request
        self._context = context

    def validate(self):
        for validator in self.validators:
            if not validator(self._request):
                return
        return True

    def _generate_id(self):
        return uuid4().hex

    def create(self, auction):
        if self.validate():
            auction_id = self._generate_id()
            auction.id = auction_id
            db = self._request.registry.db
            server_id = self._request.registry.server_id
            auction.auctionID = generate_auction_id(get_now(), db, server_id)
            self._context.modified = True
            return self._context


@implementer(IAuctionItemCreator)
class AuctionItemCreator(object):
    name = 'Auction Item creator'
    resource_interface = IItem

    def __init__(self, request, context):
        self._request = request
        self._context = context

    def _validate(self):
        return True

    def create(self, item):
        if self._validate():
            self._context.items.append(item)
            self._context.modified = True
            return item


@implementer(IAuctionQuestionCreator)
class AuctionQuestionCreator(object):
    name = 'Auction Question Creator'
    resource_interface = IQuestion
    validators = [validate_question_adding_period]

    def __init__(self, request, context):
        self._request = request
        self._context = context

    def validate(self):
        for validator in self.validators:
            if not validator(self._request):
                return False
        return True

    def create(self, question):
        if self.validate():
            self._context.questions.append(question)
            self._context.modified = True
            return question


@implementer(IAuctionCancellationCreator)
class AuctionCancellationCreator(object):
    name = 'Auction Canceller'
    resource_interface = ICancellation
    allow_pre_terminal_statuses = False

    def __init__(self, request, context):
        self._request = request
        self._context = context

    def validate(self):
        return True

    def _add_cancellation(self):
        cancellation = self._request.validated['cancellation']
        self._context.cancellations.append(cancellation)
        return cancellation

    def create(self, cancellation):
        if self.validate():
            cancellation = self._add_cancellation()
            self._context.modified = True
            return cancellation

# creator factory


@implementer(IAuctionCreator)
class AuctionCreatorsFactory(object):
    creators = (
        AuctionCancellationCreator,
        AuctionCreator,
        AuctionDocumentCreator,
        AuctionItemCreator,
        AuctionQuestionCreator,
        BidDocumentCreator,
        CancellationDocumentCreator
    )

    def __call__(self, applicant):
        for creator in self.creators:
            if creator.resource_interface.providedBy(applicant):
                return creator

# main creator


@implementer(ICreator)
class Creator(object):
    name = 'Auction Creator'
    factory = AuctionCreatorsFactory

    def __init__(self, request, context):
        self._request = request
        self._context = context

    def create(self, applicant):
        factory = self.factory()
        creator_type = factory(applicant)
        creator = creator_type(self._request, self._context)
        return creator.create(applicant)
