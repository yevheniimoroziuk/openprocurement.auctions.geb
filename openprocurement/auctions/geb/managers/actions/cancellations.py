from zope.interface import implementer

from openprocurement.auctions.geb.managers.actions.main import (
    ActionFactory
)
from openprocurement.auctions.geb.interfaces import (
    ICancellationAction
)
from openprocurement.auctions.geb.constants import (
    AUCTION_STATUSES_FOR_CLEAN_BIDS_IN_CANCELLATION
)


@implementer(ICancellationAction)
class CancellationActivationAction(object):
    """
    Cancellation Activation action
    when auction owner activate cancellation (patch status to 'active'):

    -   auction.status will set to 'cancelled'
    -   if procedure in statuses ['active.tendering', 'active.enquiry', 'active.auction']
        delete all bids
    """
    validators = []

    def __init__(self, request, auction, context):
        self._request = request
        self._auction = auction
        self._context = context

    @classmethod
    def demand(cls, request, context):
        """
            Constructor method. If it is reason of action
            this method return instance of Action
        """
        # check if patch is for activating cancellation
        new_status = request.validated['json_data'].get('status')
        if context.status == 'pending' and new_status == 'active':
            return cls
        return False

    def act(self):
        # pendify auction status
        status = 'cancelled'
        self._auction.status = status

        # clean bids after cancellation procedure
        auction_status = self._request.validated['auction_src']['status']

        if auction_status in AUCTION_STATUSES_FOR_CLEAN_BIDS_IN_CANCELLATION:
            self._auction.bids = []


# factories


class CancellationChangeActionsFactory(ActionFactory):
    actions = (CancellationActivationAction,)
