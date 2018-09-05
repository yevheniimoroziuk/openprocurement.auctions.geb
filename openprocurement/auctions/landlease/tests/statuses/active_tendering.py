# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.landlease.tests.base import (
    test_auction_data,
    BaseAuctionWebTest,
)

from openprocurement.auctions.landlease.tests.states import (
    Procedure
)

from openprocurement.auctions.landlease.tests.helpers import (
   get_procedure_state
)

from openprocurement.auctions.landlease.tests.blanks.active_tendering import (
    add_document,
    add_question
)


class StatusActiveTenderingTest(BaseAuctionWebTest):
    initial_data = test_auction_data

    test_add_question = snitch(add_question)

    def setUp(self):
        super(StatusActiveTenderingTest, self).setUp()

        procedure = Procedure(self.auction,
                              {"token": self.auction_token},
                              self)
        state = get_procedure_state(procedure, 'active.tendering')
        self.auction = state.auction
        self.entrypoint = '/auctions/{}?acc_token={}'.format(self.auction_id,
                                                             self.auction_token)


class StatusActiveTenderingDocumentTest(BaseAuctionWebTest):
    initial_data = test_auction_data
    docservice = True

    test_add_document = snitch(add_document)

    def setUp(self):
        super(StatusActiveTenderingDocumentTest, self).setUp()

        procedure = Procedure(self.auction,
                              {"token": self.auction_token},
                              self)
        state = get_procedure_state(procedure, 'active.tendering')
        self.auction = state.auction
        self.entrypoint = '/auctions/{}/documents/?acc_token={}'.format(self.auction_id,
                                                                        self.auction_token)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(StatusActiveTenderingTest))
    suite.addTest(unittest.makeSuite(StatusActiveTenderingDocumentTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
