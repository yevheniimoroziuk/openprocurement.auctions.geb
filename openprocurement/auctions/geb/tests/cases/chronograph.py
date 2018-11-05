# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.geb.tests.base import (
    BaseWebTest,
)

from openprocurement.auctions.geb.tests.states import (
    ProcedureMachine
)
from openprocurement.auctions.geb.tests.blanks.chronograph import (
    set_auctionPeriod_startDate_rectification,
    set_auctionPeriod_startDate_tendering,
    set_auctionPeriod_startDate_enquiring,
    check_enquiry_period_end_active_auction,
    check_enquiry_period_end_active_qualification,
    check_enquiry_period_end_set_unsuccessful_bids,
    check_enquiry_period_end_unsuccessful,
    check_rectification_period_end,
    check_tender_period_end_delete_draft_bids,
    check_tender_period_end_no_active_bids,
    check_tender_period_end_no_minNumberOfQualifiedBids,
    check_tender_period_end_successful,
    replaning_auction
)


class ChronographRectificationTest(BaseWebTest):
    test_set_auctionPeriod_startDate_rectification = snitch(set_auctionPeriod_startDate_rectification)

    def setUp(self):
        super(ChronographRectificationTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.rectification')
        context = procedure.snapshot()

        self.auction = context['auction']

        entrypoints = {}
        entrypoints['auction'] = '/auctions/{}'.format(self.auction['data']['id'])
        self.ENTRYPOINTS = entrypoints

        self.app.authorization = ('Basic', ('chronograph', ''))


class ChronographEndRectificationTest(BaseWebTest):
    test_check_rectification_period_end = snitch(check_rectification_period_end)

    def setUp(self):
        super(ChronographEndRectificationTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.rectification', end=True)
        context = procedure.snapshot()

        self.auction = context['auction']

        entrypoints = {}
        entrypoints['auction'] = '/auctions/{}'.format(self.auction['data']['id'])
        self.ENTRYPOINTS = entrypoints

        self.app.authorization = ('Basic', ('chronograph', ''))


class ChronographTenderingTest(BaseWebTest):

    test_set_auctionPeriod_startDate_tendering = snitch(set_auctionPeriod_startDate_tendering)

    def setUp(self):
        super(ChronographTenderingTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')

        self.procedure = procedure
        self.app.authorization = ('Basic', ('chronograph', ''))


class ChronographEndTenderingTest(BaseWebTest):

    test_check_tender_period_end_no_active_bids = snitch(check_tender_period_end_no_active_bids)
    test_check_tender_period_end_no_minNumberOfQualifiedBids = snitch(check_tender_period_end_no_minNumberOfQualifiedBids)
    test_check_tender_period_end_delete_draft_bids = snitch(check_tender_period_end_delete_draft_bids)
    test_check_tender_period_end_successful = snitch(check_tender_period_end_successful)

    def setUp(self):
        super(ChronographEndTenderingTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering', end=True)

        self.procedure = procedure
        self.app.authorization = ('Basic', ('chronograph', ''))


class ChronographEnquiryTest(BaseWebTest):

    test_check_enquiry_period_end_unsuccessful = snitch(check_enquiry_period_end_unsuccessful)
    test_check_enquiry_period_end_active_auction = snitch(check_enquiry_period_end_active_auction)
    test_check_enquiry_period_end_active_qualification = snitch(check_enquiry_period_end_active_qualification)
    test_check_enquiry_period_end_set_unsuccessful_bids = snitch(check_enquiry_period_end_set_unsuccessful_bids)
    test_set_auctionPeriod_startDate_enquiring = snitch(set_auctionPeriod_startDate_enquiring)

    def setUp(self):
        super(ChronographEnquiryTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.enquiry')

        self.procedure = procedure
        self.app.authorization = ('Basic', ('chronograph', ''))


class ChronographEndEnquiryTest(BaseWebTest):

    test_check_enquiry_period_end_unsuccessful = snitch(check_enquiry_period_end_unsuccessful)
    test_check_enquiry_period_end_active_auction = snitch(check_enquiry_period_end_active_auction)
    test_check_enquiry_period_end_active_qualification = snitch(check_enquiry_period_end_active_qualification)
    test_check_enquiry_period_end_set_unsuccessful_bids = snitch(check_enquiry_period_end_set_unsuccessful_bids)

    def setUp(self):
        super(ChronographEndEnquiryTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.enquiry', end=True)

        self.procedure = procedure
        self.app.authorization = ('Basic', ('chronograph', ''))


class ChronographReplaningAuctionTest(BaseWebTest):

    test_replaning_auction = snitch(replaning_auction)

    def setUp(self):
        super(ChronographReplaningAuctionTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.auction')

        context = procedure.snapshot()
        auction = context['auction']

        entrypoints = {}

        pattern = '/auctions/{}?acc_token={}'
        entrypoints['auction_patch'] = pattern.format(auction['data']['id'], auction['access']['token'])

        pattern = '/auctions/{}'
        entrypoints['auction_get'] = pattern.format(auction['data']['id'])
        self.auction = auction
        self.ENTRYPOINTS = entrypoints
        self.app.authorization = ('Basic', ('chronograph', ''))


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ChronographRectificationTest))
    suite.addTest(unittest.makeSuite(ChronographTenderingTest))
    suite.addTest(unittest.makeSuite(ChronographEnquiryTest))
    suite.addTest(unittest.makeSuite(ChronographReplaningAuctionTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
