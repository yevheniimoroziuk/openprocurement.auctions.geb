from uuid import uuid4
from zope.interface import implementer

from openprocurement.auctions.core.interfaces import (
    IAuctionCreator
)

from openprocurement.auctions.geb.validation import (
    validate_first_auction_status
)
from openprocurement.auctions.core.utils import (
    generate_auction_id,
    get_now
)


@implementer(IAuctionCreator)
class AuctionCreator(object):
    name = 'Auction Changer'
    validators = [validate_first_auction_status]

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

    def create(self):
        if self.validate():
            auction_id = self._generate_id()
            self._context.id = auction_id
            db = self._request.registry.db
            server_id = self._request.registry.server_id
            self._context.auctionID = generate_auction_id(get_now(), db, server_id)
            self._context.modified = True
            return self._context
