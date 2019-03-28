from pyramid.threadlocal import get_current_registry
from datetime import timedelta

from openprocurement.auctions.core.utils import (
    calculate_business_date,
    get_now,
    log_auction_status_change
)
from openprocurement.auctions.core.interfaces import (
    IContentConfigurator
)
from openprocurement.auctions.geb.constants import (
    AUCTION_RECTIFICATION_PERIOD_DURATION,
)
from openprocurement.auctions.geb.validation import (
    validate_auction_patch_draft,
    validate_auction_patch_rectification,
    validate_auction_identity_of_bids,
    validate_auction_auction_status,
    validate_auction_number_of_bids,
    validate_auction_patch_period,
    validate_auction_patch_phase_commit,
    validate_auction_patch_phase_commit_auction_period
)

from openprocurement.auctions.geb.managers.changers.base import (
    BaseAction
)


class AuctionPhaseCommitAction(BaseAction):
    """
    Auction phase commit action
    when auction owner activate auction (patch status to 'active.rectification'):

    """
    validators = [
        validate_auction_patch_phase_commit,
        validate_auction_patch_phase_commit_auction_period
    ]

    @classmethod
    def demand(cls, request, context):
        # check if patch is for activating auction

        new_status = request.validated['json_data'].get('status')
        if context.status == 'draft' and new_status == 'active.rectification':
            return cls
        return False

    def _initialize_enquiryPeriod(self):
        period = self.context.__class__.enquiryPeriod.model_class()

        start_date = self.now
        end_date = calculate_business_date(self.context.auctionPeriod.startDate,
                                           -timedelta(days=1),
                                           self.context,
                                           specific_hour=20)

        period.startDate = start_date
        period.endDate = end_date

        self.context.enquiryPeriod = period

    def _initialize_tenderPeriod(self):
        period = self.context.__class__.tenderPeriod.model_class()

        start_date = self.context.rectificationPeriod.endDate
        end_date = calculate_business_date(self.context.auctionPeriod.startDate,
                                           -timedelta(days=4),
                                           self.context,
                                           specific_hour=20,
                                           working_days=True)

        period.startDate = start_date
        period.endDate = end_date

        self.context.tenderPeriod = period

    def _initialize_rectificationPeriod(self):
        period = self.context.__class__.rectificationPeriod.model_class()

        start_date = self.now
        end_date = calculate_business_date(self.now,
                                           AUCTION_RECTIFICATION_PERIOD_DURATION,
                                           self.context)

        period.startDate = start_date
        period.endDate = end_date

        self.context.rectificationPeriod = period

    def _clean_auctionPeriod(self):
        self.context.auctionPeriod.startDate = None
        self.context.auctionPeriod.endDate = None

    def act(self):
        self.now = get_now()
        self._initialize_rectificationPeriod()
        self._initialize_tenderPeriod()
        self._initialize_enquiryPeriod()
        self._clean_auctionPeriod()


class AuctionPatchDraftAction(BaseAction):
    """
    Auction patch auction in 'draft' status
    """
    validators = [validate_auction_patch_draft]

    @classmethod
    def demand(cls, request, context):
        # check if patch in auction 'draft' status

        if context.status == 'draft':
            return cls
        return False

    def act(self):
        pass


class AuctionPatchActiveRectificationAction(BaseAction):
    """
        Auction patch auction in 'active.rectification' status
    """
    validators = [validate_auction_patch_rectification]

    @classmethod
    def demand(cls, request, context):
        # check if patch in auction 'active.rectification' status

        if context.status == 'active.rectification':
            return cls
        return False

    def act(self):
        pass


class ModuleAuctionUpdateUrlsAction(BaseAction):
    """
        This action triggered then module auction
        update urls for auction
    """
    validators = [validate_auction_identity_of_bids]

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


class AuctionPatchAction(BaseAction):
    """
        This action triggered then was patch auction
    """
    validators = [validate_auction_patch_period]

    @classmethod
    def demand(cls, request, context):
        # this action is for common patch auction resource
        return cls

    def act(self):
        pass


class ModuleAuctionBringsResultAction(BaseAction):
    """
        This action triggered then moudule auction brings result of auction
    """
    validators = [
        validate_auction_auction_status,
        validate_auction_number_of_bids,
        validate_auction_identity_of_bids
    ]

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
        context = self.context

        context.auctionPeriod['endDate'] = get_now()
        auction_value = context.value.amount
        invalid_bids = [bid for bid in context.bids if bid.value.amount == auction_value]
        for bid in invalid_bids:
            bid.status = 'invalid'

        # check if there is a winner
        # if not, then switch procedure to 'unsuccessful' status
        if any([bid.status == 'active' for bid in self.context.bids]):
            # get awarding
            reg = get_current_registry()
            awarding = reg.queryMultiAdapter((self.context, self.request), IContentConfigurator)
            awarding.start_awarding()
        else:
            self.context.status = 'unsuccessful'
            log_auction_status_change(self.request, self.context, self.context.status)


class SetAuctionPeriodStartDateAction(BaseAction):
    """
        Chronograph action
        trigger when chronograph come in end of 'active.enquiry'
    """
    validators = []

    @classmethod
    def demand(cls, request, context):
        """
            Check if request patch auctionPeriod.startDate
        """
        auction_period = request.validated['json_data'].get('auctionPeriod')
        if auction_period and auction_period.get('startDate'):
            return cls
        return False

    def act(self):
        pass
