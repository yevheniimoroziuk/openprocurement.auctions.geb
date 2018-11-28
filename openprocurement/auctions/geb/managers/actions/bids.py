from zope.interface import implementer
from openprocurement.auctions.core.utils import (
    get_now
)

from openprocurement.auctions.geb.managers.actions.main import (
    ActionFactory
)
from openprocurement.auctions.geb.validation import (
    validate_bid_activation,
    validate_bid_patch_active,
    validate_bid_patch_draft,
    validate_bid_patch_auction_period,
    validate_bid_patch_pending,
    validate_bid_patch_pending_make_active_status,
)

from openprocurement.auctions.geb.interfaces import (
    IBidAction
)


@implementer(IBidAction)
class BidActivationAction(object):
    """
    Bid Activation action
    when bid owner activate bid (patch status to 'active'):

    bid.qualified will set to False
    bid.date will set to now
    """
    validators = [
        validate_bid_activation
    ]

    def __init__(self, request, auction, context):
        self._request = request
        self._context = context
        self._auction = auction

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
        self._context.qualified = False

        # initialize_date
        self._context.date = now


@implementer(IBidAction)
class BidPendingPatchAction(object):
    """
        Bid patch in 'pending' status
    """
    validators = [
        validate_bid_patch_pending
    ]

    def __init__(self, request, auction, context):
        self._request = request
        self._context = context
        self._auction = auction

    @classmethod
    def demand(cls, request, context):
        if context.status == 'pending':
            return cls
        return False

    def act(self):
        pass


@implementer(IBidAction)
class BidDraftPatchAction(object):
    """
        Bid patch in 'draft' status
    """
    validators = [
        validate_bid_patch_draft,
    ]

    def __init__(self, request, auction, context):
        self._request = request
        self._context = context
        self._auction = auction

    @classmethod
    def demand(cls, request, context):
        if context.status == 'draft':
            return cls
        return False

    def act(self):
        pass


@implementer(IBidAction)
class BidActivePatchAction(object):
    """
        Bid patch in 'active' status
    """
    validators = [
        validate_bid_patch_active,
    ]

    def __init__(self, request, auction, context):
        self._request = request
        self._auction = auction
        self._context = context

    @classmethod
    def demand(cls, request, context):
        if context.status == 'active':
            return cls
        return False

    def act(self):
        pass


@implementer(IBidAction)
class BidMakeActiveStatusAction(object):
    """
        Action triggered then bid owner patch bid status to 'active'
    """
    validators = [
        validate_bid_patch_pending_make_active_status,
    ]

    def __init__(self, request, auction, context):
        self._request = request
        self._context = context
        self._auction = auction

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
        self._context.qualified = False

        # initialize_date
        self._context.date = now


@implementer(IBidAction)
class BidPatchAction(object):
    """
        Action triggered then patch bid
    """
    validators = [
        validate_bid_patch_auction_period
    ]

    def __init__(self, request, auction, context):
        self._request = request
        self._auction = auction
        self._context = context

    @classmethod
    def demand(cls, request, context):
        # check if it is a bid patch

        if request.method == 'PATCH':
            return cls
        return False

    def act(self):
        pass


class BidChangeActionFactory(ActionFactory):
    actions = (
        BidActivationAction,
        BidActivePatchAction,
        BidDraftPatchAction,
        BidMakeActiveStatusAction,
        BidPatchAction,
        BidPendingPatchAction
    )
