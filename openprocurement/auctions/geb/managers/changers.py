from zope.interface import implementer

from openprocurement.auctions.core.interfaces import (
    IAuctionChanger,
    IBidChanger,
    IQuestionChanger,
    IDocumentChanger
)

from openprocurement.auctions.core.utils import (
    apply_patch,
)

from openprocurement.auctions.geb.validation import (
    validate_change_bid_check_auction_status,
    validate_change_bid_check_status,
    validate_make_active_status_bid,
    validate_question_changing_period,
    validate_phase_commit,
    validate_edit_auction_document_period
)


@implementer(IAuctionChanger)
class AuctionChanger(object):
    name = 'Auction Changer'
    validators = [validate_phase_commit]

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
            self._context.modified = apply_patch(self._request, save=False, src=self._request.validated['auction_src'])
            return self._context.modified


@implementer(IBidChanger)
class BidChanger(object):
    name = 'Bid Changer'
    validators = [validate_change_bid_check_auction_status,
                  validate_change_bid_check_status,
                  validate_make_active_status_bid]

    def __init__(self, request, context):
        self._request = request
        self._context = context
        self._auction = context.__parent__

    def validate(self):
        for validator in self.validators:
            if not validator(self._request):
                return
        return True

    def change(self):
        if self.validate():
            self._auction.modified = apply_patch(self._request, save=False, src=self._context.serialize())
            return self._auction.modified


@implementer(IDocumentChanger)
class DocumentChanger(object):
    name = 'Document Changer'
    validators = [validate_edit_auction_document_period]

    def __init__(self, request, context):
        self._request = request
        self._context = context
        self._auction = context.__parent__

    def validate(self):
        for validator in self.validators:
            if not validator(self._request, self._auction, self._context):
                return
        return True

    def change(self):
        if self.validate():
            self._auction.modified = apply_patch(self._request, save=False, src=self._context.serialize())
            return self._auction.modified


@implementer(IQuestionChanger)
class QuestionChanger(object):
    name = 'Question Changer'
    validators = [validate_question_changing_period]

    def __init__(self, request, context):
        self._request = request
        self._context = context
        self._auction = context.__parent__

    def validate(self):
        for validator in self.validators:
            if not validator(self._request):
                return
        return True

    def change(self):
        if self.validate():
            self._auction.modified = apply_patch(self._request, save=False, src=self._context.serialize())
            return self._auction.modified
