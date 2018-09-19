from zope.interface import implementer

from openprocurement.auctions.core.interfaces import (
    IAuctionChanger,
    IBidChanger,
    IQuestionChanger
)

from openprocurement.auctions.core.utils import (
    apply_patch,
)

from openprocurement.auctions.geb.validation import (
    validate_change_bid_check_auction_status,
    validate_change_bid_check_status,
    validate_make_active_status_bid,
    validate_question_changing_period
)


@implementer(IBidChanger)
class BidChanger(object):
    name = 'Bid Changer'
    validators = [validate_change_bid_check_auction_status,
                  validate_change_bid_check_status,
                  validate_make_active_status_bid]

    def __init__(self, request, context):
        self._request = request
        self._context = context

    def validate(self):
        for validator in self.validators:
            if not validator(self._request):
                return
        return True

    def change(self):
        if self.validate():
            return apply_patch(self._request, save=False, src=self._context.serialize())
