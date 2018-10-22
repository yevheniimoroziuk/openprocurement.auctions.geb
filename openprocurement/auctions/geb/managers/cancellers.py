from zope.interface import implementer

from openprocurement.auctions.core.interfaces import (
    IAuctionCanceller
)


@implementer(IAuctionCanceller)
class AuctionCanceller(object):
    name = 'Auction Canceller'
    validators = []
    allow_pre_terminal_statuses = False

    def __init__(self, request, context):
        self._request = request
        self._context = context

    def validate(self):
        for validator in self.validators:
            if not validator(self._request):
                return
        return True

    def _add_cancellation(self):
        cancellation = self._request.validated['cancellation']
        self._context.cancellations.append(cancellation)
        return cancellation

    def cancel(self):
        if self.validate():
            cancellation = self._add_cancellation()
            self._context.modified = True
            return cancellation
