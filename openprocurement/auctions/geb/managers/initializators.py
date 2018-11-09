# -*- coding: utf-8 -*-
from zope.interface import implementer
from datetime import timedelta

from openprocurement.auctions.core.interfaces import (
    IAuctionInitializator,
    IAuctionReportInitializator,
    ICancellationChangerInitializator,
    IBidInitializator
)

from openprocurement.auctions.core.utils import (
    calculate_business_date,
    get_now
)

from openprocurement.auctions.geb.constants import (
    AUCTION_PARAMETERS_TYPE,
    AUCTION_RECTIFICATION_PERIOD_DURATION
)
from openprocurement.auctions.geb.validation import (
    validate_bid_initialization,
)

from openprocurement.auctions.geb.constants import (
    AUCTION_STATUSES_FOR_CLEAN_BIDS_IN_CANCELLATION
)


@implementer(IAuctionInitializator)
class AuctionInitializator(object):
    name = 'Auction Initializator'
    validators = []

    def __init__(self, request, context):
        self._now = get_now()
        self._request = request
        self._context = context

    def _validate(self, status):
        for validator in self.validators:
            if validator.name == status:
                break
        else:
            return True
        for validator in validator.validators:
            if not validator(self._request):
                return False
        return True

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

    def _initialize_auctionParameters(self):
        self._context.auctionParameters = {'type': AUCTION_PARAMETERS_TYPE}

    def _initialize_date(self):
        self._context.date = self._now

    def _clean_auctionPeriod(self):
        self._context.auctionPeriod.startDate = None
        self._context.auctionPeriod.endDate = None

    def _check_demand(self):
        auction_src = self._request.validated['auction_src']

        if self._context.status == 'draft':                                     # create
            return True
        elif self._context.status == 'active.rectification':
            if auction_src['status'] == 'draft':                                # two-phase commit
                return True
        return False

    def _invalidate_bids_after_auction(self):
        context = self._context

        auction_value = context.value.amount
        invalid_bids = [bid for bid in context.bids if bid.value.amount == auction_value]
        for bid in invalid_bids:
            bid.status = 'invalid'

    def initialize(self, status):
        if self._check_demand():
            if self._validate(status):
                if status == 'draft':
                    self._initialize_auctionParameters()
                    self._initialize_date()
                elif status == 'active.rectification':
                    self._initialize_rectificationPeriod()
                    self._initialize_tenderPeriod()
                    self._initialize_enquiryPeriod()
                    self._clean_auctionPeriod()
            else:
                self._context.modified = False


@implementer(IBidInitializator)
class BidInitializator(object):
    validators = [validate_bid_initialization]

    def __init__(self, request, context):
        self._now = get_now()
        self._request = request
        self._context = context
        self._auction = context.__parent__

    def _initialize_qualified(self):
        self._context.qualified = False

    def _initialize_date(self):
        self._context.date = self._now

    def validate(self):
        for validator in self.validators:
            if not validator(self._request):
                return
        return True

    def initialize(self):
        if self._auction.modified and self.validate():
            self._initialize_qualified()
            self._initialize_date()


@implementer(ICancellationChangerInitializator)
class CancellationChangerInitializator(object):
    name = 'Cancellation Changer Initializator'

    def __init__(self, request, auction, context):
        self._request = request
        self._auction = auction
        self._context = context

    def _validate(self, status):
        for validator in self.validators:
            if validator.name == status:
                break
        else:
            return True
        for validator in validator.validators:
            if not validator(self._request):
                return False
        return True

    def _check_demand(self):
        resource_src = self._request.validated['resource_src']
        # activate cancellation
        if self._context.status == 'active' and resource_src['status'] == 'pending':
            return True
        return False

    def _pendify_auction_status(self, context, target_status):
        pending_prefix = 'pending'

        if (
            getattr(self._context, 'merchandisingObject', False)  # indicates registry integration
            and not self._context.merchandisingObject
            and self.allow_pre_terminal_statuses  # allows to manage using of preterm statuses
        ):
            status = '{0}.{1}'.format(pending_prefix, target_status)
        else:
            status = target_status

        context.status = status

    def _clean_procedure(self):
        auction_status = self._request.validated['auction_src']['status']

        if auction_status in AUCTION_STATUSES_FOR_CLEAN_BIDS_IN_CANCELLATION:
            self._auction.bids = []

    def initialize(self):
        if self._check_demand():
            self._pendify_auction_status(self._auction, 'cancelled')
            self._clean_procedure()


@implementer(IAuctionReportInitializator)
class AuctionReportInitializator(object):
    name = 'Auction Report Initializator'

    def __init__(self, request, context):
        self._request = request
        self._context = context

    def _invalidate_bids_after_auction(self):
        context = self._context
        auction_value = context.value.amount
        invalid_bids = [bid for bid in context.bids if bid.value.amount == auction_value]
        for bid in invalid_bids:
            bid.status = 'invalid'

    def initialize(self):
            self._invalidate_bids_after_auction()
