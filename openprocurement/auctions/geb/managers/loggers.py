from zope.interface import implementer
from logging import getLogger

from openprocurement.auctions.core.interfaces import (
    IItemLogger,
    IBidLogger,
    IAuctionLogger,
    ICancellationLogger
)
from openprocurement.auctions.core.utils import (
    context_unpack
)


@implementer(IItemLogger)
class ItemLogger(object):
    name = 'Item Logger'

    def __init__(self, request, context):
        self._request = request
        self._context = context
        self.LOGGER = getLogger(type(self).__module__)

    def log_action(self, action, msg):
        extra = context_unpack(self._request, {'MESSAGE_ID': action})
        self.LOGGER.info(msg, extra=extra)


@implementer(IBidLogger)
class BidLogger(object):
    name = 'Bid Logger'

    def __init__(self, request, context):
        self._request = request
        self._context = context
        self.LOGGER = getLogger(type(self).__module__)

    def log_action(self, action, msg):
        extra = context_unpack(self._request, {'MESSAGE_ID': action})
        self.LOGGER.info(msg, extra=extra)


@implementer(ICancellationLogger)
class CancellationLogger(object):
    name = 'Cancellation Logger'

    def __init__(self, request, context):
        self._request = request
        self._context = context
        self.LOGGER = getLogger(type(self).__module__)

    def log_action(self, action, msg):
        extra = context_unpack(self._request, {'MESSAGE_ID': action})
        self.LOGGER.info(msg, extra=extra)


@implementer(IAuctionLogger)
class AuctionLogger(object):
    name = 'Auction Logger'

    def __init__(self, request, context):
        self._request = request
        self._context = context
        self.LOGGER = getLogger(type(self).__module__)

    def log_action(self, action, msg):
        extra = context_unpack(self._request, {'MESSAGE_ID': action})
        self.LOGGER.info(msg, extra=extra)
