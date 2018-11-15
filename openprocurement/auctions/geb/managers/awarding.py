# -*- coding: utf-8 -*-
from datetime import timedelta
from openprocurement.auctions.core.plugins.awarding.v3_1.adapters import (
    AwardingV3_1ConfiguratorMixin as BaseAwarding
)
from openprocurement.auctions.core.adapters import (
    AuctionConfigurator
)
from openprocurement.auctions.core.utils import (
    set_specific_hour,
    get_now
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
        start_awarding = self.context.awardPeriod.startDate
        auction_end_date = self.context.auctionPeriod.endDate

        # set start_date
        start_date = start_awarding

        if auction_end_date:
            end_date = cbd(start_awarding, timedelta(days=0), self.context, specific_hour=18)

            # find the outstanding time for bringing result of module auction
            outstanding_auction_time = set_specific_hour(auction_end_date, 18)

            # check if module auction outstanding time to brings result
            if start_awarding > outstanding_auction_time:
                start_date = cbd(start_awarding,
                                 timedelta(days=0),
                                 self.context,
                                 specific_hour=17)
        else:
            # if auction minNumberOfQualifiedBids was 1
            # only 1 bid was in status 'active'
            # after 'active.enquiry' auction switch to 'active.qualification'
            # verificationPeriod start after end of enquiryPeriod
            now = get_now()
            end_date = cbd(now,
                           timedelta(days=1),
                           self.context,
                           specific_hour=18,
                           working_days=True)

        verification_period = {
            'startDate': start_date,
            'endDate': end_date
        }
        self.verification_period = verification_period
        return verification_period

    @property
    def signingPeriod(self):
        start_awarding = self.context.awardPeriod.startDate
        auction_end_date = self.context.auctionPeriod.endDate
        verification_end_date = self.verification_period['endDate']

        # set endDate
        end_date = cbd(verification_end_date, timedelta(days=0), self.context, specific_hour=23) + timedelta(minutes=59)

        # set startDate
        start_date = start_awarding

        if auction_end_date:

            # find the outstanding time for bringing result of module auction
            outstanding_auction_time = set_specific_hour(auction_end_date, 18)

            # check if module auction outstanding time to brings result
            if start_awarding > outstanding_auction_time:
                start_date = cbd(start_awarding,
                                 timedelta(days=0),
                                 self.context,
                                 specific_hour=17)

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
