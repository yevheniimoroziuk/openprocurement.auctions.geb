# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.base import snitch

from openprocurement.auctions.geb.tests.base import (
    test_auction_data,
    BaseAuctionWebTest
)

from openprocurement.auctions.geb.tests.states import (Procedure)
from openprocurement.auctions.geb.tests.helpers import (
   get_procedure_state
)

from openprocurement.auctions.geb.tests.blanks.active_rectification import (
    change_title,
    change_desctiption,
    change_tenderAttempts,
    change_lotIdentifier,
    change_value,
    change_minimalStep,
    change_guarantee,
    change_items,
    change_invalid_tenderAttempts,
    change_budgetSpent,
    change_registrationFee,
    change_procuringEntity,
    change_lotHolder,
    change_bankAccount,
    change_contractTerms,
    add_document
)


class StatusActiveRectificationChangeFieldTest(BaseAuctionWebTest):
    initial_data = test_auction_data

    test_change_title = snitch(change_title)
    test_change_description = snitch(change_desctiption)
    test_change_tenderAttempts = snitch(change_tenderAttempts)
    test_change_lotIdentifier = snitch(change_lotIdentifier)
    test_change_value = snitch(change_value)
    test_change_minimalStep = snitch(change_minimalStep)
    test_change_guarantee = snitch(change_guarantee)
    test_change_items = snitch(change_items)
    test_change_invalid_tenderAttempts = snitch(change_invalid_tenderAttempts)
    test_change_budgetSpent = snitch(change_budgetSpent)
    test_change_registrationFee = snitch(change_registrationFee)
    test_change_procuringEntity = snitch(change_procuringEntity)
    test_change_lotHolder = snitch(change_lotHolder)
    test_change_bankAccount = snitch(change_bankAccount)
    test_change_contractTerms = snitch(change_contractTerms)

    def setUp(self):
        super(StatusActiveRectificationChangeFieldTest, self).setUp()

        procedure = Procedure(self.auction,
                              {"token": self.auction_token},
                              self)
        state = get_procedure_state(procedure, 'active.rectification')
        self.auction = state.auction
        self.entrypoint = '/auctions/{}?acc_token={}'.format(self.auction_id,
                                                             self.auction_token)


class StatusActiveRectificationDocumentTest(BaseAuctionWebTest):
    docservice = True

    def setUp(self):
        super(StatusActiveRectificationDocumentTest, self).setUp()
        procedure = Procedure(self.auction,
                              {"token": self.auction_token},
                              self)
        state = get_procedure_state(procedure, 'active.rectification')
        self.auction = state.auction
        self.entrypoint = '/auctions/{}/documents/?acc_token={}'.format(self.auction_id,
                                                                        self.auction_token)

    test_add_document = snitch(add_document)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(StatusActiveRectificationChangeFieldTest))
    suite.addTest(unittest.makeSuite(StatusActiveRectificationDocumentTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
