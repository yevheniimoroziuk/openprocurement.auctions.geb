from zope.interface import implementer

from openprocurement.auctions.core.interfaces import (
    IAuctionItemer
)


@implementer(IAuctionItemer)
class AuctionItemer(object):
    name = 'Auction Itemer'
    validators = []

    def __init__(self, request, context):
        self._request = request
        self._context = context

    def validate(self):
        for validator in self.validators:
            if not validator(self._request):
                return
        return True

    def add_item(self):
        if self.validate():
            item = self._request.validated['item']
            self._context.items.append(item)
            self._context.modified = True
            return item
