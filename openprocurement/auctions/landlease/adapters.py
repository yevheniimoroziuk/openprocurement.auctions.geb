# -*- coding: utf-8 -*-
from openprocurement.auctions.core.adapters import (
    AuctionConfigurator,
    AuctionManagerAdapter
)
from openprocurement.auctions.landlease.models import (
    Rubble
)
from openprocurement.auctions.core.plugins.awarding.v2_1.adapters import (
    AwardingV2_1ConfiguratorMixin
)


class AuctionRubbleConfigurator(AuctionConfigurator,
                                     AwardingV2_1ConfiguratorMixin):
    name = 'Auction Rubble Configurator'
    model = Rubble


class AuctionRubbleManagerAdapter(AuctionManagerAdapter):

    def create_auction(self, request):
        pass

    def change_auction(self, request):
        pass
