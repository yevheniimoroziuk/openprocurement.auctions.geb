# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.base import snitch

from openprocurement.auctions.geb.tests.base import (
    BaseWebTest
)

from openprocurement.auctions.geb.tests.states import (
    ProcedureMachine
)

from openprocurement.auctions.geb.tests.fixtures.active_rectification import (
    AUCTION_WITH_QUESTIONS,
    AUCTION_WITH_DOCUMENTS,
    AUCTION_WITHOUT_ITEMS,
    AUCTION_WITH_CANCELLATION,
    AUCTION_WITH_CANCELLATION_WITH_DOCUMENTS
)

from openprocurement.auctions.geb.tests.blanks.cancellations import (
    cancellation_post
)
from openprocurement.auctions.geb.tests.blanks.mixins import (
    BaseAdministratorTestMixin,
    CancellationDocumentsWorkFlowMixin,
    CancellationWorkFlowMixin,
)

from openprocurement.auctions.geb.tests.blanks.active_rectification import (
    auction_document_post,
    auction_document_post_offline,
    auction_document_post_without_ds,
    auction_document_put_without_ds,
    auction_document_patch,
    auction_document_put,
    auction_document_download,
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
)


class ActiveRectificationTest(BaseWebTest):
    docservice = True

    test_add_question = snitch(add_question)
    test_cancellation_post = snitch(cancellation_post)
    test_auction_document_post = snitch(auction_document_post)
    test_auction_document_post_offline = snitch(auction_document_post_offline)
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
        super(ActiveRectificationTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.rectification')
        context = procedure.snapshot()
        auction = context['auction']
        items = context['items']

        entrypoints = {}

        entrypoint_pattern = '/auctions/{}?acc_token={}'
        entrypoints['patch_auction'] = entrypoint_pattern.format(auction['data']['id'], auction['access']['token'])

        entrypoint_pattern = '/auctions/{}/questions'
        entrypoints['post_question'] = entrypoint_pattern.format(auction['data']['id'])

        entrypoints['get_auction'] = '/auctions/{}'.format(auction['data']['id'])

        entrypoint_pattern = '/auctions/{}/cancellations?acc_token={}'
        entrypoints['post_cancellation'] = entrypoint_pattern.format(auction['data']['id'], auction['access']['token'])

        entrypoint_pattern = '/auctions/{}/documents?acc_token={}'
        entrypoints['documents'] = entrypoint_pattern.format(auction['data']['id'], auction['access']['token'])

        self.auction = auction
        self.items = items
        self.ENTRYPOINTS = entrypoints


class ActiveRectificationWithoutDSTest(BaseWebTest):
    docservice = False

    test_auction_document_post_without_ds = snitch(auction_document_post_without_ds)

    def setUp(self):
        super(ActiveRectificationWithoutDSTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.rectification')
        context = procedure.snapshot()
        auction = context['auction']

        entrypoints = {}

        entrypoint_pattern = '/auctions/{}/documents?acc_token={}'
        entrypoints['documents'] = entrypoint_pattern.format(auction['data']['id'], auction['access']['token'])

        self.auction = auction
        self.ENTRYPOINTS = entrypoints


class ActiveRectificationQuestionsTest(BaseWebTest):

    test_answer_question = snitch(answer_question)
    test_get_question = snitch(get_question)

    def setUp(self):
        super(ActiveRectificationQuestionsTest, self).setUp()

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


class ActiveRectificationItemsTest(BaseWebTest):

    test_item_get = snitch(item_get)
    test_item_patch = snitch(item_patch)
    test_items_get_listing = snitch(items_get_listing)
    test_items_patch_collections = snitch(items_patch_collections)
    test_items_patch_collections_blank_items = snitch(items_patch_collections_blank_items)

    def setUp(self):
        super(ActiveRectificationItemsTest, self).setUp()

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


class ActiveRectificationWithoutItemsTest(BaseWebTest):
    test_item_post = snitch(item_post)

    def setUp(self):
        super(ActiveRectificationWithoutItemsTest, self).setUp()
        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.rectification')
        context = procedure.snapshot(fixture=AUCTION_WITHOUT_ITEMS)

        auction = context['auction']

        entrypoints = {}

        entrypoints['get_auction'] = '/auctions/{}'.format(auction['data']['id'])
        entrypoints['item_post'] = '/auctions/{}/items?acc_token={}'.format(auction['data']['id'],
                                                                            auction['access']['token'])
        self.auction = auction
        self.ENTRYPOINTS = entrypoints


class ActiveRectificationDocumentsTest(BaseWebTest):
    docservice = True

    test_auction_document_patch = snitch(auction_document_patch)
    test_auction_document_put = snitch(auction_document_put)
    test_auction_document_download = snitch(auction_document_download)

    def setUp(self):
        super(ActiveRectificationDocumentsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.rectification')
        context = procedure.snapshot(fixture=AUCTION_WITH_DOCUMENTS)

        auction = context['auction']
        document = context['documents'][0]

        entrypoints = {}
        entrypoint_pattern = '/auctions/{}/documents/{}?acc_token={}'
        entrypoints['document_patch'] = entrypoint_pattern.format(auction['data']['id'], document['data']['id'], auction['access']['token'])

        entrypoint_pattern = '/auctions/{}/documents/{}'
        entrypoints['document_get'] = entrypoint_pattern.format(auction['data']['id'], document['data']['id'])

        entrypoints['document_put'] = entrypoints['document_patch']

        self.document = document
        self.auction = auction
        self.ENTRYPOINTS = entrypoints


class ActiveRectificationDocumentsWithoutDSTest(BaseWebTest):
    docservice = False

    test_auction_document_put_without_ds = snitch(auction_document_put_without_ds)

    def setUp(self):
        super(ActiveRectificationDocumentsWithoutDSTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.rectification')
        context = procedure.snapshot(fixture=AUCTION_WITH_DOCUMENTS)

        auction = context['auction']
        document = context['documents'][0]

        entrypoints = {}
        entrypoint_pattern = '/auctions/{}/documents/{}?acc_token={}'
        entrypoints['document_put'] = entrypoint_pattern.format(auction['data']['id'], document['data']['id'], auction['access']['token'])

        entrypoint_pattern = '/auctions/{}/documents/{}'
        entrypoints['document_get'] = entrypoint_pattern.format(auction['data']['id'], document['data']['id'])

        self.document = document
        self.auction = auction
        self.ENTRYPOINTS = entrypoints


class ActiveRectificationCancellationsTest(BaseWebTest, CancellationWorkFlowMixin):
    docservice = True

    def setUp(self):
        super(ActiveRectificationCancellationsTest, self).setUp()

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


class ActiveRectificationCancellationsDocumentsTest(BaseWebTest, CancellationDocumentsWorkFlowMixin):
    docservice = True

    def setUp(self):
        super(ActiveRectificationCancellationsDocumentsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.rectification')
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


class ActiveRectificationAdministratorTest(BaseWebTest, BaseAdministratorTestMixin):

    def setUp(self):
        super(ActiveRectificationAdministratorTest, self).setUp()
        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.rectification')
        context = procedure.snapshot()

        auction = context['auction']

        entrypoints = {}

        entrypoints['get_auction'] = '/auctions/{}'.format(auction['data']['id'])
        entrypoints['patch_auction'] = '/auctions/{}'.format(auction['data']['id'])
        self.auction = auction
        self.ENTRYPOINTS = entrypoints


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ActiveRectificationAdministratorTest))
    suite.addTest(unittest.makeSuite(ActiveRectificationCancellationsDocumentsTest))
    suite.addTest(unittest.makeSuite(ActiveRectificationItemsTest))
    suite.addTest(unittest.makeSuite(ActiveRectificationQuestionsTest))
    suite.addTest(unittest.makeSuite(ActiveRectificationTest))
    suite.addTest(unittest.makeSuite(ActiveRectificationWithoutItemsTest))
    # documents tests
    suite.addTest(unittest.makeSuite(ActiveRectificationDocumentsTest))
    suite.addTest(unittest.makeSuite(ActiveRectificationDocumentsWithoutDSTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
