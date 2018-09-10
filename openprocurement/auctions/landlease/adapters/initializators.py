# -*- coding: utf-8 -*-
from zope.interface import implementer
from datetime import timedelta

from openprocurement.auctions.landlease.interfaces import (
    IAuctionInitializator,
    IBidInitializator
)

from openprocurement.auctions.core.utils import (
    calculate_business_date,
    get_now
)

from openprocurement.auctions.landlease.constants import (
    RECTIFICATION_PERIOD_DURATION,
    TENDER_PERIOD_DURATION,
    AUCTION_PARAMETERS_TYPE
)


@implementer(IAuctionInitializator)
class AuctionInitializator(object):
    name = 'Auction Initializator'

    def __init__(self, context):
        self._now = get_now()
        self._context = context

    def _initialize_enquiryPeriod(self):
        period = self._context.__class__.enquiryPeriod.model_class()

        start_date = self._now
        end_date = calculate_business_date(self._context.auctionPeriod.startDate,
                                           -timedelta(days=1),
                                           self._context)

        period.startDate = start_date
        period.endDate = end_date

        self._context.enquiryPeriod = period

    def _initialize_tenderPeriod(self):
        period = self._context.__class__.tenderPeriod.model_class()

        start_date = self._context.rectificationPeriod.endDate
        end_date = calculate_business_date(start_date,
                                           TENDER_PERIOD_DURATION,
                                           self._context)

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

    def initialize(self):
        self._initialize_rectificationPeriod()
        self._initialize_tenderPeriod()
        self._initialize_enquiryPeriod()
        self._initialize_auctionParameters()
        self._initialize_date()
        self._clean_auctionPeriod()


@implementer(IBidInitializator)
class BidInitializator(object):

    def __init__(self, request, context):
        self._now = get_now()
        self._request = request
        self._context = context

    def _initialize_qualified(self):
        self._context.qualified = False

    def _initialize_date(self):
        self._context.date = self._now

    def initialize(self):
        if self._request.validated['data'].get('status') == 'pending':
            self._initialize_qualified()
            self._initialize_date()
