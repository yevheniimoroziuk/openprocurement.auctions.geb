from zope.interface import implementer
from pyramid.threadlocal import get_current_registry
from datetime import timedelta

from openprocurement.auctions.core.utils import (
    calculate_business_date,
    get_now
)
from openprocurement.auctions.core.interfaces import (
    IContentConfigurator
)
from openprocurement.auctions.geb.managers.actions.main import (
    ActionFactory
)
from openprocurement.auctions.geb.interfaces import (
    IAuctionAction
)
from openprocurement.auctions.geb.constants import (
    AUCTION_PARAMETERS_TYPE,
    AUCTION_RECTIFICATION_PERIOD_DURATION,
)
from openprocurement.auctions.geb.validation import (
    validate_auction_patch_draft,
    validate_auction_patch_rectification,
    validate_auction_identity_of_bids,
    validate_auction_post_correct_auctionPeriod,
    validate_auction_auction_status,
    validate_auction_number_of_bids,
    validate_auction_patch_period,
    validate_auction_patch_phase_commit,
    validate_auction_patch_phase_commit_auction_period
)


@implementer(IAuctionAction)
class AuctionPhaseCommitAction(object):
    """
    Auction phase commit action
    when auction owner activate auction (patch status to 'active.rectification'):

    """
    validators = [
        validate_auction_patch_phase_commit,
        validate_auction_patch_phase_commit_auction_period
    ]

    def __init__(self, request, context):
        self._request = request
        self._context = context

    @classmethod
    def demand(cls, request, context):
        # check if patch is for activating auction

        new_status = request.validated['json_data'].get('status')
        if context.status == 'draft' and new_status == 'active.rectification':
            return cls
        return False

    def _initialize_enquiryPeriod(self):
        period = self._context.__class__.enquiryPeriod.model_class()

        start_date = self._now
        end_date = calculate_business_date(self._context.auctionPeriod.startDate,
                                           -timedelta(days=1),
                                           self._context,
                                           specific_hour=20)

        period.startDate = start_date
        period.endDate = end_date

        self._context.enquiryPeriod = period

    def _initialize_tenderPeriod(self):
        period = self._context.__class__.tenderPeriod.model_class()

        start_date = self._context.rectificationPeriod.endDate
        end_date = calculate_business_date(self._context.auctionPeriod.startDate,
                                           -timedelta(days=4),
                                           self._context,
                                           specific_hour=20,
                                           working_days=True)

        period.startDate = start_date
        period.endDate = end_date

        self._context.tenderPeriod = period

    def _initialize_rectificationPeriod(self):
        period = self._context.__class__.rectificationPeriod.model_class()

        start_date = self._now
        end_date = calculate_business_date(self._now,
                                           AUCTION_RECTIFICATION_PERIOD_DURATION,
                                           self._context)

        period.startDate = start_date
        period.endDate = end_date

        self._context.rectificationPeriod = period

    def _clean_auctionPeriod(self):
        self._context.auctionPeriod.startDate = None
        self._context.auctionPeriod.endDate = None

    def act(self):
        self._now = get_now()
        self._initialize_rectificationPeriod()
        self._initialize_tenderPeriod()
        self._initialize_enquiryPeriod()
        self._clean_auctionPeriod()


@implementer(IAuctionAction)
class AuctionPatchDraftAction(object):
    """
    Auction patch auction in 'draft' status
    """
    validators = [validate_auction_patch_draft]

    def __init__(self, request, context):
        self._request = request
        self._context = context

    @classmethod
    def demand(cls, request, context):
        # check if patch in auction 'draft' status

        if request.method == 'PATCH' and context.status == 'draft':
            return cls
        return False

    def act(self):
        pass


@implementer(IAuctionAction)
class AuctionPatchActiveRectificationAction(object):
    """
        Auction patch auction in 'active.rectification' status
    """
    validators = [validate_auction_patch_rectification]

    def __init__(self, request, context):
        self._request = request
        self._context = context

    @classmethod
    def demand(cls, request, context):
        # check if patch in auction 'active.rectification' status

        if request.method == 'PATCH' and context.status == 'active.rectification':
            return cls
        return False

    def act(self):
        pass


@implementer(IAuctionAction)
class ModuleAuctionUpdateUrlsAction(object):
    """
        This action triggered then module auction
        update urls for auction
    """
    validators = [validate_auction_identity_of_bids]

    def __init__(self, request, context):
        self._request = request
        self._context = context

    @classmethod
    def demand(cls, request, context):
        # check if it is update auction urls
        # in request data must be 'participationUrl'

        bids = request.validated['json_data'].get('bids')
        if not bids or not all([isinstance(bid, dict) for bid in bids]):
            return False

        bids = [bid.keys() for bid in bids]
        participation_urls = ['participationUrl' in bid for bid in bids]
        relevant_data = any(participation_urls)
        if relevant_data:
            return cls
        return False

    def act(self):
        pass


@implementer(IAuctionAction)
class AuctionPatchAction(object):
    """
        This action triggered then was patch auction
    """
    validators = [validate_auction_patch_period]

    def __init__(self, request, context):
        self._request = request
        self._context = context

    @classmethod
    def demand(cls, request, context):
        # this action is for common patch auction resource
        if request.method != 'PATCH':
            return False
        return cls

    def act(self):
        pass


@implementer(IAuctionAction)
class AuctionCreateAction(object):
    """
        This action triggered then was created auction resource
    """
    validators = [
        validate_auction_post_correct_auctionPeriod
    ]

    def __init__(self, request, context):
        self._request = request
        self._context = context

    @classmethod
    def demand(cls, request, context):
        if context.status != 'draft':
            return False

        if request.method != 'POST':
            return False
        return cls

    def act(self):
        now = get_now()

        # initialize auctionParameters
        self._context.auctionParameters = {'type': AUCTION_PARAMETERS_TYPE}

        # initialize date
        self._context.date = now


@implementer(IAuctionAction)
class ModuleAuctionBringsAction(object):
    """
        This action triggered then moudule auction brings result of auction
    """
    validators = [
        validate_auction_auction_status,
        validate_auction_number_of_bids,
        validate_auction_identity_of_bids
    ]

    def __init__(self, request, context):
        self._request = request
        self._context = context

    @classmethod
    def demand(cls, request, context):
        if request.method == 'POST':
            return cls
        return False

    def act(self):
        """
            After the auction results have come
            in bids wich didn`t do rate change status to 'invalid'
        """
        # invalidate bids after auction
        context = self._context
        auction_value = context.value.amount
        invalid_bids = [bid for bid in context.bids if bid.value.amount == auction_value]
        for bid in invalid_bids:
            bid.status = 'invalid'

        # check if there is a winner
        # if not, then switch procedure to 'unsuccessful' status
        if any([bid.status == 'active' for bid in self._context.bids]):
            # get awarding
            reg = get_current_registry()
            awarding = reg.queryMultiAdapter((self._context, self._request), IContentConfigurator)
            awarding.start_awarding()
        else:
            self._context.status = 'unsuccessful'


class AuctionActionsFactory(ActionFactory):
    actions = (
        AuctionPhaseCommitAction,
        AuctionPatchDraftAction,
        AuctionPatchActiveRectificationAction,
        AuctionPatchAction
    )


class AuctionCreateActionsFactory(ActionFactory):
    actions = (
        AuctionCreateAction,
    )


class ModuleAuctionChangeActionsFactory(ActionFactory):
    actions = (
        ModuleAuctionBringsAction,
        ModuleAuctionUpdateUrlsAction
    )
