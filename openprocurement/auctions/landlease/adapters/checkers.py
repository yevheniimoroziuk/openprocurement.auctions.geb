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

    def _check_bids(self):
        import ipdb; ipdb.set_trace()  # XXX BREAKPOINT
        for bid in self._context.bids:
            if bid.status in ['pending', 'active']:
                return
        self._context.status = 'unsuccessful'
        raise StopChecks()

    def _check_status(self):
        status = self._context.status

        if status == 'active.rectification':
            new_status = 'active.tendering'

        self._context.status = new_status

    def _check_minNumberOfQualifiedBids(self):
        pass

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

    def check(self):
        date = self._get_check_date()
        try:
            if date == self._context.rectificationPeriod.endDate:
                self._check_status()
            elif date == self._context.tenderPeriod.endDate:
                self._check_bids()
                self._check_minNumberOfQualifiedBids()
        except StopChecks:
            pass
