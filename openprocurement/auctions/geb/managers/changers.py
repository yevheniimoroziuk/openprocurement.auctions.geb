from zope.interface import implementer

from openprocurement.auctions.core.utils import (
    apply_patch,
    upload_file,
    get_now
)
from openprocurement.auctions.geb.interfaces import (
    IResourceChanger,
    ISubResourceChanger
)
<<<<<<< HEAD

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
=======
from openprocurement.auctions.geb.managers.actions.bids import (
    BidChangeActionFactory
>>>>>>> refactoring
)

from openprocurement.auctions.geb.managers.actions.items import (
    ItemChangeActionFactory
)

from openprocurement.auctions.geb.managers.actions.auctions import (
    AuctionActionsFactory,
    ModuleAuctionChangeActionsFactory
)
from openprocurement.auctions.geb.managers.actions.questions import (
    QuestionPatchActionsFactory
)
from openprocurement.auctions.geb.managers.actions.documents import (
    AuctionDocumentPatchActionsFactory,
    AuctionDocumentPutActionsFactory,
    BidDocumentPatchActionsFactory
)
from openprocurement.auctions.geb.managers.actions.chronograph import (
    ChronographActionsFactory
)
from openprocurement.auctions.geb.managers.actions.cancellations import (
    CancellationChangeActionFactory
)

<<<<<<< HEAD
@implementer(IAuctionChanger)
class AuctionChanger(object):
    name = 'Auction Changer'
    validators = [
        validate_auction_patch_phase_commit,
        validate_auction_patch_period,
        validate_auction_patch_rectification
    ]
=======
# base changers
>>>>>>> refactoring


@implementer(IResourceChanger)
class ResourceChanger(object):
    """
        Base Changer for resource such as 'auction'
    """

<<<<<<< HEAD
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
=======
    action_factory = AuctionActionsFactory
>>>>>>> refactoring

    def __init__(self, request, context):
        self._request = request
        self._context = context

    def _validate(self, validators):
        for validator in validators:
            if not validator(self._request, context=self._context):
                return False
        return True

    def _change(self):
        modified = apply_patch(self._request, save=False, src=self._context.serialize())
        if modified:
            self._context.modified = modified
        return modified

    def change(self):
<<<<<<< HEAD
        if self._validate(self._context.status):
            self._auction.changed = apply_patch(self._request, save=False, src=self._context.serialize())
            return self._auction.changed


@implementer(IDocumentChanger)
class DocumentChanger(object):
    name = 'Document Changer'
    patch_validators = [validate_period_auction_document_patch]
    put_validators = [validate_period_auction_document_put]

    def __init__(self, request, context):
=======
        factory = self.action_factory()
        actions = factory.get_actions(self._request, self._context)
        if actions:
            if all([self._validate(action.validators) for action in actions]):
                change = self._change()
                if change:
                    [action(self._request, self._context).act() for action in actions]
                return change


@implementer(ISubResourceChanger)
class SubResourceChanger(object):
    """
        Base Changer for subresource
    """
    action_factory = None

    def __init__(self, request, auction, context):
>>>>>>> refactoring
        self._request = request
        self._context = context
        self._auction = auction

    def _validate(self, validators):
        for validator in validators:
            if not validator(self._request, context=self._context, auction=self._auction):
                return False
        return True

    def _change(self):
        modified = apply_patch(self._request, save=False, src=self._context.serialize())
        if modified:
            self._auction.modified = modified
        return modified

    def change(self):
<<<<<<< HEAD
        if self.validate(self.patch_validators):
            self._auction.changed = apply_patch(self._request, save=False, src=self._context.serialize())
            return self._auction.changed

    def put(self):
        if self.validate(self.put_validators):
            document = upload_file(self._request)
            self._auction.documents.append(document)
            self._auction.changed = True
            return document
=======
        factory = self.action_factory()
        actions = factory.get_actions(self._request, self._context)

        if actions:
            if all([self._validate(action.validators) for action in actions]):
                change = self._change()
                if change:
                    [action(self._request, self._auction, self._context).act() for action in actions]
                return change
>>>>>>> refactoring

# auction changers


class AuctionChanger(ResourceChanger):
    """
        Auction changer
        trigger when patch auction
    """
    action_factory = AuctionActionsFactory


<<<<<<< HEAD
    def change(self):
        if self.validate():
            self._auction.changed = apply_patch(self._request, save=False, src=self._context.serialize())
            return self._auction.changed
=======
class ModuleAuctionChanger(ResourceChanger):
    """
        Module auction changer
        trigger when module auction change auction
    """
    action_factory = ModuleAuctionChangeActionsFactory
>>>>>>> refactoring

    def _change(self):
        """
            When results come, it is end of auctionPerion
        """
        self._context.auctionPeriod['endDate'] = get_now()

        modified = apply_patch(self._request, save=False, src=self._context.serialize())
        if modified:
            self._context.modified = modified
        return modified


class ChronographChanger(ResourceChanger):
    """
        Chronograph changer
        trigger when chronograph change auction
    """
    action_factory = ChronographActionsFactory

<<<<<<< HEAD
    def change(self):
        if self.validate():
            self._auction.changed = apply_patch(self._request, save=False, src=self._context.serialize())
            return self._auction.changed
=======
# subresource changers
>>>>>>> refactoring


class BidPatchChanger(SubResourceChanger):
    """
        Bid patch changer
        trigger when patch bid
    """
    action_factory = BidChangeActionFactory


class CancellationPatchChanger(SubResourceChanger):
    """
        Cancellation patch changer
        trigger when patch cancellation
    """
    action_factory = CancellationChangeActionFactory

<<<<<<< HEAD
    def change(self):
        if self.validate():
            self._auction.changed = apply_patch(self._request, save=False, src=self._context.serialize())
            return self._auction.changed
=======
>>>>>>> refactoring

class AuctionDocumentPatchChanger(SubResourceChanger):
    """
        Auction Document patch changer
        trigger when patch auction document
    """
    action_factory = AuctionDocumentPatchActionsFactory


class AuctionDocumentPutChanger(SubResourceChanger):
    """
        Auction Document put changer
        trigger when put auction document
    """

    action_factory = AuctionDocumentPutActionsFactory

    def _change(self):
<<<<<<< HEAD
        changed = apply_patch(self._request, save=False, src=self._context.serialize())
        return changed
=======
        document = upload_file(self._request)
        self._auction.documents.append(document)
        self._auction.modified = True
        return document
>>>>>>> refactoring


<<<<<<< HEAD
    def change(self):
        if self.validate():
            self._auction.changed = self._change()
            if self._auction.changed:
                self._initialize()
            return self._auction.changed
=======
class BidDocumentPatchChanger(SubResourceChanger):
    """
        Bid Document patch changer
        trigger when patch bid document
    """

    action_factory = BidDocumentPatchActionsFactory


class QuestionPatchChanger(SubResourceChanger):
    """
        Question patch changer
        trigger when patch  question
    """

    action_factory = QuestionPatchActionsFactory


class ItemPatchChanger(SubResourceChanger):
    """
        Item patch changer
        trigger when patch item
    """

    action_factory = ItemChangeActionFactory
>>>>>>> refactoring
