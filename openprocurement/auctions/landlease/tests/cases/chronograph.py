# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.landlease.tests.base import (
    test_auction_data,
    BaseAuctionWebTest,
)

from openprocurement.auctions.landlease.tests.states import (
    Procedure
)

from openprocurement.auctions.landlease.tests.helpers import (
    get_procedure_state
)


from openprocurement.auctions.landlease.tests.blanks.chronograph import (
    set_auctionPeriod,
    check_tender_period_end,
    check_rectification_period_end
)


class ChronographRectificationTest(BaseAuctionWebTest):
    initial_data = test_auction_data

    test_set_auction_period = snitch(set_auctionPeriod)
    test_check_rectification_period_end = snitch(check_rectification_period_end)

    def setUp(self):
        super(ChronographRectificationTest, self).setUp()

        procedure = Procedure(self.auction,
                              {"token": self.auction_token},
                              self)
        state = get_procedure_state(procedure, 'active.rectification')
        entrypoints = {}
        self.auction = state.auction
        self.app.authorization = ('Basic', ('chronograph', ''))

        entrypoints['auction'] = '/auctions/{}'.format(self.auction_id)
        self.ENTRYPOINTS = entrypoints


class ChronographTenderingTest(BaseAuctionWebTest):
    initial_data = test_auction_data

    test_check_tender_period_end = snitch(check_tender_period_end)

    def setUp(self):
        super(ChronographTenderingTest, self).setUp()

        procedure = Procedure(self.auction,
                              {"token": self.auction_token},
                              self)
        state = get_procedure_state(procedure, 'active.tendering')
        entrypoints = {}
        self.auction = state.auction
        self.app.authorization = ('Basic', ('chronograph', ''))

        entrypoints['auction'] = '/auctions/{}'.format(self.auction_id)
        self.ENTRYPOINTS = entrypoints


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ChronographRectificationTest))
    suite.addTest(unittest.makeSuite(ChronographTenderingTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
