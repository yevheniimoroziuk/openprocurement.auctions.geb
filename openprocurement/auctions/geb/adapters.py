# -*- coding: utf-8 -*-
from openprocurement.auctions.core.adapters import (
    AuctionConfigurator
)
from openprocurement.auctions.core.plugins.awarding.v3_1.adapters import (
    AwardingV3_1ConfiguratorMixin
)

from openprocurement.auctions.geb.models.schemas import (
    Auction
)


class AuctionConfigurator(AuctionConfigurator,
                          AwardingV3_1ConfiguratorMixin):
    name = 'Auction Geb Configurator'
    model = Auction
