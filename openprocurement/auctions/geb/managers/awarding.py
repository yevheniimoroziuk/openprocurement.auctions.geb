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
    pending_admission_for_one_bid = False
    NUMBER_OF_BIDS_TO_BE_QUALIFIED = 1

    @property
    def verificationPeriod(self):
        auction_end_date = self.context.auctionPeriod.endDate
        if auction_end_date:
            end_date = cbd(auction_end_date,
                           timedelta(days=0),
                           self.context,
                           specific_hour=18)
        else:
            enquiry_end_date = self.context.enquiryPeriod.endDate
            end_date = cbd(enquiry_end_date,
                           timedelta(days=1),
                           self.context,
                           specific_hour=18,
                           working_days=True)

        verification_period = {
            'startDate': self._start_awarding,
            'endDate': end_date
        }
        self.verification_period = verification_period
        return verification_period

    @property
    def signingPeriod(self):
        verification_end_date = self.verification_period['endDate']
        end_date = cbd(verification_end_date, timedelta(days=0), self.context, specific_hour=23) + timedelta(minutes=59)
        singing_period = {
            'startDate': self._start_awarding,
            'endDate': end_date
        }

        return singing_period
