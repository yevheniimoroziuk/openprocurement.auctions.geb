
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
    ACTIVE_ENQUIRY_AUCTION_DEFAULT_FIXTURE_WITH_NOT_ACTIVE_BID
)
from openprocurement.auctions.geb.tests.blanks.active_enquiry import (
    add_bid,
    add_bid_document,
    add_document,
    add_question,
    answer_question,
    delete_bid,
    get_bid,
    get_question,
    make_active_status_bid
)


class StatusActiveEnquiryTest(BaseWebTest):

    test_add_bid = snitch(add_bid)
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


class StatusActiveEnquiryBidsTest(BaseWebTest):
    docservice = True

    test_add_bid_document = snitch(add_bid_document)
    test_get_bid = snitch(get_bid)
    test_delete_bid = snitch(delete_bid)
    test_make_active_status_bid = snitch(make_active_status_bid)

    def setUp(self):
        super(StatusActiveEnquiryBidsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.enquiry')
        context = procedure.snapshot(fixture=ACTIVE_ENQUIRY_AUCTION_DEFAULT_FIXTURE_WITH_NOT_ACTIVE_BID)

        self.auction = context['auction']
        self.bids = context['bids']


class StatusActiveEnquiryDocumentsTest(BaseWebTest):
    docservice = True

    test_add_document = snitch(add_document)

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
    suite.addTest(unittest.makeSuite(StatusActiveEnquiryBidsTest))
    suite.addTest(unittest.makeSuite(StatusActiveEnquiryDocumentsTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
