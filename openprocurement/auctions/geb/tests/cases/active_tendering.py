# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.geb.tests.base import (
    BaseWebTest,
)

from openprocurement.auctions.geb.tests.states import (
    ProcedureMachine
)
from openprocurement.auctions.geb.tests.fixtures.active_tendering import (
    ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE,
    ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE_WITH_BIDS,
    ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE_WITH_QUESTION
)

from openprocurement.auctions.geb.tests.blanks.active_tendering import (
    activate_bid,
    add_bid,
    get_bid,
    add_bid_document,
    add_document,
    add_invalid_bid,
    add_question,
    answer_question,
    delete_bid,
    get_question,
    make_active_status_bid
)


class StatusActiveTenderingTest(BaseWebTest):

    test_add_question = snitch(add_question)
    test_add_bid = snitch(add_bid)
    test_add_invalid_bid = snitch(add_invalid_bid)

    def setUp(self):
        super(StatusActiveTenderingTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot()

        self.auction = context['auction']

        entrypoints = {}
        entrypoints['questions'] = '/auctions/{}/questions'.format(self.auction['data']['id'])
        entrypoints['bids'] = '/auctions/{}/bids'.format(self.auction['data']['id'])

        self.ENTRYPOINTS = entrypoints


class StatusActiveTenderingQuestionsTest(BaseWebTest):

    test_answer_question = snitch(answer_question)
    test_get_question = snitch(get_question)

    def setUp(self):
        super(StatusActiveTenderingQuestionsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE_WITH_QUESTION)

        self.auction = context['auction']
        self.questions = context['questions']


class StatusActiveTenderingBidsTest(BaseWebTest):
    docservice = True

    test_add_bid_document = snitch(add_bid_document)
    test_get_bid = snitch(get_bid)
    test_activate_bid = snitch(activate_bid)
    test_make_active_status_bid = snitch(make_active_status_bid)
    test_delete_bid = snitch(delete_bid)

    def setUp(self):
        super(StatusActiveTenderingBidsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE_WITH_BIDS)

        self.auction = context['auction']
        self.bids = context['bids']


class StatusActiveTenderingDocumentsTest(BaseWebTest):
    docservice = True

    test_add_document = snitch(add_document)

    def setUp(self):
        super(StatusActiveTenderingDocumentsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE)

        self.auction = context['auction']

        entrypoints = {}
        entrypoints['documents'] = '/auctions/{}/documents?acc_token={}'.format(self.auction['data']['id'],
                                                                                self.auction['access']['token'])

        self.ENTRYPOINTS = entrypoints


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(StatusActiveTenderingTest))
    suite.addTest(unittest.makeSuite(StatusActiveTenderingQuestionsTest))
    suite.addTest(unittest.makeSuite(StatusActiveTenderingBidsTest))
    suite.addTest(unittest.makeSuite(StatusActiveTenderingDocumentsTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
