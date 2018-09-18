import os
import logging
from pyramid.interfaces import IRequest

from openprocurement.auctions.core.includeme import (
    get_evenly_plugins
)

from openprocurement.auctions.geb.managers.main import (
    AuctionManager,
    BidManager,
    QuestionManager
)
from openprocurement.auctions.geb.constants import (
    DEFAULT_LEVEL_OF_ACCREDITATION,
    DEFAULT_PROCUREMENT_METHOD_TYPE,
)
from openprocurement.auctions.geb.models.schemas import (
    Geb
)

from openprocurement.auctions.core.interfaces import (
    IAuctionManager,
    IQuestionManager,
    IBidManager
)
from openprocurement.auctions.geb.interfaces import (
    IAuction,
    IBid,
    IQuestion
)

LOGGER = logging.getLogger(__name__)


def includeme(config, plugin_map):

    # add procurement method types
    procurement_method_types = plugin_map.get('aliases', [])
    if plugin_map.get('use_default', False):
        procurement_method_types.append(DEFAULT_PROCUREMENT_METHOD_TYPE)
    for procurementMethodType in procurement_method_types:
        config.add_auction_procurementMethodType(Geb, procurementMethodType)

    # add views
    config.scan("openprocurement.auctions.geb.views")

    # register adapters
    config.registry.registerAdapter(AuctionManager, (IRequest, IAuction), IAuctionManager)
    config.registry.registerAdapter(BidManager, (IRequest, IBid), IBidManager)
    config.registry.registerAdapter(QuestionManager, (IRequest, IQuestion), IQuestionManager)

    LOGGER.info("Included openprocurement.auctions.geb plugin",
                extra={'MESSAGE_ID': 'included_plugin'})

    # add accreditation level
    if not plugin_map.get('accreditation'):
        config.registry.accreditation['auction'][Geb._internal_type] = DEFAULT_LEVEL_OF_ACCREDITATION
    else:
        config.registry.accreditation['auction'][Geb._internal_type] = plugin_map['accreditation']

    # migrate data
    if plugin_map['migration'] and not os.environ.get('MIGRATION_SKIP'):
        get_evenly_plugins(config, plugin_map['plugins'], 'openprocurement.auctions.geb.plugins')
