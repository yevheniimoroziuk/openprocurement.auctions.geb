# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.base import snitch

from openprocurement.auctions.geb.tests.base import (
    BaseWebTest
)

from openprocurement.auctions.geb.tests.states import (
    ProcedureMachine
)

from openprocurement.auctions.geb.tests.fixtures.active_rectification import (
    AUCTION_CANCELLED
)

from openprocurement.auctions.geb.tests.blanks.cancelled import (
    auction_get
)


class StatusCancelledTest(BaseWebTest):

    test_auction_get = snitch(auction_get)

    def setUp(self):
        super(StatusCancelledTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('cancelled')
        context = procedure.snapshot(fixture=AUCTION_CANCELLED)
        auction = context['auction']

        entrypoints = {}
        entrypoints['auction_get'] = '/auctions/{}'.format(auction['data']['id'])

        self.auction = auction
        self.ENTRYPOINTS = entrypoints


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(StatusCancelledTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
