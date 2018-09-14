import os
import logging
from pyramid.interfaces import IRequest

from openprocurement.auctions.core.includeme import (
    IContentConfigurator,
    get_evenly_plugins
)
from openprocurement.auctions.core.interfaces import (
    IAuctionManager,
    IAuctionInitializator
)

from openprocurement.auctions.landlease.adapters.managers import (
    BidManager,
    QuestionManager
)

from openprocurement.auctions.core.adapters import (
    AuctionManagerAdapter
)
from openprocurement.auctions.landlease.adapters.configurators import (
    AuctionConfigurator,
)
from openprocurement.auctions.landlease.adapters.changers import (
    AuctionChanger,
    QuestionChanger,
    BidChanger
)
from openprocurement.auctions.landlease.adapters.documenters import (
    AuctionDocumenter
)
from openprocurement.auctions.landlease.adapters.questioners import (
    AuctionQuestioner
)
from openprocurement.auctions.landlease.adapters.checkers import (
    AuctionChecker
)
from openprocurement.auctions.landlease.adapters.deleters import (
    BidDeleter
)
from openprocurement.auctions.landlease.adapters.initializators import (
    AuctionInitializator,
    BidInitializator
)

from openprocurement.auctions.landlease.constants import (
    DEFAULT_LEVEL_OF_ACCREDITATION,
    DEFAULT_PROCUREMENT_METHOD_TYPE,
)
from openprocurement.auctions.landlease.models.schemas import (
    LandLease
)

from openprocurement.auctions.landlease.interfaces import (
    IAuction,
    IAuctionChanger,
    IAuctionChecker,
    IAuctionDocumenter,
    IAuctionQuestioner,
    IBid,
    IBidChanger,
    IBidDeleter,
    IBidInitializator,
    IBidManager,
    IQuestion,
    IQuestionChanger,
    IQuestionManager
)

LOGGER = logging.getLogger(__name__)


def registrator(config):
    config.registry.registerAdapter(
        AuctionConfigurator,
        (IAuction, IRequest),
        IContentConfigurator
    )
# Auction Adapters
    config.registry.registerAdapter(
        AuctionManagerAdapter,
        (IRequest, IAuction),
        IAuctionManager
    )
    config.registry.registerAdapter(
        AuctionChecker,
        (IAuction,),
        IAuctionChecker
    )
    config.registry.registerAdapter(
        AuctionChanger,
        (IRequest, IAuction),
        IAuctionChanger
    )
    config.registry.registerAdapter(
        AuctionDocumenter,
        (IRequest, IAuction),
        IAuctionDocumenter
    )
    config.registry.registerAdapter(
        AuctionQuestioner,
        (IRequest, IAuction),
        IAuctionQuestioner
    )
    config.registry.registerAdapter(
        AuctionInitializator,
        (IAuction,),
        IAuctionInitializator
    )
# Bid Adapters
    config.registry.registerAdapter(
        BidManager,
        (IRequest, IBid),
        IBidManager
    )
    config.registry.registerAdapter(
        BidInitializator,
        (IBid,),
        IBidInitializator
    )
    config.registry.registerAdapter(
        BidChanger,
        (IRequest, IBid),
        IBidChanger
    )
    config.registry.registerAdapter(
        BidDeleter,
        (IRequest, IBid),
        IBidDeleter
    )
# QuestionAdapters
    config.registry.registerAdapter(
        QuestionManager,
        (IRequest, IQuestion),
        IQuestionManager
    )
    config.registry.registerAdapter(
        QuestionChanger,
        (IRequest, IQuestion),
        IQuestionChanger
    )


def includeme(config, plugin_map):
    procurement_method_types = plugin_map.get('aliases', [])
    if plugin_map.get('use_default', False):
        procurement_method_types.append(
            DEFAULT_PROCUREMENT_METHOD_TYPE
        )
    for procurementMethodType in procurement_method_types:
        config.add_auction_procurementMethodType(LandLease,
                                                 procurementMethodType)

    config.scan("openprocurement.auctions.landlease.views")
    registrator(config)

    LOGGER.info("Included openprocurement.auctions.landlease plugin",
                extra={'MESSAGE_ID': 'included_plugin'})

    # add accreditation level
    if not plugin_map.get('accreditation'):
        config.registry.accreditation['auction'][LandLease._internal_type] = DEFAULT_LEVEL_OF_ACCREDITATION
    else:
        config.registry.accreditation['auction'][LandLease._internal_type] = plugin_map['accreditation']

    # migrate data
    if plugin_map['migration'] and not os.environ.get('MIGRATION_SKIP'):
        get_evenly_plugins(config, plugin_map['plugins'], 'openprocurement.auctions.landlease.plugins')
