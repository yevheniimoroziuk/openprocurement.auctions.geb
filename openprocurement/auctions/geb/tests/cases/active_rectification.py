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
    AUCTION_WITH_QUESTIONS,
    AUCTION_WITHOUT_ITEMS,
    AUCTION_WITH_CANCELLATION,
    AUCTION_WITH_CANCELLATION_WITH_DOCUMENTS
)

from openprocurement.auctions.geb.tests.blanks.cancellations import (
    cancellation_post
)
from openprocurement.auctions.geb.tests.blanks.mixins import (
    CancellationWorkFlowMixin,
    CancellationDocumentsWorkFlowMixin
)

from openprocurement.auctions.geb.tests.blanks.active_rectification import (
    add_document,
    add_offline_document,
    add_question,
    answer_question,
    change_bankAccount,
    change_budgetSpent,
    change_contractTerms,
    change_desctiption,
    change_guarantee,
    change_lotHolder,
    change_lotIdentifier,
    change_minNumberOfQualifiedBids,
    change_minimalStep,
    change_one_field_rest_same,
    change_procuringEntity,
    change_registrationFee,
    change_tenderAttempts,
    change_title,
    change_value,
    get_question,
    item_patch,
    item_post,
    item_get,
    items_get_listing,
    items_patch_collections,
    items_patch_collections_blank_items,
    patch_document,
    put_document,
    download_document
)


