# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.geb.tests.base import (
    test_auction_data,
    BaseAuctionWebTest,
)

from openprocurement.auctions.geb.tests.states import (
    Procedure
)

from openprocurement.auctions.geb.tests.helpers import (
    get_procedure_state,
)
from openprocurement.auctions.geb.tests.blanks.active_auction import (
    get_auction,
    patch_auction
)


class StatusActiveAuctionTest(BaseAuctionWebTest):
    initial_data = test_auction_data

    test_get_auction = snitch(get_auction)
    test_patch_auction = snitch(patch_auction)

    def setUp(self):
        super(StatusActiveAuctionTest, self).setUp()

        procedure = Procedure(self.auction,
                              {"token": self.auction_token},
                              self)
        state = get_procedure_state(procedure, 'active.auction')
        self.auction = state.auction
        self.app.authorization = ('Basic', ('auction', ''))
        self.entrypoint = '/auctions/{}/auction'.format(self.auction['id'])


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(StatusActiveAuctionTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
