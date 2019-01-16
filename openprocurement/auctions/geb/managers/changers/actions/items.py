from openprocurement.auctions.geb.validation import (
    validate_item_patch_auction_period,
)

from openprocurement.auctions.geb.managers.changers.base import (
    BaseAction
)


class ItemPatchAction(BaseAction):
    """
        Action triggered then patch item
    """
    validators = [
        validate_item_patch_auction_period
    ]

    @classmethod
    def demand(cls, request, context):
        # check if it is a item patch

        if request.method == 'PATCH':
            return cls
        return False

    def act(self):
        pass
