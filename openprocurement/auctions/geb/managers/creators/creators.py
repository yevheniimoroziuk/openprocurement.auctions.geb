from uuid import uuid4
from zope.interface import implementer

from openprocurement.auctions.core.utils import (
    generate_auction_id,
    get_now,
)
from openprocurement.auctions.geb.utils import (
    upload_file
)
from openprocurement.auctions.geb.managers.actions.auctions import (
    AuctionCreateActionsFactory
)
from openprocurement.auctions.geb.managers.actions.items import (
    ItemCreateActionsFactory
)
from openprocurement.auctions.geb.managers.actions.questions import (
    QuestionCreateActionsFactory
)
from openprocurement.auctions.geb.managers.actions.cancellations import (
    CancellationCreateActionsFactory
)
from openprocurement.auctions.geb.managers.actions.documents import (
    AuctionDocumentCreateActionsFactory,
    BidDocumentCreateActionsFactory,
    CancellationDocumentCreateActionsFactory
)
from openprocurement.auctions.geb.interfaces import (
    IAuction,
    IAuctionDocument,
    IBasicCreator,
    IDerivativeCreator,
    IDerivativeResourceCreator,
    IBidDocument,
    ICancellation,
    ICancellationDocument,
    IItem,
    IQuestion,
    IBasicResourceCreator,
)

# creator factory


class CreatorsFactory(object):
    """
        Creators Factory
    """
    def __init__(self, creators):
        self.creators = creators

    def __call__(self, applicant):
        for creator in self.creators:
            if creator.resource_interface.providedBy(applicant):
                return creator

# base creator


@implementer(IDerivativeCreator)
class DerivativeCreator(object):
    """
        Derivative Creator
        Creator for subresources of auction
    """
    creators = []
    factory = CreatorsFactory

    def __init__(self, request, auction, context):
        self._request = request
        self._context = context
        self._auction = auction

    def create(self, applicant):
        factory = self.factory(self.creators)
        creator_type = factory(applicant)
        creator = creator_type(self._request, self._auction, self._context)
        return creator.create(applicant)


@implementer(IBasicCreator)
class BasicCreator(object):
    """
        Base Creator
        Creator for resource auction
    """
    creators = []
    factory = CreatorsFactory

    def __init__(self, request, context):
        self._request = request
        self._context = context

    def create(self, applicant):
        factory = self.factory(self.creators)
        creator_type = factory(applicant)
        creator = creator_type(self._request, self._context)
        return creator.create(applicant)


# creators


@implementer(IBasicResourceCreator)
class BasicResourceCreator(object):
    resource_interface = None

    def __init__(self, request, context):
        self._request = request
        self._context = context

    def _validate(self, validators):
        for validator in validators:
            if not validator(self._request, context=self._context):
                return False
        return True

    def _create(self, applicant):
        pass

    def create(self, applicant):
        factory = self.action_factory()
        actions = factory.get_actions(self._request, self._context)
        if actions:
            if all([self._validate(action.validators) for action in actions]):
                created = self._create(applicant)
                if created:
                    [action(self._request, self._context).act() for action in actions]
                return created


@implementer(IDerivativeResourceCreator)
class DerivativeResourceCreator(object):
    resource_interface = None

    def __init__(self, request, auction, context):
        self._request = request
        self._context = context
        self._auction = auction

    def _validate(self, validators):
        for validator in validators:
            if not validator(self._request, context=self._context):
                return False
        return True

    def _create(self, applicant):
        pass

    def create(self, applicant):
        factory = self.action_factory()
        actions = factory.get_actions(self._request, self._context)
        if actions:
            if all([self._validate(action.validators) for action in actions]):
                created = self._create(applicant)
                if created:
                    [action(self._request, self._auction, self._context).act() for action in actions]
                return created


class AuctionResourceCreator(BasicResourceCreator):
    """
       Auction Creator
    """
    resource_interface = IAuction
    action_factory = AuctionCreateActionsFactory

    def _create(self, auction):
        auction_id = uuid4().hex
        db = self._request.registry.db
        server_id = self._request.registry.server_id

        auction.id = auction_id
        auction.auctionID = generate_auction_id(get_now(), db, server_id)
        auction.modified = True
        return auction


class AuctionDocumentResourceCreator(DerivativeResourceCreator):
    """
        Auction Document Creator
    """

    resource_interface = IAuctionDocument
    action_factory = AuctionDocumentCreateActionsFactory

    def _create(self, document):
        uploaded_document = upload_file(self._request, document)
        self._context.documents.append(uploaded_document)
        self._context.modified = True
        return document


class BidDocumentCreator(DerivativeResourceCreator):
    """
        Bid Document Creator
    """

    resource_interface = IBidDocument
    action_factory = BidDocumentCreateActionsFactory

    def _create(self, document):
        uploaded_document = upload_file(self._request, document)
        self._context.documents.append(uploaded_document)
        self._context.modified = True
        return document


class CancellationDocumentResourceCreator(DerivativeResourceCreator):
    """
        Cancellation Document Creator
    """

    resource_interface = ICancellationDocument
    action_factory = CancellationDocumentCreateActionsFactory

    def _create(self, document):
        uploaded_document = upload_file(self._request, document)
        self._context.documents.append(uploaded_document)
        self._context.modified = True
        return document


class ItemResourceCreator(DerivativeResourceCreator):
    """
        Item Creator
    """

    resource_interface = IItem
    action_factory = ItemCreateActionsFactory

    def _create(self, item):
        self._auction.items.append(item)
        self._auction.modified = True
        return item


class QuestionResourceCreator(DerivativeResourceCreator):
    """
        Question Creator
    """

    resource_interface = IQuestion
    action_factory = QuestionCreateActionsFactory

    def create(self, question):
        self._auction.questions.append(question)
        self._auction.modified = True
        return question


class CancellationResourceCreator(DerivativeResourceCreator):
    """
        Cancellation Creator
    """

    resource_interface = ICancellation
    action_factory = CancellationCreateActionsFactory

    def create(self, cancellation):
        self._auction.cancellations.append(cancellation)
        self._auction.modified = True
        return cancellation


# creators

class AuctionCreator(BasicCreator):
    """Auction Creator"""

    creators = (
        AuctionResourceCreator,
        AuctionDocumentResourceCreator,
        CancellationResourceCreator,
        ItemResourceCreator,
        QuestionResourceCreator
    )


class CancellationCreator(DerivativeResourceCreator):

    creators = (CancellationDocumentResourceCreator, )
