from openprocurement.auctions.core.utils import (
    get_now
)

from openprocurement.auctions.geb.validation import (
    validate_bid_activation,
    validate_bid_patch_active,
    validate_bid_patch_draft,
    validate_bid_patch_auction_period,
    validate_bid_patch_pending,
    validate_bid_patch_pending_make_active_status,
)

from openprocurement.auctions.geb.managers.changers.base import (
    BaseAction
)


class BidActivationAction(BaseAction):
    """
    Bid Activation action
    when bid owner activate bid (patch status to 'active'):

    bid.qualified will set to False
    bid.date will set to now
    """
    validators = [
        validate_bid_activation
    ]

    @classmethod
    def demand(cls, request, context):
        # check if it is a bid activation action
        new_status = request.validated['json_data'].get('status')
        old_status = request.validated['resource_src']['status']
        if new_status == 'pending' and old_status == 'draft':
            return cls
        return False

    def act(self):
        now = get_now()

        # initialize qualified
        self.context.qualified = False

        # initialize_date
        self.context.date = now


class BidPendingPatchAction(BaseAction):
    """
        Bid patch in 'pending' status
    """
    validators = [
        validate_bid_patch_pending
    ]

    @classmethod
    def demand(cls, request, context):
        if context.status == 'pending':
            return cls
        return False

    def act(self):
        pass


class BidDraftPatchAction(BaseAction):
    """
        Bid patch in 'draft' status
    """
    validators = [
        validate_bid_patch_draft,
    ]

    @classmethod
    def demand(cls, request, context):
        if context.status == 'draft':
            return cls
        return False

    def act(self):
        pass


class BidActivePatchAction(BaseAction):
    """
        Bid patch in 'active' status
    """
    validators = [
        validate_bid_patch_active,
    ]

    @classmethod
    def demand(cls, request, context):
        if context.status == 'active':
            return cls
        return False

    def act(self):
        pass


class BidMakeActiveStatusAction(BaseAction):
    """
        Action triggered then bid owner patch bid status to 'active'
    """
    validators = [
        validate_bid_patch_pending_make_active_status,
    ]

    @classmethod
    def demand(cls, request, context):
        # check if it is a bid change status 'active'

        new_status = request.validated['json_data'].get('status')
        if new_status == 'active':
            return cls
        return False

    def act(self):
        now = get_now()

        # initialize qualified
        self.context.qualified = False

        # initialize_date
        self.context.date = now


class BidPatchAction(BaseAction):
    """
        Action triggered then patch bid
    """
    validators = [
        validate_bid_patch_auction_period
    ]

    @classmethod
    def demand(cls, request, context):
        # check if it is a bid patch

        if request.method == 'PATCH':
            return cls
        return False

    def act(self):
        pass
