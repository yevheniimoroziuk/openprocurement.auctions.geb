from zope.interface import implementer

from openprocurement.auctions.landlease.interfaces import (
    IAuctionChecker
)

from openprocurement.auctions.core.utils import (
    get_now
)


class StopChecks(Exception):
    pass


@implementer(IAuctionChecker)
class AuctionChecker(object):
    name = 'Auction Checker'

    def __init__(self, context):
        self._now = get_now()
        self._context = context
        self._next_status = None

    def _check_bids(self):
        for bid in self._context.bids:
            if bid.status in ['pending', 'active']:
                return
        self._next_status = 'unsuccessful'
        raise StopChecks()

    def _check_tendering_minNumberOfQualifiedBids(self):
        min_number = self._context.minNumberOfQualifiedBids
        bids = len([bid for bid in self._context.bids if bid.status in ('active', 'pending')])

        if min_number == 2 and bids == 1:
            self._next_status = 'unsuccessful'
            raise StopChecks()

    def _check_enquiry_minNumberOfQualifiedBids(self):
        min_number = self._context.minNumberOfQualifiedBids
        bids = len([bid for bid in self._context.bids if bid.status in ('active', 'pending')])
        if min_number == 1:
            if bids == 0:
                self._next_status = 'unsuccessful'
            elif bids == 1:
                self._next_status = 'active.qualification'
            elif bids >= 2:
                self._next_status = 'active.auction'
        elif min_number == 2:
            if bids == 0:
                self._next_status = 'unsuccessful'
            elif bids == 1:
                self._next_status = 'unsuccessful'
            elif bids >= 2:
                self._next_status = 'active.auction'

    def _get_check_date(self):
        status = self._context.status
        rectification_period = self._context.rectificationPeriod
        tender_period = self._context.tenderPeriod
        enquiry_period = self._context.enquiryPeriod

        if status == 'active.rectification' and self._now > rectification_period.endDate:
            return rectification_period.endDate
        elif status == 'active.tendering' and self._now > tender_period.endDate:
            return tender_period.endDate
        elif status == 'active.enquiry' and self._now > enquiry_period.endDate:
            return enquiry_period.endDate

    def _set_next_status(self):
        if self._next_status:
            self._context.status = self._next_status

    def _set_unseccessful_bids(self):
        for bid in self._context['bids']:
            if bid.status in ['draft', 'pending']:
                bid.status = 'unsuccessful'

    def check(self):
        date = self._get_check_date()
        try:
            if date == self._context.rectificationPeriod.endDate:
                self._next_status = 'active.tendering'
            elif date == self._context.tenderPeriod.endDate:
                self._check_bids()
                self._check_tendering_minNumberOfQualifiedBids()
                self._next_status = 'active.enquiry'
            elif date == self._context.enquiryPeriod.endDate:
                self._check_enquiry_minNumberOfQualifiedBids()
                self._set_unseccessful_bids()
        except StopChecks:
            pass
        self._set_next_status()
        return True
