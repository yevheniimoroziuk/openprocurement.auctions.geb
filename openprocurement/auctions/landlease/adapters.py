# -*- coding: utf-8 -*-
from openprocurement.auctions.core.adapters import (
    AuctionConfigurator,
    AuctionManagerAdapter
)
from openprocurement.auctions.landlease.models import (
    LandLease
)
from openprocurement.auctions.core.plugins.awarding.v2_1.adapters import (
    AwardingV2_1ConfiguratorMixin
)


class AuctionLandLeaseConfigurator(AuctionConfigurator,
                                     AwardingV2_1ConfiguratorMixin):
    name = 'Auction LandLease Configurator'
    model = LandLease


class AuctionLandLeaseManagerAdapter(AuctionManagerAdapter):

    def create_auction(self, request):
        pass

    def change_auction(self, request):
        pass
