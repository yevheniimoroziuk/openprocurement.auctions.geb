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
        # check if it is a bid patch

        if request.method == 'PATCH':
            return cls
        return False

    def act(self):
        pass


class ItemChangeActionFactory(ActionFactory):
    actions = (
        ItemPatchAction,
    )
