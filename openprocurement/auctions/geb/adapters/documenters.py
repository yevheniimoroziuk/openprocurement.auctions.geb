from zope.interface import implementer

from openprocurement.auctions.geb.interfaces import (
    IAuctionDocumenter
)

from openprocurement.auctions.geb.validation import (
    validate_document_editing_period
)

from openprocurement.auctions.geb.utils import (
    upload_file
)


@implementer(IAuctionDocumenter)
class AuctionDocumenter(object):
    name = 'Auction Changer'
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
