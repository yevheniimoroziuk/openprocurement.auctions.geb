import os
import logging
from pyramid.interfaces import IRequest

from openprocurement.auctions.core.includeme import (
    IContentConfigurator,
    IAwardingNextCheck,
    get_evenly_plugins
)
from openprocurement.auctions.core.interfaces import IAuctionManager
from openprocurement.auctions.core.plugins.awarding.v2_1.adapters import (
    AwardingNextCheckV2_1
)

from openprocurement.auctions.landlease.adapters.managers import (
    AuctionManagerAdapter,
)

from openprocurement.auctions.landlease.adapters.configurators import (
    AuctionConfigurator,
)
from openprocurement.auctions.landlease.adapters.changers import (
    AuctionChanger
)
from openprocurement.auctions.landlease.adapters.initializators import (
    AuctionInitializator
)

from openprocurement.auctions.landlease.constants import (
    DEFAULT_LEVEL_OF_ACCREDITATION,
    DEFAULT_PROCUREMENT_METHOD_TYPE,
)
from openprocurement.auctions.landlease.models import (
    LandLease
)

from openprocurement.auctions.landlease.interfaces import (
    IAuction,
    IAuctionChanger,
    IAuctionInitializator
)

LOGGER = logging.getLogger(__name__)


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

    config.registry.registerAdapter(
        AuctionConfigurator,
        (IAuction, IRequest),
        IContentConfigurator
    )
    config.registry.registerAdapter(
        AwardingNextCheckV2_1,
        (IAuction,),
        IAwardingNextCheck
    )
    config.registry.registerAdapter(
        AuctionManagerAdapter,
        (IAuction,),
        IAuctionManager
    )

    config.registry.registerAdapter(
        AuctionInitializator,
        (IAuction,),
        IAuctionInitializator
    )

    config.registry.registerAdapter(
        AuctionChanger,
        (IRequest, IAuction),
        IAuctionChanger
    )

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
