# -*- coding: utf-8 -*-
from zope.interface import implementer
from datetime import timedelta

from openprocurement.auctions.core.interfaces import (
    IAuctionInitializator,
    IBidInitializator
)

from openprocurement.auctions.core.utils import (
    calculate_business_date,
    get_now
)

from openprocurement.auctions.geb.constants import (
    RECTIFICATION_PERIOD_DURATION,
    AUCTION_PARAMETERS_TYPE
)
from openprocurement.auctions.geb.validation import (
    validate_bid_initialization
)


@implementer(IAuctionInitializator)
class AuctionInitializator(object):
    name = 'Auction Initializator'
    validators = []

    def __init__(self, request, context):
        self._now = get_now()
        self._request = request
        self._context = context

    def validate(self):
        for validator in self.validators:
            if not validator(self._request):
                return
        return True

    def _initialize_enquiryPeriod(self):
        period = self._context.__class__.enquiryPeriod.model_class()

        start_date = self._now
        end_date = calculate_business_date(self._context.auctionPeriod.startDate,
                                           -timedelta(days=1),
                                           self._context,
                                           specific_hour=20,
                                           working_days=True)

        period.startDate = start_date
        period.endDate = end_date

        self._context.enquiryPeriod = period

    def _initialize_tenderPeriod(self):
        period = self._context.__class__.tenderPeriod.model_class()

        start_date = self._context.rectificationPeriod.endDate
        end_date = calculate_business_date(self._context.auctionPeriod.startDate,
                                           -timedelta(days=3),
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
                                           RECTIFICATION_PERIOD_DURATION,
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

    def _invalidate_bids(self):
        context = self._context

        value = context.value.amount
        unsuccessful_bids = [bid for bid in context.bids if bid.value.amount == value]
        for bid in unsuccessful_bids:
            bid.status = 'unsuccessful'

    def initialize(self, status):
        if status == 'active.rectification':
            self._initialize_rectificationPeriod()
            self._initialize_tenderPeriod()
            self._initialize_enquiryPeriod()
            self._initialize_auctionParameters()
            self._initialize_date()
            self._clean_auctionPeriod()
        elif status == 'active.auction':
            self._invalidate_bids()


@implementer(IBidInitializator)
class BidInitializator(object):
    validators = [validate_bid_initialization]

    def __init__(self, request, context):
        self._now = get_now()
        self._request = request
        self._context = context

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
        if self._context.modified and self.validate():
            self._initialize_qualified()
            self._initialize_date()
