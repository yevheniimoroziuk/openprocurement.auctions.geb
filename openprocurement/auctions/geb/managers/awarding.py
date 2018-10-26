# -*- coding: utf-8 -*-
from datetime import timedelta
from openprocurement.auctions.core.plugins.awarding.v3_1.adapters import (
    AwardingV3_1ConfiguratorMixin as BaseAwarding
)
from openprocurement.auctions.geb.models.schemas import (
    Auction
)
from openprocurement.auctions.core.utils import (
    calculate_business_date as cbd
)


class Awarding(BaseAwarding):
    model = Auction
    PENDING_ADMISSION_FOR_ONE_BID = False
    NUMBER_OF_BIDS_TO_BE_QUALIFIED = 1

    @property
    def verificationPeriod(self):
        auction_end_date = self.context.auctionPeriod.endDate
        end_date = cbd(auction_end_date, timedelta(days=0), self.context, specific_hour=18)
        verification_period = {
            'startDate': self._start_awarding,
            'endDate': end_date
        }
        self.verification_period = verification_period
        return verification_period

    @property
    def signingPeriod(self):
        auction_end_date = self.context.auctionPeriod.endDate
        verification_end_date = self.verification_period['endDate']
        end_date = cbd(auction_end_date, timedelta(days=0), self.context, self.context, specific_hour=23) + timedelta(minutes=59)
        singing_period = {
            'startDate': verification_end_date,
            'endDate': end_date
        }

        return singing_period
