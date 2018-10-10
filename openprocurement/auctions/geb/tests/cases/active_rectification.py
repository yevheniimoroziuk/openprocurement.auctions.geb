# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.base import snitch

from openprocurement.auctions.geb.tests.base import (
    BaseWebTest
)

from openprocurement.auctions.geb.tests.helpers import (
    change_machine_state
)
from openprocurement.auctions.geb.tests.states import (
    ProcedureMachine
)

from openprocurement.auctions.geb.tests.fixtures.active_rectification import (
    ACTIVE_RECTIFICATION_AUCTION_FIXTURE_WITH_QUESTION
)

from openprocurement.auctions.geb.tests.blanks.active_rectification import (
    add_document,
    add_question,
    answer_question,
    change_bankAccount,
    change_budgetSpent,
    change_contractTerms,
    change_desctiption,
    change_guarantee,
    change_items_collections,
    change_items_singly,
    change_lotHolder,
    change_lotIdentifier,
    change_minimalStep,
    change_one_field_rest_same,
    change_procuringEntity,
    change_registrationFee,
    change_tenderAttempts,
    change_title,
    change_value,
    get_items_collection,
    get_question,
    patch_document
)


class StatusActiveRectificationChangeFieldTest(BaseWebTest):

    test_add_question = snitch(add_question)
    test_change_title = snitch(change_title)
    test_change_description = snitch(change_desctiption)
    test_change_tenderAttempts = snitch(change_tenderAttempts)
    test_change_lotIdentifier = snitch(change_lotIdentifier)
    test_change_value = snitch(change_value)
    test_change_minimalStep = snitch(change_minimalStep)
    test_change_guarantee = snitch(change_guarantee)
    test_change_budgetSpent = snitch(change_budgetSpent)
    test_change_registrationFee = snitch(change_registrationFee)
    test_change_procuringEntity = snitch(change_procuringEntity)
    test_change_lotHolder = snitch(change_lotHolder)
    test_change_bankAccount = snitch(change_bankAccount)
    test_change_contractTerms = snitch(change_contractTerms)
    test_change_one_field_rest_same = snitch(change_one_field_rest_same)

    def setUp(self):
        super(StatusActiveRectificationChangeFieldTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        change_machine_state(procedure, 'active.rectification')
        context = procedure.snapshot()
        self.auction = context['auction']
        self.items = context['items']

        entrypoints = {}

        entrypoints['patch_auction'] = '/auctions/{}?acc_token={}'.format(self.auction['data']['id'],
                                                                          self.auction['access']['token'])
        entrypoints['post_question'] = '/auctions/{}/questions'.format(self.auction['data']['id'])
        entrypoints['get_auction'] = '/auctions/{}'.format(self.auction['data']['id'])

        self.ENTRYPOINTS = entrypoints


class StatusActiveRectificationQuestionsTest(BaseWebTest):

    test_answer_question = snitch(answer_question)
    test_get_question = snitch(get_question)

    def setUp(self):
        super(StatusActiveRectificationQuestionsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.rectification')
        context = procedure.snapshot(fixture=ACTIVE_RECTIFICATION_AUCTION_FIXTURE_WITH_QUESTION)

        self.auction = context['auction']
        self.question = context['questions'][0]

        entrypoints = {}

        entrypoints['patch_question'] = '/auctions/{}/questions/{}?acc_token={}'.format(self.auction['data']['id'],
                                                                                        self.question['data']['id'],
                                                                                        self.auction['access']['token'])

        entrypoints['question'] = '/auctions/{}/questions/{}'.format(self.auction['data']['id'],
                                                                     self.question['data']['id'])
        self.ENTRYPOINTS = entrypoints


class StatusActiveRectificationItemsTest(BaseWebTest):

    test_change_items_collections = snitch(change_items_collections)
    test_change_items_singly = snitch(change_items_singly)
    test_get_items_collection = snitch(get_items_collection)

    def setUp(self):
        super(StatusActiveRectificationItemsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.rectification')
        context = procedure.snapshot()

        auction = context['auction']
        item = context['items'][0]

        entrypoints = {}

        entrypoints['patch_auction'] = '/auctions/{}?acc_token={}'.format(auction['data']['id'],
                                                                          auction['access']['token'])

        entrypoints['get_auction'] = '/auctions/{}'.format(auction['data']['id'])

        entrypoints['patch_item'] = '/auctions/{}/items/{}?acc_token={}'.format(auction['data']['id'],
                                                                                item['data']['id'],
                                                                                auction['access']['token'])

        entrypoints['get_item'] = '/auctions/{}/items/{}'.format(auction['data']['id'],
                                                                 item['data']['id'])

        entrypoints['get_items_collection'] = '/auctions/{}/items'.format(auction['data']['id'])

        self.auction = auction
        self.item = item
        self.items = context['items']
        self.ENTRYPOINTS = entrypoints


class StatusActiveRectificationDocumentTest(BaseWebTest):
    docservice = True

    test_add_document = snitch(add_document)
    test_patch_document = snitch(patch_document)

    def setUp(self):
        super(StatusActiveRectificationDocumentTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        change_machine_state(procedure, 'active.rectification')
        self.procedure = procedure


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(StatusActiveRectificationChangeFieldTest))
    suite.addTest(unittest.makeSuite(StatusActiveRectificationDocumentTest))
    suite.addTest(unittest.makeSuite(StatusActiveRectificationQuestionsTest))
    suite.addTest(unittest.makeSuite(StatusActiveRectificationItemsTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