class StatusActiveRectificationTest(BaseWebTest):

    test_add_question = snitch(add_question)
    test_cancellation_post = snitch(cancellation_post)
    test_change_title = snitch(change_title)
    test_change_description = snitch(change_desctiption)
    test_change_tenderAttempts = snitch(change_tenderAttempts)
    test_change_lotIdentifier = snitch(change_lotIdentifier)
    test_change_value = snitch(change_value)
    test_change_minimalStep = snitch(change_minimalStep)
    test_change_guarantee = snitch(change_guarantee)
    test_change_budgetSpent = snitch(change_budgetSpent)
    test_change_registrationFee = snitch(change_registrationFee)
    test_change_minNumberOfQualifiedBids = snitch(change_minNumberOfQualifiedBids)
    test_change_procuringEntity = snitch(change_procuringEntity)
    test_change_lotHolder = snitch(change_lotHolder)
    test_change_bankAccount = snitch(change_bankAccount)
    test_change_contractTerms = snitch(change_contractTerms)
    test_change_one_field_rest_same = snitch(change_one_field_rest_same)

    def setUp(self):
        super(StatusActiveRectificationTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        change_machine_state(procedure, 'active.rectification')
        context = procedure.snapshot()
        auction = context['auction']
        items = context['items']

        entrypoints = {}

        entrypoints['patch_auction'] = '/auctions/{}?acc_token={}'.format(auction['data']['id'],
                                                                          auction['access']['token'])
        entrypoints['post_question'] = '/auctions/{}/questions'.format(auction['data']['id'])
        entrypoints['get_auction'] = '/auctions/{}'.format(auction['data']['id'])
        entrypoints['post_cancellation'] = '/auctions/{}/cancellations?acc_token={}'.format(auction['data']['id'],
                                                                                            auction['access']['token'])
        self.auction = auction
        self.items = items
        self.ENTRYPOINTS = entrypoints


class StatusActiveRectificationQuestionsTest(BaseWebTest):

    test_answer_question = snitch(answer_question)
    test_get_question = snitch(get_question)

    def setUp(self):
        super(StatusActiveRectificationQuestionsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.rectification')
        context = procedure.snapshot(fixture=AUCTION_WITH_QUESTIONS)

        self.auction = context['auction']
        self.question = context['questions'][0]

        entrypoints = {}

        entrypoints['patch_question'] = '/auctions/{}/questions/{}?acc_token={}'.format(self.auction['data']['id'],
                                                                                        self.question['data']['id'],
                                                                                        self.auction['access']['token'])

        entrypoints['get_question'] = '/auctions/{}/questions/{}'.format(self.auction['data']['id'],
                                                                         self.question['data']['id'])
        self.ENTRYPOINTS = entrypoints


class StatusActiveRectificationItemsTest(BaseWebTest):

    test_item_get = snitch(item_get)
    test_item_patch = snitch(item_patch)
    test_items_get_listing = snitch(items_get_listing)
    test_items_patch_collections = snitch(items_patch_collections)
    test_items_patch_collections_blank_items = snitch(items_patch_collections_blank_items)

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


class StatusDraftWithoutItemsTest(BaseWebTest):
    test_item_post = snitch(item_post)

    def setUp(self):
        super(StatusDraftWithoutItemsTest, self).setUp()
        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        change_machine_state(procedure, 'active.rectification')
        context = procedure.snapshot(fixture=AUCTION_WITHOUT_ITEMS)

        auction = context['auction']

        entrypoints = {}

        entrypoints['get_auction'] = '/auctions/{}'.format(auction['data']['id'])
        entrypoints['item_post'] = '/auctions/{}/items?acc_token={}'.format(auction['data']['id'],
                                                                            auction['access']['token'])
        self.auction = auction
        self.ENTRYPOINTS = entrypoints


class StatusActiveRectificationDocumentTest(BaseWebTest):
    docservice = True

    test_add_online_document = snitch(add_document)
    test_add_offline_document = snitch(add_offline_document)
    test_patch_document = snitch(patch_document)
    test_put_document = snitch(put_document)
    test_download_document = snitch(download_document)

    def setUp(self):
        super(StatusActiveRectificationDocumentTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        change_machine_state(procedure, 'active.rectification')
        self.procedure = procedure


class StatusActiveRectificationCancellationsTest(BaseWebTest, CancellationWorkFlowMixin):
    docservice = True

    def setUp(self):
        super(StatusActiveRectificationCancellationsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.rectification')
        context = procedure.snapshot(fixture=AUCTION_WITH_CANCELLATION)

        auction = context['auction']
        cancellation = context['cancellations'][0]

        entrypoints = {}
        entrypoints['get_auction'] = '/auctions/{}'.format(auction['data']['id'])

        entrypoints['patch_cancellation'] = '/auctions/{}/cancellations/{}?acc_token={}'.format(auction['data']['id'],
                                                                                                cancellation['data']['id'],
                                                                                                auction['access']['token'])

        entrypoints['get_cancellation'] = '/auctions/{}/cancellations/{}'.format(auction['data']['id'],
                                                                                 cancellation['data']['id'])

        entrypoints['cancellation_document_post'] = '/auctions/{}/cancellations/{}/documents?acc_token={}'.format(auction['data']['id'],
                                                                                                                  cancellation['data']['id'],
                                                                                                                  auction['access']['token'])
        entrypoints['get_cancellations_listing'] = '/auctions/{}/cancellations'.format(auction['data']['id'])

        self.auction = auction
        self.cancellation = cancellation
        self.cancellations = context['cancellations']
        self.ENTRYPOINTS = entrypoints


class StatusActiveRectificationCancellationsDocumentsTest(BaseWebTest, CancellationDocumentsWorkFlowMixin):
    docservice = True

    def setUp(self):
        super(StatusActiveRectificationCancellationsDocumentsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('draft')
        context = procedure.snapshot(fixture=AUCTION_WITH_CANCELLATION_WITH_DOCUMENTS)

        auction = context['auction']
        cancellation = context['cancellations'][0]
        document = cancellation['data']['documents'][0]
        documents = cancellation['data']['documents']

        entrypoints = {}
        entrypoints['cancellation_document_listing'] = '/auctions/{}/cancellations/{}/documents?acc_token={}'.format(auction['data']['id'],
                                                                                                                     cancellation['data']['id'],
                                                                                                                     auction['access']['token'])

        entrypoints['cancellation_document'] = '/auctions/{}/cancellations/{}/documents/{}?acc_token={}'.format(auction['data']['id'],
                                                                                                                cancellation['data']['id'],
                                                                                                                document['id'],
                                                                                                                auction['access']['token'])

        self.auction = auction
        self.cancellation = cancellation
        self.documents = documents
        self.ENTRYPOINTS = entrypoints


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(StatusActiveRectificationTest))
    suite.addTest(unittest.makeSuite(StatusActiveRectificationDocumentTest))
    suite.addTest(unittest.makeSuite(StatusActiveRectificationQuestionsTest))
    suite.addTest(unittest.makeSuite(StatusActiveRectificationItemsTest))
    suite.addTest(unittest.makeSuite(StatusDraftWithoutItemsTest))
    suite.addTest(unittest.makeSuite(StatusActiveRectificationCancellationsTest))
    suite.addTest(unittest.makeSuite(StatusActiveRectificationCancellationsDocumentsTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
