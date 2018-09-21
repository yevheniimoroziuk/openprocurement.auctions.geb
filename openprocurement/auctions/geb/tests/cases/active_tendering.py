# -*- coding: utf-8 -*-
import os
import unittest

from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.geb.tests.base import (
    BaseWebTest,
)

from openprocurement.auctions.geb.tests.states import (
    ProcedureMachine
)
from openprocurement.auctions.geb.tests.fixtures.active_tendering import (
    ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE_WITH_QUESTION
)

from openprocurement.auctions.geb.tests.blanks.active_tendering import (
    add_document,
    add_question,
    answer_question,
    add_bid,
    add_invalid_bid,
    add_document_to_bid,
    activate_bid,
    make_active_status_bid,
    delete_bid
)


class StatusActiveTenderingTest(BaseWebTest):

    test_add_question = snitch(add_question)

    def setUp(self):
        super(StatusActiveTenderingTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot()

        self.auction = context['auction']
        self.entrypoint = '/auctions/{}/questions'.format(self.auction['data']['id'])


class StatusActiveTenderingQuestionsTest(BaseWebTest):

    test_answer_question = snitch(answer_question)
    # test_get__question

    def setUp(self):
        super(StatusActiveTenderingQuestionsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE_WITH_QUESTION)

        self.auction = context['auction']
        self.questions = context['questions']


#class StatusActiveTenderingBidsTest(BaseWebTest):
#    docservice = True
#
#    test_add_bid = snitch(add_bid)
#    test_add_invalid_bid = snitch(add_invalid_bid)
#    # test_add_document_to_bid = snitch(add_document_to_bid)
#    # get_auction_bidder
#    test_activate_bid = snitch(activate_bid)
#    test_make_active_status_bid = snitch(make_active_status_bid)
#    test_delete_bid = snitch(delete_bid)
#
#    def setUp(self):
#        super(StatusActiveTenderingBidsTest, self).setUp()
#
#        procedure = ProcedureMachine()
#        self.auction = state.auction
#        bid_context = create_bid(self, self.auction)
#        self.bid_token = bid_context['access']['token']
#        access = bid_context['access']
#        self.bid = bid_context['data']
#        entrypoints = {}
#        add_document = '/auctions/{}/bids/{}/documents?acc_token={}'.format(self.auction_id,
#                                                                            self.bid['id'],
#                                                                            access['token'])
#        entrypoints['create_bid'] = '/auctions/{}/bids'.format(self.auction_id)
#
#        entrypoints['add_document'] = add_document
#
#        edit_bid = '/auctions/{}/bids/{}?acc_token={}'.format(self.auction_id,
#                                                              self.bid['id'],
#                                                              access['token'])
#        entrypoints['bid'] = edit_bid
#        self.ENTRYPOINTS = entrypoints


#class StatusActiveTenderingDocumentsTest(BaseAuctionWebTest):
#    initial_data = test_auction_data
#    docservice = True
#
#    test_add_document = snitch(add_document)
#
#    def setUp(self):
#        super(StatusActiveTenderingDocumentsTest, self).setUp()
#
#        procedure = Procedure(self.auction,
#                              {"token": self.auction_token},
#                              self)
#        state = get_procedure_state(procedure, 'active.tendering')
#        self.auction = state.auction
#        self.entrypoint = '/auctions/{}/documents/?acc_token={}'.format(self.auction_id,
#                                                                        self.auction_token)
#
#    def tearDown(self):
#        os.environ.pop('FAKE_NOW')


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(StatusActiveTenderingTest))
    suite.addTest(unittest.makeSuite(StatusActiveTenderingQuestionsTest))
    #suite.addTest(unittest.makeSuite(StatusActiveTenderingBidsTest))
    #suite.addTest(unittest.makeSuite(StatusActiveTenderingDocumentsTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
