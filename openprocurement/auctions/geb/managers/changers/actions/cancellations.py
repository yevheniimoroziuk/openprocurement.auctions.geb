from openprocurement.auctions.geb.constants import (
    AUCTION_STATUSES_FOR_CLEAN_BIDS_IN_CANCELLATION
)
from openprocurement.auctions.geb.managers.changers.base import (
    BaseAction
)


class CancellationActivationAction(BaseAction):
    """
    Cancellation Activation action
    when auction owner activate cancellation (patch status to 'active'):

    -   auction.status will set to 'cancelled'
    -   if procedure in statuses ['active.tendering', 'active.enquiry', 'active.auction']
        delete all bids
    """
    validators = []

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
        auction = self.request

        # pendify auction status
        status = 'cancelled'
        auction.status = status

        # clean bids after cancellation procedure
        auction_status = self.request.validated['auction_src']['status']

        if auction_status in AUCTION_STATUSES_FOR_CLEAN_BIDS_IN_CANCELLATION:
            auction.bids = []
