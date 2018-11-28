from zope.interface import implementer

from openprocurement.auctions.geb.managers.actions.main import (
    ActionFactory
)
from openprocurement.auctions.geb.interfaces import (
    IAuctionDocumentAction,
    IBidDocumentAction,
)
from openprocurement.auctions.geb.validation import (
    validate_auction_document_patch,
    validate_auction_document_put
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


# auction document actions factories


class AuctionDocumentPatchActionsFactory(ActionFactory):
    actions = (
         AuctionDocumentPatchAction,
    )


class AuctionDocumentPutActionsFactory(ActionFactory):
    actions = (
         AuctionDocumentPutAction,
    )

# bid document actions factories


class BidDocumentPatchActionsFactory(ActionFactory):
    actions = (
         BidDocumentPatchAction,
    )
