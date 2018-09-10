# -*- coding: utf-8 -*-

from openprocurement.auctions.core.adapters import (
    AuctionConfigurator as BaseAuctionConfigurator,
)
from openprocurement.auctions.landlease.models.schemas import (
    LandLease
)
from openprocurement.auctions.core.plugins.awarding.v2_1.adapters import (
    AwardingV2_1ConfiguratorMixin
)


class AuctionConfigurator(BaseAuctionConfigurator,
                          AwardingV2_1ConfiguratorMixin):
    name = 'Auction LandLease Configurator'
    model = LandLease
