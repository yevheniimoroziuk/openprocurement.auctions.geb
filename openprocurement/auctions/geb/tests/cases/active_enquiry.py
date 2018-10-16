
# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.base import snitch

from openprocurement.auctions.geb.tests.base import (
    BaseWebTest
)
from openprocurement.auctions.geb.tests.states import (
    ProcedureMachine
)
from openprocurement.auctions.geb.tests.fixtures.active_enquiry import (
    ACTIVE_ENQUIRY_AUCTION_DEFAULT_FIXTURE_WITH_QUESTION,
    AUCTION_WITH_PENDING_BID,
    AUCTION_WITH_ACTIVE_BID
)
from openprocurement.auctions.geb.tests.blanks.active_enquiry import (
    add_document,
    add_offline_document,
    add_question,
    answer_question,
    get_question,
    bid_add,
    bid_add_document_in_active_status,
    bid_add_document_in_pending_status,
    bid_delete_in_active_status,
    bid_delete_in_pending_status,
    bid_get_in_active_status,
    bid_get_in_pending_status,
    bid_make_activate,
    bid_patch_in_active_status,
    bid_patch_in_pending_status,
)


class StatusActiveEnquiryTest(BaseWebTest):

    test_bid_add = snitch(bid_add)
    test_add_question = snitch(add_question)

    def setUp(self):
        super(StatusActiveEnquiryTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.enquiry')
        context = procedure.snapshot()

        self.auction = context['auction']

        entrypoints = {}
        entrypoints['questions'] = '/auctions/{}/questions'.format(self.auction['data']['id'])
        entrypoints['bids'] = '/auctions/{}/bids'.format(self.auction['data']['id'])

        self.ENTRYPOINTS = entrypoints


class StatusActiveEnquiryQuestionsTest(BaseWebTest):

    test_answer_question = snitch(answer_question)
    test_get_question = snitch(get_question)

    def setUp(self):
        super(StatusActiveEnquiryQuestionsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.enquiry')
        context = procedure.snapshot(fixture=ACTIVE_ENQUIRY_AUCTION_DEFAULT_FIXTURE_WITH_QUESTION)

        self.auction = context['auction']
        self.questions = context['questions']


class StatusActiveEnquiryPendingBidsTest(BaseWebTest):
    docservice = True

    test_bid_patch_in_pending_status = snitch(bid_patch_in_pending_status)
    test_bid_make_activate = snitch(bid_make_activate)
    test_bid_add_document_in_pending_status = snitch(bid_add_document_in_pending_status)
    test_bid_delete_in_pending_status = snitch(bid_delete_in_pending_status)
    test_bid_get_in_pending_status = snitch(bid_get_in_pending_status)
    test_bid_patch_in_pending_status = snitch(bid_patch_in_pending_status)

    def setUp(self):
        super(StatusActiveEnquiryPendingBidsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.enquiry')
        context = procedure.snapshot(fixture=AUCTION_WITH_PENDING_BID)

        auction = context['auction']
        bid = context['bids'][0]

        entrypoints = {}

        pattern = '/auctions/{auction}/bids/{bid}?acc_token={token}'
        entrypoints['bid'] = pattern.format(auction=auction['data']['id'],
                                            bid=bid['data']['id'],
                                            token=bid['access']['token'])

        pattern = '/auctions/{auction}/bids/{bid}/documents?acc_token={token}'
        entrypoints['add_bid_document'] = pattern.format(auction=auction['data']['id'],
                                                         bid=bid['data']['id'],
                                                         token=bid['access']['token'])
        self.ENTRYPOINTS = entrypoints
        self.bid = bid
        self.auction = auction


class StatusActiveEnquiryActiveBidsTest(BaseWebTest):
    docservice = True

    test_bid_patch_in_active_status = snitch(bid_patch_in_active_status)
    test_bid_add_document_in_active_status = snitch(bid_add_document_in_active_status)
    test_bid_delete_in_active_status = snitch(bid_delete_in_active_status)
    test_bid_get_in_active_status = snitch(bid_get_in_active_status)
    test_bid_patch_in_active_status = snitch(bid_patch_in_active_status)

    def setUp(self):
        super(StatusActiveEnquiryActiveBidsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.enquiry')
        context = procedure.snapshot(fixture=AUCTION_WITH_ACTIVE_BID)

        auction = context['auction']
        bid = context['bids'][0]

        entrypoints = {}

        pattern = '/auctions/{auction}/bids/{bid}?acc_token={token}'
        entrypoints['bid'] = pattern.format(auction=auction['data']['id'],
                                            bid=bid['data']['id'],
                                            token=bid['access']['token'])

        pattern = '/auctions/{auction}/bids/{bid}/documents?acc_token={token}'
        entrypoints['add_bid_document'] = pattern.format(auction=auction['data']['id'],
                                                         bid=bid['data']['id'],
                                                         token=bid['access']['token'])
        self.ENTRYPOINTS = entrypoints
        self.bid = bid
        self.auction = auction


class StatusActiveEnquiryDocumentsTest(BaseWebTest):
    docservice = True

    test_add_document = snitch(add_document)
    test_add_offline_document = snitch(add_offline_document)

    def setUp(self):
        super(StatusActiveEnquiryDocumentsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot()

        self.auction = context['auction']

        entrypoints = {}
        entrypoints['documents'] = '/auctions/{}/documents?acc_token={}'.format(self.auction['data']['id'],
                                                                                self.auction['access']['token'])

        self.ENTRYPOINTS = entrypoints


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(StatusActiveEnquiryTest))
    suite.addTest(unittest.makeSuite(StatusActiveEnquiryQuestionsTest))
    suite.addTest(unittest.makeSuite(StatusActiveEnquiryDocumentsTest))
    suite.addTest(unittest.makeSuite(StatusActiveEnquiryPendingBidsTest))
    suite.addTest(unittest.makeSuite(StatusActiveEnquiryActiveBidsTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
