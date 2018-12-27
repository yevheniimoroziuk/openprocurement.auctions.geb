# -*- coding: utf-8 -*-
import unittest
from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.geb.tests.base import (
    BaseWebTest
)
from openprocurement.auctions.geb.tests.states import (
    ProcedureMachine
)
from openprocurement.auctions.geb.tests.blanks.mixins import (
    CancellationWorkFlowMixin,
    CancellationDocumentsWorkFlowMixin
)
from openprocurement.auctions.geb.tests.fixtures.active_enquiry import (
    AUCTION_WITH_CANCELLATION,
    AUCTION_WITH_CANCELLATION_WITH_DOCUMENTS,
    AUCTION_WITH_BIDS_WITH_CANCELLATION
)
from openprocurement.auctions.geb.tests.blanks.active_auction import (
    auction_document_patch,
    auction_document_post,
    auction_item_patch,
    auction_question_patch,
    auction_question_post,
    bid_delete,
    bid_document_post,
    bid_get,
    bid_get_participation_urls,
    bid_patch,
    module_auction_get_auction_auction,
    module_auction_post_audit,
    module_auction_post_audit_without_ds,
    module_auction_post_result_invalid_number_of_bids,
    module_auction_switch_to_qualification,
    module_auction_switch_to_qualification_outstanding,
    module_auction_switch_to_unsuccessful,
    module_auction_update_auction_urls
)
from openprocurement.auctions.geb.tests.blanks.cancellations import (
    cancellation_make_clean_bids
)


class StatusActiveAuctionTest(BaseWebTest):
    docservice = True

    test_auction_document_patch = snitch(auction_document_patch)
    test_auction_question_post = snitch(auction_question_post)
    test_auction_document_post = snitch(auction_document_post)
    test_auction_item_patch = snitch(auction_item_patch)
    test_auction_question_patch = snitch(auction_question_patch)
    test_bid_delete = snitch(bid_delete)
    test_bid_get_participation_urls = snitch(bid_get_participation_urls)
    test_bid_get = snitch(bid_get)
    test_bid_document_post = snitch(bid_document_post)
    test_bid_patch = snitch(bid_patch)

    def setUp(self):
        super(StatusActiveAuctionTest, self).setUp()
        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.auction')
        self.procedure = procedure


class StatusActiveAuctionModuleAuctionTest(BaseWebTest):
    docservice = True

    test_module_auction_get_auction_auction = snitch(module_auction_get_auction_auction)
    test_module_auction_post_audit = snitch(module_auction_post_audit)
    test_module_auction_post_result_invalid_number_of_bids = snitch(module_auction_post_result_invalid_number_of_bids)
    test_module_auction_switch_to_qualification = snitch(module_auction_switch_to_qualification)
    test_module_auction_switch_to_qualification_outstanding = snitch(module_auction_switch_to_qualification_outstanding)
    test_module_auction_switch_to_unsuccessful = snitch(module_auction_switch_to_unsuccessful)
    test_module_auction_update_auction_urls = snitch(module_auction_update_auction_urls)

    def setUp(self):
        super(StatusActiveAuctionModuleAuctionTest, self).setUp()
        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.auction')
        self.procedure = procedure

        self.app.authorization = ('Basic', ('auction', ''))


class StatusActiveAuctionModuleAuctionWithoutDSTest(BaseWebTest):
    docservice = False

    test_module_auction_post_audit_without_ds = snitch(module_auction_post_audit_without_ds)

    def setUp(self):
        super(StatusActiveAuctionModuleAuctionWithoutDSTest, self).setUp()
        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.auction')
        self.procedure = procedure

        context = procedure.snapshot()

        self.auction = context['auction']

        entrypoints = {}

        entrypoint_pattern = '/auctions/{}/documents?acc_token={}'
        entrypoints['documents'] = entrypoint_pattern.format(self.auction['data']['id'], self.auction['access']['token'])

        self.ENTRYPOINTS = entrypoints
        self.app.authorization = ('Basic', ('auction', ''))


class StatusActiveAuctionCancellationsTest(BaseWebTest, CancellationWorkFlowMixin):
    docservice = True

    def setUp(self):
        super(StatusActiveAuctionCancellationsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.auction')
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


class StatusActiveAuctionWithBidsCancellationsTest(BaseWebTest):
    test_cancellation_make_clean_bids = snitch(cancellation_make_clean_bids)

    def setUp(self):
        super(StatusActiveAuctionWithBidsCancellationsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=AUCTION_WITH_BIDS_WITH_CANCELLATION)

        auction = context['auction']
        bids = context['bids']
        cancellation = context['cancellations'][0]

        entrypoints = {}
        entrypoints['get_auction'] = '/auctions/{}'.format(auction['data']['id'])
        entrypoints['patch_cancellation'] = '/auctions/{}/cancellations/{}?acc_token={}'.format(auction['data']['id'],
                                                                                                cancellation['data']['id'],
                                                                                                auction['access']['token'])

        self.auction = auction
        self.bids = bids
        self.cancellation = cancellation
        self.cancellations = context['cancellations']
        self.ENTRYPOINTS = entrypoints


class StatusActiveAuctionCancellationsDocumentsTest(BaseWebTest, CancellationDocumentsWorkFlowMixin):
    docservice = True

    def setUp(self):
        super(StatusActiveAuctionCancellationsDocumentsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.auction')
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
    suite.addTest(unittest.makeSuite(StatusActiveAuctionTest))
    suite.addTest(unittest.makeSuite(StatusActiveAuctionModuleAuctionTest))
    suite.addTest(unittest.makeSuite(StatusActiveAuctionModuleAuctionWithoutDSTest))
    suite.addTest(unittest.makeSuite(StatusActiveAuctionCancellationsTest))
    suite.addTest(unittest.makeSuite(StatusActiveAuctionWithBidsCancellationsTest))
    suite.addTest(unittest.makeSuite(StatusActiveAuctionCancellationsDocumentsTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
