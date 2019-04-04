# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.geb.tests.base import (
    BaseWebTest,
)

from openprocurement.auctions.geb.tests.states import (
    ProcedureMachine
)
from openprocurement.auctions.geb.tests.blanks.auction_period_patch import (
    set_auctionPeriod_startDate_enquiring,
    set_auctionPeriod_startDate_rectification,
    set_auctionPeriod_startDate_tendering
)


class AuctionBridgeTenderingTest(BaseWebTest):
    test_set_auctionPeriod_startDate_tendering = snitch(set_auctionPeriod_startDate_tendering)

    def setUp(self):
        super(AuctionBridgeTenderingTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')

        self.procedure = procedure
        self.app.authorization = ('Basic', ('auction', ''))


class AuctionBridgeRectificationTest(BaseWebTest):
    test_set_auctionPeriod_startDate_rectification = snitch(set_auctionPeriod_startDate_rectification)

    def setUp(self):
        super(AuctionBridgeRectificationTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.rectification')
        context = procedure.snapshot()

        self.auction = context['auction']

        entrypoints = {}
        entrypoints['auction'] = '/auctions/{}'.format(self.auction['data']['id'])
        self.ENTRYPOINTS = entrypoints

        self.app.authorization = ('Basic', ('auction', ''))


class AuctionBridgeEnquiryTest(BaseWebTest):

    test_set_auctionPeriod_startDate_enquiring = snitch(set_auctionPeriod_startDate_enquiring)

    def setUp(self):
        super(AuctionBridgeEnquiryTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.enquiry')

        self.procedure = procedure
        self.app.authorization = ('Basic', ('auction', ''))


def suite():
    suite = unittest.TestSuite()
    # auction tests
    suite.addTest(unittest.makeSuite(AuctionBridgeTenderingTest))
    suite.addTest(unittest.makeSuite(AuctionBridgeEnquiryTest))
    suite.addTest(unittest.makeSuite(AuctionBridgeRectificationTest))
