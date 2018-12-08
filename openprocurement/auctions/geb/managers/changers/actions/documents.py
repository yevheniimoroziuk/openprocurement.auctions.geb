from openprocurement.auctions.geb.validation import (
    validate_auction_document_patch,
    validate_auction_document_put,
)
from openprocurement.auctions.geb.managers.changers.base import (
    BaseAction
)


class AuctionDocumentPatchAction(BaseAction):
    """
        This action triggered then patch auction document
    """
    validators = [validate_auction_document_patch]

    @classmethod
    def demand(cls, request, context):
        if request.method == 'PATCH':
            return cls
        return False

    def act(self):
        pass


class AuctionDocumentPutAction(BaseAction):
    """
        This action triggered then put auction document
    """
    validators = [validate_auction_document_put]

    @classmethod
    def demand(cls, request, context):
        if request.method == 'PUT':
            return cls
        return False

    def act(self):
        pass


class BidDocumentPatchAction(BaseAction):
    """
        This action triggered then patch bid document
    """
    validators = []

    @classmethod
    def demand(cls, request, context):
        if request.method == 'PATCH':
            return cls
        return False

    def act(self):
        pass
