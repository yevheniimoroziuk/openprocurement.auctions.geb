
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
from openprocurement.auctions.geb.tests.blanks.active_enquiry import (
    add_document,
    add_question,
    answer_question,
    add_bid,
    add_invalid_bid,
    add_document_to_bid,
    make_active_status_bid,
    delete_bid
)


class StatusActiveEnquiryQuestionsTest(BaseAuctionWebTest):
    initial_data = test_auction_data

    test_add_question = snitch(add_question)
    test_answer_question = snitch(answer_question)

    def setUp(self):
        super(StatusActiveEnquiryQuestionsTest, self).setUp()

        procedure = Procedure(self.auction,
                              {"token": self.auction_token},
                              self)
        state = get_procedure_state(procedure, 'active.enquiry')
        self.auction = state.auction
        self.entrypoint = '/auctions/{}/questions'.format(self.auction_id)


class StatusActiveEnquiryBidsTest(BaseAuctionWebTest):
    initial_data = test_auction_data
    docservice = True

    test_add_bid = snitch(add_bid)
    test_add_invalid_bid = snitch(add_invalid_bid)
    test_add_document_to_bid = snitch(add_document_to_bid)
    test_make_active_status_bid = snitch(make_active_status_bid)
    test_delete_bid = snitch(delete_bid)

    def setUp(self):
        super(StatusActiveEnquiryBidsTest, self).setUp()

        procedure = Procedure(self.auction,
                              {"token": self.auction_token},
                              self)
        state = get_procedure_state(procedure, 'active.enquiry')
        self.auction = state.auction
        for bid in state.extra['bids']:
            access = bid['access']
            bid_owner = bid['owner']
            bid = bid['data']
            break

        self.bid = bid
        self.bid_token = access['token']
        self.app.authorization = bid_owner
        entrypoints = {}
        add_document = '/auctions/{}/bids/{}/documents?acc_token={}'.format(self.auction_id,
                                                                            self.bid['id'],
                                                                            access['token'])
        entrypoints['create_bid'] = '/auctions/{}/bids'.format(self.auction_id)

        entrypoints['add_document'] = add_document

        edit_bid = '/auctions/{}/bids/{}?acc_token={}'.format(self.auction_id,
                                                              self.bid['id'],
                                                              access['token'])
        entrypoints['bid'] = edit_bid
        self.ENTRYPOINTS = entrypoints


class StatusActiveEnquiryDocumentsTest(BaseAuctionWebTest):
    initial_data = test_auction_data
    docservice = True

    test_add_document = snitch(add_document)

    def setUp(self):
        super(StatusActiveEnquiryDocumentsTest, self).setUp()

        procedure = Procedure(self.auction,
                              {"token": self.auction_token},
                              self)
        state = get_procedure_state(procedure, 'active.enquiry')
        self.auction = state.auction
        self.entrypoint = '/auctions/{}/documents/?acc_token={}'.format(self.auction_id,
                                                                        self.auction_token)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(StatusActiveEnquiryQuestionsTest))
    suite.addTest(unittest.makeSuite(StatusActiveEnquiryBidsTest))
    suite.addTest(unittest.makeSuite(StatusActiveEnquiryDocumentsTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
