# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.geb.tests.base import (
    BaseWebTest,
)
from openprocurement.auctions.geb.tests.blanks.draft import (
    auction_patch_items,
    check_generated_enquiry_period,
    check_generated_rectification_period,
    check_generated_tender_period,
    invalid_phase_commit,
    item_post,
    item_post_collections,
    phase_commit,
    phase_commit_invalid_auctionPeriod,
    phase_commit_without_items
)
from openprocurement.auctions.geb.tests.blanks.cancellations import (
    cancellation_post
)
from openprocurement.auctions.geb.tests.blanks.mixins import (
    CancellationWorkFlowMixin,
    CancellationDocumentsWorkFlowMixin
)
from openprocurement.auctions.geb.tests.helpers import (
    change_machine_state
)
from openprocurement.auctions.geb.tests.states import (
    ProcedureMachine
)

from openprocurement.auctions.geb.tests.fixtures.draft import (
    AUCTION_WITHOUT_ITEMS,
    AUCTION_WITH_INVALID_AUCTON_PERIOD,
    AUCTION_WITH_CANCELLATION,
    AUCTION_WITH_CANCELLATION_WITH_DOCUMENTS
)


class StatusDraftTest(BaseWebTest):

    test_phase_commit = snitch(phase_commit)
    test_cancellation_post = snitch(cancellation_post)
    test_check_generated_rectification_period = snitch(check_generated_rectification_period)
    test_check_generated_tender_period = snitch(check_generated_tender_period)
    test_check_generated_enquiry_period = snitch(check_generated_enquiry_period)
    test_auction_patch_items = snitch(auction_patch_items)
    test_invalid_phase_commit = snitch(invalid_phase_commit)

    def setUp(self):
        super(StatusDraftTest, self).setUp()
        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        change_machine_state(procedure, 'draft')
        context = procedure.snapshot()

        auction = context['auction']

        entrypoints = {}

        entrypoints['get_auction'] = '/auctions/{}'.format(auction['data']['id'])
        entrypoints['patch_auction'] = '/auctions/{}?acc_token={}'.format(auction['data']['id'],
                                                                          auction['access']['token'])
        entrypoints['post_cancellation'] = '/auctions/{}/cancellations?acc_token={}'.format(auction['data']['id'],
                                                                                            auction['access']['token'])
        self.auction = auction
        self.ENTRYPOINTS = entrypoints


class StatusDraftWithoutItemsTest(BaseWebTest):
    test_item_post = snitch(item_post)
    test_item_post_collections = snitch(item_post_collections)
    test_phase_commit_without_items = snitch(phase_commit_without_items)

    def setUp(self):
        super(StatusDraftWithoutItemsTest, self).setUp()
        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        change_machine_state(procedure, 'draft')
        context = procedure.snapshot(fixture=AUCTION_WITHOUT_ITEMS)

        auction = context['auction']

        entrypoints = {}

        entrypoints['get_auction'] = '/auctions/{}'.format(auction['data']['id'])
        entrypoints['item_post'] = '/auctions/{}/items?acc_token={}'.format(auction['data']['id'],
                                                                            auction['access']['token'])

        entrypoints['patch_auction'] = '/auctions/{}?acc_token={}'.format(auction['data']['id'],
                                                                          auction['access']['token'])
        self.auction = auction
        self.ENTRYPOINTS = entrypoints


class StatusDraftInvalidAuctionPeriodTest(BaseWebTest):

    test_phase_commit_invalid_auctionPeriod = snitch(phase_commit_invalid_auctionPeriod)

    def setUp(self):
        super(StatusDraftInvalidAuctionPeriodTest, self).setUp()
        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        change_machine_state(procedure, 'draft')
        context = procedure.snapshot(fixture=AUCTION_WITH_INVALID_AUCTON_PERIOD)

        auction = context['auction']

        entrypoints = {}

        entrypoints['patch_auction'] = '/auctions/{}?acc_token={}'.format(auction['data']['id'],
                                                                          auction['access']['token'])
        self.auction = auction
        self.ENTRYPOINTS = entrypoints


class StatusDraftCancellationsTest(BaseWebTest, CancellationWorkFlowMixin):
    docservice = True

    def setUp(self):
        super(StatusDraftCancellationsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('draft')
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
        entrypoints['cancellation_document_listing'] = '/auctions/{}/cancellations/{}/documents?acc_token={}'.format(auction['data']['id'],
                                                                                                                     cancellation['data']['id'],
                                                                                                                     auction['access']['token'])

        entrypoints['get_cancellations_listing'] = '/auctions/{}/cancellations'.format(auction['data']['id'])

        self.auction = auction
        self.cancellation = cancellation
        self.cancellations = context['cancellations']
        self.ENTRYPOINTS = entrypoints


class StatusDraftCancellationsDocumentsTest(BaseWebTest, CancellationDocumentsWorkFlowMixin):
    docservice = True

    def setUp(self):
        super(StatusDraftCancellationsDocumentsTest, self).setUp()

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
    suite.addTest(unittest.makeSuite(StatusDraftTest))
    suite.addTest(unittest.makeSuite(StatusDraftInvalidAuctionPeriodTest))
    suite.addTest(unittest.makeSuite(StatusDraftCancellationsTest))
    suite.addTest(unittest.makeSuite(StatusDraftCancellationsDocumentsTest))
    suite.addTest(unittest.makeSuite(StatusDraftWithoutItemsTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
