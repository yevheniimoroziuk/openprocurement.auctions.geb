import logging
from pyramid.interfaces import IRequest

from openprocurement.auctions.geb.managers.base import (
    AuctionDocumentManager,
    AuctionManager,
    AuctionPartialManager,
    BidDocumentManager,
    BidManager,
    CancellationDocumentManager,
    CancellationManager,
    ItemManager,
    QuestionManager
)
from openprocurement.auctions.geb.managers.awarding import (
    Awarding
)
from openprocurement.auctions.geb.constants import (
    DEFAULT_PROCUREMENT_METHOD_TYPE,
    DEFAULT_LEVEL_OF_ACCREDITATION
)
from openprocurement.auctions.geb.models.schemas import (
    Auction
)

from openprocurement.auctions.core.interfaces import (
    IAuctionManager,
    IContentConfigurator,
    IManager

)
from openprocurement.auctions.geb.interfaces import (
    IAuction,
    IAuctionDocument,
    IBid,
    IBidDocument,
    ICancellation,
    ICancellationDocument,
    IItem,
    IQuestion
)

LOGGER = logging.getLogger(__name__)


def includeme(config, plugin_map):

    # add procurement method types
    procurement_method_types = plugin_map.get('aliases', [])
    if plugin_map.get('use_default', False):
        procurement_method_types.append(DEFAULT_PROCUREMENT_METHOD_TYPE)
    for procurementMethodType in procurement_method_types:
        config.add_auction_procurementMethodType(Auction, procurementMethodType)

    # add views
    config.scan("openprocurement.auctions.geb.views")

    # register adapters
    config.registry.registerAdapter(Awarding, (IAuction, IRequest), IContentConfigurator)
    config.registry.registerAdapter(AuctionManager, (IRequest, IAuction), IManager)
    config.registry.registerAdapter(AuctionPartialManager, (IAuction,), IAuctionManager)
    config.registry.registerAdapter(BidManager, (IRequest, IBid), IManager)
    config.registry.registerAdapter(BidDocumentManager, (IRequest, IBidDocument), IManager)
    config.registry.registerAdapter(QuestionManager, (IRequest, IQuestion), IManager)
    config.registry.registerAdapter(ItemManager, (IRequest, IItem), IManager)
    config.registry.registerAdapter(CancellationManager, (IRequest, ICancellation), IManager)
    config.registry.registerAdapter(CancellationDocumentManager, (IRequest, ICancellationDocument), IManager)
    config.registry.registerAdapter(AuctionDocumentManager, (IRequest, IAuctionDocument), IManager)

    LOGGER.info("Included openprocurement.auctions.geb plugin",
                extra={'MESSAGE_ID': 'included_plugin'})

    # add accreditation level
    if not plugin_map.get('accreditation'):
        config.registry.accreditation['auction'][Auction._internal_type] = DEFAULT_LEVEL_OF_ACCREDITATION
    else:
        config.registry.accreditation['auction'][Auction._internal_type] = plugin_map['accreditation']
