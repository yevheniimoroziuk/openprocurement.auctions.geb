from zope.interface import implementer

from openprocurement.auctions.core.interfaces import (
    IAuctionDocumenter,
    IBidDocumenter
)

from openprocurement.auctions.geb.validation import (
    validate_document_editing_period,
    validate_bid_document
)

from openprocurement.auctions.geb.utils import (
    upload_file
)


@implementer(IAuctionDocumenter)
class AuctionDocumenter(object):
    name = 'Auction Documenter'
    validators = [validate_document_editing_period]

    def __init__(self, request, context):
        self._request = request
        self._context = context

    def validate(self):
        for validator in self.validators:
            if not validator(self._request):
                return
        return True

    def upload_document(self):
        if self.validate():
            document = upload_file(self._request)
            self._context.documents.append(document)
            return document


@implementer(IBidDocumenter)
class BidDocumenter(object):
    name = 'Bid Documenter'
    validators = [validate_bid_document]

    def __init__(self, request, context):
        self._request = request
        self._context = context

    def validate(self):
        for validator in self.validators:
            if not validator(self._request):
                return
        return True

    def upload_document(self):
        if self.validate():
            document = upload_file(self._request)
            self._context.documents.append(document)
            return document
