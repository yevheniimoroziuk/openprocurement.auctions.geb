from zope.interface import implementer

from openprocurement.auctions.core.interfaces import (
    IAuctionChanger,
    IBidChanger,
    IBidDocumentChanger,
    ICancellationChanger,
    IDocumentChanger,
    IItemChanger,
    INamedValidators,
    IQuestionChanger
)

from openprocurement.auctions.core.utils import (
    apply_patch,
    upload_file
)

from openprocurement.auctions.geb.managers.utils import (
    NamedValidators
)

from openprocurement.auctions.geb.validation import (
    validate_question_changing_period,
    validate_item_changing_period,
    # patch auction validators
    validate_auction_patch_phase_commit,
    validate_auction_patch_period,
    # patch auction document validators
    validate_period_auction_document_patch,
    # put auction document validators
    validate_period_auction_document_put,
    # patch bids validators
    validate_bid_patch_draft,
    validate_bid_patch_pending,
    validate_bid_patch_active,
    validate_bid_patch_auction_period,
    validate_auction_patch_rectification
)

from openprocurement.auctions.geb.managers.initializators import (
    CancellationChangerInitializator
)


@implementer(IAuctionChanger)
class AuctionChanger(object):
    name = 'Auction Changer'
    validators = [
        validate_auction_patch_phase_commit,
        validate_auction_patch_period,
        validate_auction_patch_rectification
    ]

    def __init__(self, request, context):
        self._request = request
        self._context = context

    def validate(self):
        for validator in self.validators:
            if not validator(self._request, auction=self._context):
                return
        return True

    def change(self):
        if self.validate():
            self._context.changed = apply_patch(self._request, save=False, src=self._request.validated['auction_src'])
            return self._context.changed


@implementer(IBidChanger)
class BidChanger(object):
    name = 'Bid Changer'
    validators_named = [
        NamedValidators(name='draft', validators=(
            validate_bid_patch_draft,
        )),
        NamedValidators(name='pending', validators=(
            validate_bid_patch_pending,
        )),
        NamedValidators(name='active', validators=(
            validate_bid_patch_active,
        )),
    ]
    validators_collective = (
        validate_bid_patch_auction_period,
    )

    def __init__(self, request, context):
        self._request = request
        self._context = context
        self._auction = context.__parent__

    def _validate_named(self, name):
        for validator in self.validators_named:
            if INamedValidators.providedBy(validator) and validator.name == name:
                break
        for named_validator in validator.validators:
            if not named_validator(self._request, auction=self._auction, bid=self._context):
                return False
        return True

    def _validate_collective(self):
        for validator in self.validators_collective:
            if not validator(self._request, auction=self._auction, bid=self._context):
                return False
        return True

    def _validate(self, status):
        if not self._validate_collective() or not self._validate_named(status):
            return False
        return True

    def change(self):
        if self._validate(self._context.status):
            self._auction.changed = apply_patch(self._request, save=False, src=self._context.serialize())
            return self._auction.changed


@implementer(IDocumentChanger)
class DocumentChanger(object):
    name = 'Document Changer'
    patch_validators = [validate_period_auction_document_patch]
    put_validators = [validate_period_auction_document_put]

    def __init__(self, request, context):
        self._request = request
        self._context = context
        self._auction = context.__parent__

    def validate(self, validators):
        for validator in validators:
            if not validator(self._request, auction=self._auction, document=self._context):
                return False
        return True

    def change(self):
        if self.validate(self.patch_validators):
            self._auction.changed = apply_patch(self._request, save=False, src=self._context.serialize())
            return self._auction.changed

    def put(self):
        if self.validate(self.put_validators):
            document = upload_file(self._request)
            self._auction.documents.append(document)
            self._auction.changed = True
            return document


@implementer(IBidDocumentChanger)
class BidDocumentChanger(object):
    name = 'Bid Document Changer'

    def __init__(self, request, context):
        self._request = request
        self._context = context
        self._auction = context.__parent__

    def validate(self):
        return True

    def change(self):
        if self.validate():
            self._auction.changed = apply_patch(self._request, save=False, src=self._context.serialize())
            return self._auction.changed


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
            if not validator(self._request, auction=self._auction, question=self._context):
                return False
        return True

    def change(self):
        if self.validate():
            self._auction.changed = apply_patch(self._request, save=False, src=self._context.serialize())
            return self._auction.changed


@implementer(IItemChanger)
class ItemChanger(object):
    name = 'Item Changer'
    validators = [validate_item_changing_period]

    def __init__(self, request, context):
        self._request = request
        self._context = context
        self._auction = context.__parent__

    def validate(self):
        for validator in self.validators:
            if not validator(self._request, auction=self._auction, item=self._context):
                return False
        return True

    def change(self):
        if self.validate():
            self._auction.changed = apply_patch(self._request, save=False, src=self._context.serialize())
            return self._auction.changed


@implementer(ICancellationChanger)
class CancellationChanger(object):
    name = 'Cancellation Changer'
    initializator = CancellationChangerInitializator

    def __init__(self, request, context):
        self._request = request
        self._context = context
        self._auction = context.__parent__
        self._initializator = self.initializator(self._request, self._auction, self._context)

    def validate(self):
        return True

    def _change(self):
        changed = apply_patch(self._request, save=False, src=self._context.serialize())
        return changed

    def _initialize(self):
        self._initializator.initialize()

    def change(self):
        if self.validate():
            self._auction.changed = self._change()
            if self._auction.changed:
                self._initialize()
            return self._auction.changed
