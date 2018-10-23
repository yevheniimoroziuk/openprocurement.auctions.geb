# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.geb.tests.base import (
    BaseWebTest
)

from openprocurement.auctions.geb.tests.blanks.create import (
    auction_create_without_items,
    create_auction,
    create_auction_invalid_auctionPeriod,
    create_auction_check_minNumberOfQualifiedBids,
    create_auction_check_auctionParameters
)
from openprocurement.auctions.geb.tests.fixtures.create import (
    AUCTION_WITHOUT_ITEMS
)
from openprocurement.auctions.geb.tests.helpers import (
    change_machine_state
)
from openprocurement.auctions.geb.tests.states import (
    ProcedureMachine
)


class CreateAuctionResourceTest(BaseWebTest):

    test_create_auction = snitch(create_auction)
    test_create_auction_check_minNumberOfQualifiedBids = snitch(create_auction_check_minNumberOfQualifiedBids)
    test_create_auction_invalid_auctionPeriod = snitch(create_auction_invalid_auctionPeriod)
    test_create_auction_check_auctionParameters = snitch(create_auction_check_auctionParameters)

    def setUp(self):
        super(CreateAuctionResourceTest, self).setUp()
        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        change_machine_state(procedure, 'create')
        context = procedure.snapshot(dump=False)
        self.auction = context['auction']['data']


class CreateAuctionResourceWithoutItemsTest(BaseWebTest):

    test_create_auction = snitch(auction_create_without_items)

    def setUp(self):
        super(CreateAuctionResourceWithoutItemsTest, self).setUp()
        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        change_machine_state(procedure, 'create')
        context = procedure.snapshot(fixture=AUCTION_WITHOUT_ITEMS, dump=False)
        self.auction = context['auction']['data']


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CreateAuctionResourceTest))
    suite.addTest(unittest.makeSuite(CreateAuctionResourceWithoutItemsTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
