# -*- coding: utf-8 -*-
from zope.interface import implementer
from datetime import timedelta

from openprocurement.auctions.core.adapters import (
    AuctionConfigurator as BaseAuctionConfigurator,
    AuctionManagerAdapter as BaseAuctionManagerAdapter
)
from openprocurement.auctions.landlease.models import (
    LandLease
)
from openprocurement.auctions.core.plugins.awarding.v2_1.adapters import (
    AwardingV2_1ConfiguratorMixin
)

from openprocurement.auctions.landlease.interfaces import (
    IAuctionInitializator
)

from openprocurement.auctions.core.utils import (
    calculate_business_date,
    get_now,
    TZ
)

from openprocurement.auctions.landlease.constants import (
    MINIMAL_PERIOD_FROM_RECTIFICATION_END,
    AUCTION_PARAMETERS_TYPE
)


class AuctionConfigurator(BaseAuctionConfigurator,
                          AwardingV2_1ConfiguratorMixin):
    name = 'Auction LandLease Configurator'
    model = LandLease


@implementer(IAuctionInitializator)
class AuctionInitializator(object):
    name = 'Auction Initializator'

    def __init__(self, context):
        self._now = get_now()
        self._context = context

    def _generate_rectificationPeriod(self):
        period = self._context.__class__.rectificationPeriod.model_class()

        period.startDate = self._now
        calculated_endDate = calculate_business_date(self._context.tenderPeriod.endDate,
                                                     -MINIMAL_PERIOD_FROM_RECTIFICATION_END,
                                                     self._context)

        period.endDate = calculated_endDate if calculated_endDate > self._now else self._now
        period.invalidationDate = None
        return period

    def _initialize_enquiryPeriod(self):
        self._context.enquiryPeriod = self._context.__class__.enquiryPeriod.model_class()
        self._context.enquiryPeriod.startDate = self._now

        start_date = TZ.localize(self._context.auctionPeriod.startDate.replace(tzinfo=None))
        item = (start_date.replace(hour=20, minute=0, second=0, microsecond=0) - timedelta(days=1))
        pause_between_periods = start_date - item
        end_date = calculate_business_date(start_date, -pause_between_periods, self)

        self._context.enquiryPeriod.endDate = end_date

    def _initialize_tenderPeriod(self):
        self._context.tenderPeriod = self._context.__class__.tenderPeriod.model_class()
        self._context.tenderPeriod.startDate = self._now

        start_date = TZ.localize(self._context.auctionPeriod.startDate.replace(tzinfo=None))
        item = (start_date.replace(hour=20, minute=0, second=0, microsecond=0) - timedelta(days=1))
        pause_between_periods = start_date - item
        end_date = calculate_business_date(start_date, -pause_between_periods, self)

        self._context.tenderPeriod.endDate = end_date

    def _initialize_rectificationPeriod(self):
        self._context.rectificationPeriod = self._generate_rectificationPeriod()

    def _initialize_auctionParameters(self):
        self._context.auctionParameters = {'type': AUCTION_PARAMETERS_TYPE}

    def _initialize_date(self):
        self._context.date = self._now

    def _clean_auctionPeriod(self):
        self._context.auctionPeriod.startDate = None
        self._context.auctionPeriod.endDate = None

    def initialize(self):
        self._initialize_enquiryPeriod()
        self._initialize_tenderPeriod()
        self._initialize_rectificationPeriod()
        self._initialize_auctionParameters()
        self._initialize_date()
        self._clean_auctionPeriod()


class AuctionManagerAdapter(BaseAuctionManagerAdapter):

    def create_auction(self, request):
        pass

    def change_auction(self, request):
        pass

    def initialize(self, initializator):
        self._initializator = initializator
        self._initializator.initialize()
