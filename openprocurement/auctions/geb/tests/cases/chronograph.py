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
    check_rectification_period_end,
    enquiry_switch_to_active_auction,
    enquiry_switch_to_active_qualification,
    enquiry_switch_to_active_qualification_sandbox,
    enquiry_set_unsuccessful_bids,
    enquiry_switch_to_unsuccessful_bids_min_number_1_no_bids,
    enquiry_switch_to_unsuccessful_bids_min_number_2_no_bids,
    enquiry_switch_to_unsuccessful_bids_min_number_2_bid_1_active,
    enquiry_switch_to_active_auction_bids_min_number_1_bids_2_active,
    replaning_auction,
    tendering_delete_draft_bids,
    tendering_switch_to_enquiry,
    tendering_switch_to_unsuccessful_bid_min_number_2_bid_1_active,
    tendering_switch_to_unsuccessful_only_draft_bids,
)


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


    def setUp(self):
        super(ChronographTenderingTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')

        self.procedure = procedure
        self.app.authorization = ('Basic', ('chronograph', ''))


class ChronographEndTenderingTest(BaseWebTest):

    test_tendering_switch_to_unsuccessful_only_draft_bids = snitch(tendering_switch_to_unsuccessful_only_draft_bids)
    test_tendering_switch_unsuccessful_bid_min_number_2_bid_1_active = snitch(tendering_switch_to_unsuccessful_bid_min_number_2_bid_1_active)
    test_tendering_delete_draft_bids = snitch(tendering_delete_draft_bids)
    test_tendering_switch_to_enquiry = snitch(tendering_switch_to_enquiry)

    def setUp(self):
        super(ChronographEndTenderingTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering', end=True)

        self.procedure = procedure
        self.app.authorization = ('Basic', ('chronograph', ''))


class ChronographEndEnquiryTest(BaseWebTest):

    test_enquiry_switch_to_unsuccessful_bids_min_number_2_no_bids = snitch(enquiry_switch_to_unsuccessful_bids_min_number_2_no_bids)
    test_enquiry_switch_to_unsuccessful_bids_min_number_2_bid_1_active = snitch(enquiry_switch_to_unsuccessful_bids_min_number_2_bid_1_active)
    test_enquiry_switch_to_unsuccessful_bids_min_number_1_no_bids = snitch(enquiry_switch_to_unsuccessful_bids_min_number_1_no_bids)
    test_enquiry_switch_to_active_auction_bids_min_number_1_bids_2_active = snitch(enquiry_switch_to_active_auction_bids_min_number_1_bids_2_active)
    test_enquiry_switch_to_active_auction = snitch(enquiry_switch_to_active_auction)
    test_enquiry_switch_to_active_qualification = snitch(enquiry_switch_to_active_qualification)
    test_enquiry_switch_to_active_qualification_sandbox = snitch(enquiry_switch_to_active_qualification_sandbox)
    test_enquiry_set_unsuccessful_bids = snitch(enquiry_set_unsuccessful_bids)

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
    suite.addTest(unittest.makeSuite(ChronographTenderingTest))
    suite.addTest(unittest.makeSuite(ChronographReplaningAuctionTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
