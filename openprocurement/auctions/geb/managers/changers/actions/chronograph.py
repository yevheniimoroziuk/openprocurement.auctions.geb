from pyramid.threadlocal import get_current_registry
from openprocurement.auctions.core.interfaces import (
    IContentConfigurator
)
from openprocurement.auctions.core.utils import (
    get_now,
    remove_bid
)

from openprocurement.auctions.geb.managers.changers.base import (
    BaseAction
)


class EndActiveRectificationAction(BaseAction):
    """
        Chronograph action
        trigger when chronograph come in end of 'active.rectification'
    """
    validators = []

    @classmethod
    def demand(cls, request, context):
        # check if chrongraph come in end of 'active.rectification'

        status = context.status
        rectification_period = context.rectificationPeriod
        now = get_now()

        if status == 'active.rectification' and now >= rectification_period.endDate:
            return cls
        return False

    def act(self):
        # switch procedure to 'active.tendering'

        self._context.status = 'active.tendering'
        self._context.modified = True


class EndActiveTenderingAction(BaseAction):
    """
        Chronograph action
        trigger when chronograph come in end of 'active.tendering'
    """
    validators = []

    @classmethod
    def demand(cls, request, context):
        # check if chrongraph come in end of 'active.tendering'

        status = context.status
        tender_period = context.tenderPeriod
        now = get_now()

        if status == 'active.tendering' and now >= tender_period.endDate:
            return cls
        return False

    def act(self):
        bids = self._context.bids
        active_bids = [bid for bid in bids if bid.status in ['pending', 'active']]

        # if no any bids in status 'active' or 'pending'
        # switch procedure to status 'unsuccessful'
        if not active_bids:
            self._context.status = 'unsuccessful'
            self._context.modified = True
            return True

        # if minNumberOfQualifiedBids is 2 and is only 1 bid
        # switch procedure to status 'unsuccessful'
        min_number = self._context.minNumberOfQualifiedBids

        if min_number == 2 and len(active_bids) == 1:
            self._context.status = 'unsuccessful'
            self._context.modified = True
            return True

        # after tendering period, all bids in status 'draft' are delete
        for bid in bids:
            if bid.status == 'draft':
                remove_bid(self._request, self._context, bid)

        # switch procedure to 'active.enquiry'
        self._context.status = 'active.enquiry'

        self._context.modified = True


class EndActiveEnquiryAction(BaseAction):
    """
        Chronograph action
        trigger when chronograph come in end of 'active.enquiry'
    """
    validators = []

    @classmethod
    def demand(cls, request, context):
        # check if chrongraph come in end of 'active.enquiry'

        status = context.status
        enquiry_period = context.enquiryPeriod
        now = get_now()

        if status == 'active.enquiry' and now >= enquiry_period.endDate:
            return cls
        return False

    def act(self):
        # check enquiry minNumberOfQualifiedBids

        min_number = self._context.minNumberOfQualifiedBids
        bids = self._context.bids
        active_bids = [bid for bid in bids if bid.status == 'active']

        if min_number == 1:
            if len(active_bids) == 0:
                self._context.status = 'unsuccessful'
            elif len(active_bids) == 1:
                self._context.status = 'active.qualification'
                # start awarding
                reg = get_current_registry()
                awarding = reg.queryMultiAdapter((self._context, self._request), IContentConfigurator)
                awarding.start_awarding()

            elif len(active_bids) >= 2:
                self._context.status = 'active.auction'
        elif min_number == 2:
            if len(active_bids) == 0:
                self._context.status = 'unsuccessful'
            elif len(active_bids) == 1:
                self._context.status = 'unsuccessful'
            elif len(active_bids) >= 2:
                self._context.status = 'active.auction'

        # in the end of enquiry period
        # all bids that are in status 'draft/pending'
        # switch to 'unsuccessful' status
        for bid in self._context['bids']:
            if bid.status in ['draft', 'pending']:
                bid.status = 'unsuccessful'

        self._context.modified = True


class SetAuctionPeriodStartDateAction(BaseAction):
    """
        Chronograph action
        trigger when chronograph come in end of 'active.enquiry'
    """
    validators = []

    @classmethod
    def demand(cls, request, context):
        """
            Check if request patch auctionPeriod.startDate
        """
        auction_period = request.validated['json_data'].get('auctionPeriod')
        if auction_period and auction_period.get('startDate'):
            return cls
        return False

    def act(self):
        pass


class ChronographPatchAction(BaseAction):
    """
        Chronograph patch actions
    """
    validators = []

    @classmethod
    def demand(cls, request, context):
        """
            Trigger when chronograph patch
        """
        if request.method == 'PATCH':
            return cls
        return False

    def act(self):
        pass
