from openprocurement.auctions.geb.managers.changers.base import (
    BaseAction
)


class SetAuctionPeriodStartDateAction(BaseAction):
    """
        Action that will be triggered when chronograph or bridge
        come to patch auction period
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
