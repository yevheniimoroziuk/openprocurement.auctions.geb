# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.base import snitch

from openprocurement.auctions.landlease.tests.base import (
    test_auction_data,
    BaseAuctionWebTest
)

from openprocurement.auctions.landlease.tests.helpers import get_next_status

from openprocurement.auctions.landlease.tests.blanks.active_rectification import (
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
        next_status = get_next_status(self.auction['status'])

        self.entrypoint = '/auctions/{}?acc_token={}'.format(self.auction_id,
                                                             self.auction_token)
        request_data = {"data": {"status": next_status}}
        self.app.patch_json(self.entrypoint, request_data)
        response = self.app.get('/auctions/{}'.format(self.auction_id))
        self.auction = response.json['data']


class StatusActiveRectificationDocumentTest(BaseAuctionWebTest):
    docservice = True

    def setUp(self):
        super(StatusActiveRectificationDocumentTest, self).setUp()
        next_status = get_next_status(self.auction['status'])

        self.entrypoint = '/auctions/{}?acc_token={}'.format(self.auction_id,
                                                             self.auction_token)
        request_data = {"data": {"status": next_status}}
        self.app.patch_json(self.entrypoint, request_data)
        response = self.app.get('/auctions/{}'.format(self.auction_id))
        self.auction = response.json['data']
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
