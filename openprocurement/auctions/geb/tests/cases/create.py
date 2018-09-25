# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.geb.tests.base import (
    BaseWebTest
)

from openprocurement.auctions.geb.tests.blanks.create import (
    create_auction,
)
from openprocurement.auctions.geb.tests.helpers import (
    change_machine_state
)
from openprocurement.auctions.geb.tests.states import (
    ProcedureMachine
)


class CreateAuctionResourceTest(BaseWebTest):

    test_create_auction = snitch(create_auction)

    def setUp(self):
        super(CreateAuctionResourceTest, self).setUp()
        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        change_machine_state(procedure, 'create')
        context = procedure.snapshot(dump=False)
        self.auction = context['auction']['data']


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CreateAuctionResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
