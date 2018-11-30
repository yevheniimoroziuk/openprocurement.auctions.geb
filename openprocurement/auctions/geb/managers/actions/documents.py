from zope.interface import implementer

from openprocurement.auctions.geb.managers.actions.main import (
    ActionFactory
)
from openprocurement.auctions.geb.interfaces import (
    IAuctionDocumentAction,
    IBidDocumentAction,
    ICancellationDocumentAction
)
from openprocurement.auctions.geb.validation import (
    validate_auction_document_patch,
    validate_auction_document_put,
    validate_document_adding_period,
    validate_auction_status_for_adding_bid_document,                        # TODO rename all
    validate_bid_status_for_adding_bid_document
)

# auction documents actions


@implementer(IAuctionDocumentAction)
class AuctionDocumentPatchAction(object):
    """
        This action triggered then patch auction document
    """
    validators = [validate_auction_document_patch]

    def __init__(self, request, auction, context):
        self._request = request
        self._context = context
        self._auction = auction

    @classmethod
    def demand(cls, request, context):
        if request.method == 'PATCH':
            return cls
        return False

    def act(self):
        pass


@implementer(IAuctionDocumentAction)
class AuctionDocumentPutAction(object):
    """
        This action triggered then put auction document
    """
    validators = [validate_auction_document_put]

    def __init__(self, request, auction, context):
        self._request = request
        self._context = context
        self._auction = auction

    @classmethod
    def demand(cls, request, context):
        if request.method == 'PUT':
            return cls
        return False

    def act(self):
        pass


@implementer(IAuctionDocumentAction)
class AuctionDocumentPostAction(object):
    """
        This action triggered then create(post) auction document
    """
    validators = [validate_document_adding_period]

    def __init__(self, request, auction, context):
        self._request = request
        self._context = context
        self._auction = auction

    @classmethod
    def demand(cls, request, context):
        if request.method == 'POST':
            return cls
        return False

    def act(self):
        pass

# bid documents actions


@implementer(IBidDocumentAction)
class BidDocumentPatchAction(object):
    """
        This action triggered then patch bid document
    """
    validators = []

    def __init__(self, request, auction, context):
        self._request = request
        self._context = context
        self._auction = auction

    @classmethod
    def demand(cls, request, context):
        if request.method == 'PATCH':
            return cls
        return False

    def act(self):
        pass


@implementer(IBidDocumentAction)
class BidDocumentPostAction(object):
    """
        This action triggered then create(post) bid document
    """
    validators = [
        validate_auction_status_for_adding_bid_document,
        validate_bid_status_for_adding_bid_document
    ]

    def __init__(self, request, auction, context):
        self._request = request
        self._context = context
        self._auction = auction

    @classmethod
    def demand(cls, request, context):
        if request.method == 'POST':
            return cls
        return False

    def act(self):
        pass

# cancellation document actions


@implementer(ICancellationDocumentAction)
class CancellationDocumentPostAction(object):
    """
        This action triggered then create(post) cancellation document
    """
    validators = []

    def __init__(self, request, auction, context):
        self._request = request
        self._context = context
        self._auction = auction

    @classmethod
    def demand(cls, request, context):
        if request.method == 'POST':
            return cls
        return False

    def act(self):
        pass

# auction document actions factories


class AuctionDocumentPatchActionsFactory(ActionFactory):
    actions = (
         AuctionDocumentPatchAction,
    )


class AuctionDocumentPutActionsFactory(ActionFactory):
    actions = (
         AuctionDocumentPutAction,
    )


class AuctionDocumentCreateActionsFactory(ActionFactory):
    actions = (
         AuctionDocumentPostAction,
    )


# bid document actions factories


class BidDocumentPatchActionsFactory(ActionFactory):
    actions = (
         BidDocumentPatchAction,
    )


class BidDocumentCreateActionsFactory(ActionFactory):
    actions = (
         BidDocumentPostAction,
    )


# Cancellation document actions factories

class CancellationDocumentCreateActionsFactory(ActionFactory):
    actions = (
         CancellationDocumentPostAction,
    )
