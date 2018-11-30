from zope.interface import implementer

from openprocurement.auctions.geb.managers.actions.main import (
    ActionFactory
)
from openprocurement.auctions.geb.validation import (
    validate_item_patch_auction_period,
)

from openprocurement.auctions.geb.interfaces import (
    IItemAction
)


@implementer(IItemAction)
class ItemPatchAction(object):
    """
        Action triggered then patch item
    """
    validators = [
        validate_item_patch_auction_period
    ]

    def __init__(self, request, auction, context):
        self._request = request
        self._context = context
        self._auction = auction

    @classmethod
    def demand(cls, request, context):
        # check if it is a item patch

        if request.method == 'PATCH':
            return cls
        return False

    def act(self):
        pass


@implementer(IItemAction)
class ItemPostAction(object):
    """
        This action triggered then create(post) item
    """
    validators = []

    def __init__(self, request, auction, context):
        self._request = request
        self._context = context
        self._auction = auction

    @classmethod
    def demand(cls, request, context):
        if request.method == 'POST':
            return cls
        return False

    def act(self):
        pass

# factories


class ItemChangeActionsFactory(ActionFactory):
    actions = (
        ItemPatchAction,
    )


class ItemCreateActionsFactory(ActionFactory):
    actions = (
        ItemPostAction,
    )
