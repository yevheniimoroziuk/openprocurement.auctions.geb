# -*- coding: utf-8 -*-
from datetime import timedelta
from openprocurement.auctions.core.plugins.awarding.v3_1.adapters import (
    AwardingV3_1ConfiguratorMixin as BaseAwarding
)
from openprocurement.auctions.core.adapters import (
    AuctionConfigurator
)
from openprocurement.auctions.core.utils import (
    set_specific_hour
)
from openprocurement.auctions.geb.models.schemas import (
    Auction
)
from openprocurement.auctions.core.utils import (
    calculate_business_date as cbd
)


class Awarding(AuctionConfigurator, BaseAwarding):
    model = Auction
    pending_admission_for_one_bid = False
    NUMBER_OF_BIDS_TO_BE_QUALIFIED = 1

    @property
    def verificationPeriod(self):
        # generate verificationPeriod.endDate
        start_awarding = self.context.awardPeriod.startDate
        auction_end_date = self.context.auctionPeriod.endDate

        if auction_end_date:
            end_date = cbd(start_awarding,
                           timedelta(days=0),
                           self.context,
                           specific_hour=18)
        else:
            # if auction minNumberOfQualifiedBids was 1
            # only 1 bid was in status 'active'
            # after 'active.enquiry' auction switch to 'active.qualification'
            # verificationPeriod start after end of enquiryPeriod
            enquiry_end_date = self.context.enquiryPeriod.endDate
            end_date = cbd(enquiry_end_date,
                           timedelta(days=1),
                           self.context,
                           specific_hour=18,
                           working_days=True)

        # generate verificationPeriod.startDate
        outstanding_auction_time = set_specific_hour(end_date, 18)

        # check if module auction outstanding time to brings result
        if start_awarding > outstanding_auction_time:
            start_date = set_specific_hour(end_date, 17)
        else:
            start_date = start_awarding
        verification_period = {
            'startDate': start_date,
            'endDate': end_date
        }
        self.verification_period = verification_period
        return verification_period

    @property
    def signingPeriod(self):
        verification_end_date = self.verification_period['endDate']
        end_date = cbd(verification_end_date, timedelta(days=0), self.context, specific_hour=23) + timedelta(minutes=59)
        outstanding_auction_time = set_specific_hour(end_date, 18)
        start_awarding = self.context.awardPeriod.startDate

        # check if module auction outstanding time to brings result
        if start_awarding > outstanding_auction_time:
            start_date = set_specific_hour(end_date, 17)
        else:
            start_date = start_awarding
        singing_period = {
            'startDate': start_date,
            'endDate': end_date
        }

        return singing_period

    def _reject_award(self):
        # organizer reject award, auction switch to status 'unsuccessful'

        self.context.status = 'unsuccessful'

    def back_to_awarding(self):
        self._reject_award()
