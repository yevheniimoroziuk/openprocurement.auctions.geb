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
    auction_item_patch,
    bid_patch,
    auction_question_patch,
    get_auction_auction,
    get_participation_urls,
    post_auction_document_audit,
    post_result_invalid_number_of_bids,
    switch_to_qualification,
    switch_to_qualification_outstanding,
    switch_to_unsuccessful,
    update_auction_urls
)
from openprocurement.auctions.geb.tests.blanks.cancellations import (
    cancellation_make_clean_bids
)


class StatusActiveAuctionTest(BaseWebTest):
    docservice = True

    test_get_auction_auction = snitch(get_auction_auction)
    test_bid_patch = snitch(bid_patch)
    test_auction_question_patch = snitch(auction_question_patch)
    test_auction_item_patch = snitch(auction_item_patch)
    test_auction_document_patch = snitch(auction_document_patch)
    test_update_auction_urls = snitch(update_auction_urls)
    test_switch_to_qualification = snitch(switch_to_qualification)
    test_post_result_invalid_number_of_bids = snitch(post_result_invalid_number_of_bids)
    test_switch_to_qualification_outstanding = snitch(switch_to_qualification_outstanding)
    test_post_auction_document_audit = snitch(post_auction_document_audit)
    test_switch_to_unsuccessful = snitch(switch_to_unsuccessful)
    test_get_participation_urls = snitch(get_participation_urls)

    def setUp(self):
        super(StatusActiveAuctionTest, self).setUp()
        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.auction')
        self.procedure = procedure

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
    suite.addTest(unittest.makeSuite(StatusActiveAuctionTest))
    suite.addTest(unittest.makeSuite(StatusActiveAuctionCancellationsTest))
    suite.addTest(unittest.makeSuite(StatusActiveAuctionWithBidsCancellationsTest))
    suite.addTest(unittest.makeSuite(StatusActiveAuctionCancellationsDocumentsTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
