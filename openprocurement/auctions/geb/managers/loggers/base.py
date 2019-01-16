from zope.interface import implementer
from logging import getLogger

from openprocurement.auctions.core.utils import (
    context_unpack
)
from openprocurement.auctions.geb.interfaces import (
    IResourceLogger
)


@implementer(IResourceLogger)
class BaseLogger(object):

    def __init__(self, request, context):
        self.request = request
        self.context = context
        self.LOGGER = getLogger(type(self).__module__)

    def log(self, action, msg):
        extra = context_unpack(self.request, {'MESSAGE_ID': action})
        self.LOGGER.info(msg, extra=extra)
