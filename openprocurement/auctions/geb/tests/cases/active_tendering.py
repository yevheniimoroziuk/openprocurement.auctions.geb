# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.geb.tests.base import (
    BaseWebTest,
)

from openprocurement.auctions.geb.tests.states import (
    ProcedureMachine
)
from openprocurement.auctions.geb.tests.fixtures.active_tendering import (
    ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE_WITH_QUESTION,
    AUCTION_WITH_DRAFT_BID,
    AUCTION_WITH_PENDING_BID,
    AUCTION_WITH_ACTIVE_BID,
    AUCTION_WITH_DRAFT_BID_WITH_DOCUMENT,
    AUCTION_WITH_PENDING_BID_WITH_DOCUMENT,
    AUCTION_WITH_ACTIVE_BID_WITH_DOCUMENT
)

from openprocurement.auctions.geb.tests.blanks.active_tendering import (
    add_document,
    add_invalid_bid,
    add_offline_document,
    add_question,
    answer_question,
    auction_change_fields,
    bid_add,
    bid_add_document_in_active_status,
    bid_add_document_in_draft_status,
    bid_add_document_in_pending_status,
    bid_delete_in_active_status,
    bid_delete_in_draft_status,
    bid_delete_in_pending_status,
    bid_get_in_active_status,
    bid_get_in_draft_status,
    bid_get_in_pending_status,
    bid_make_activate,
    bid_make_pending,
    bid_patch_in_active_status,
    bid_patch_in_draft_status,
    bid_patch_in_pending_status,
    bid_draft_get_document,
    bid_draft_patch_document,
    bid_pending_patch_document,
    bid_pending_get_document,
    bid_active_patch_document,
    bid_active_get_document,
    get_question
)


class StatusActiveTenderingTest(BaseWebTest):

    test_add_question = snitch(add_question)
    test_bid_add = snitch(bid_add)
    test_auction_change_fields = snitch(auction_change_fields)
    test_add_invalid_bid = snitch(add_invalid_bid)

    def setUp(self):
        super(StatusActiveTenderingTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot()

        self.auction = context['auction']

        entrypoints = {}
        entrypoints['patch_auction'] = '/auctions/{}?acc_token={}'.format(self.auction['data']['id'],
                                                                          self.auction['access']['token'])
        entrypoints['get_auction'] = '/auctions/{}'.format(self.auction['data']['id'])
        entrypoints['questions'] = '/auctions/{}/questions'.format(self.auction['data']['id'])
        entrypoints['bids'] = '/auctions/{}/bids'.format(self.auction['data']['id'])

        self.ENTRYPOINTS = entrypoints


class StatusActiveTenderingQuestionsTest(BaseWebTest):

    test_answer_question = snitch(answer_question)
    test_get_question = snitch(get_question)

    def setUp(self):
        super(StatusActiveTenderingQuestionsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE_WITH_QUESTION)

        self.auction = context['auction']
        self.questions = context['questions']


class StatusActiveTenderingDraftBidsTest(BaseWebTest):
    docservice = True

    test_bid_patch_in_draft_status = snitch(bid_patch_in_draft_status)
    test_bid_make_pending = snitch(bid_make_pending)
    test_bid_add_document_in_draft_status = snitch(bid_add_document_in_draft_status)
    test_bid_delete_in_draft_status = snitch(bid_delete_in_draft_status)
    test_bid_get_in_draft_status = snitch(bid_get_in_draft_status)
    test_bid_patch_in_draft_status = snitch(bid_patch_in_draft_status)

    def setUp(self):
        super(StatusActiveTenderingDraftBidsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=AUCTION_WITH_DRAFT_BID)

        auction = context['auction']
        bid = context['bids'][0]

        entrypoints = {}

        pattern = '/auctions/{auction}/bids/{bid}?acc_token={token}'
        entrypoints['bid'] = pattern.format(auction=auction['data']['id'],
                                            bid=bid['data']['id'],
                                            token=bid['access']['token'])

        pattern = '/auctions/{auction}/bids/{bid}/documents?acc_token={token}'
        entrypoints['add_bid_document'] = pattern.format(auction=auction['data']['id'],
                                                         bid=bid['data']['id'],
                                                         token=bid['access']['token'])
        self.ENTRYPOINTS = entrypoints
        self.bid = bid
        self.auction = auction


class StatusActiveTenderingPendingBidsTest(BaseWebTest):
    docservice = True

    test_bid_patch_in_pending_status = snitch(bid_patch_in_pending_status)
    test_bid_make_activate = snitch(bid_make_activate)
    test_bid_add_document_in_pending_status = snitch(bid_add_document_in_pending_status)
    test_bid_delete_in_pending_status = snitch(bid_delete_in_pending_status)
    test_bid_get_in_pending_status = snitch(bid_get_in_pending_status)
    test_bid_patch_in_pending_status = snitch(bid_patch_in_pending_status)

    def setUp(self):
        super(StatusActiveTenderingPendingBidsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=AUCTION_WITH_PENDING_BID)

        auction = context['auction']
        bid = context['bids'][0]

        entrypoints = {}

        pattern = '/auctions/{auction}/bids/{bid}?acc_token={token}'
        entrypoints['bid'] = pattern.format(auction=auction['data']['id'],
                                            bid=bid['data']['id'],
                                            token=bid['access']['token'])

        pattern = '/auctions/{auction}/bids/{bid}/documents?acc_token={token}'
        entrypoints['add_bid_document'] = pattern.format(auction=auction['data']['id'],
                                                         bid=bid['data']['id'],
                                                         token=bid['access']['token'])
        self.ENTRYPOINTS = entrypoints
        self.bid = bid
        self.auction = auction


class StatusActiveTenderingActiveBidsTest(BaseWebTest):
    docservice = True

    test_bid_patch_in_active_status = snitch(bid_patch_in_active_status)
    test_bid_add_document_in_active_status = snitch(bid_add_document_in_active_status)
    test_bid_delete_in_active_status = snitch(bid_delete_in_active_status)
    test_bid_get_in_active_status = snitch(bid_get_in_active_status)
    test_bid_patch_in_active_status = snitch(bid_patch_in_active_status)

    def setUp(self):
        super(StatusActiveTenderingActiveBidsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=AUCTION_WITH_ACTIVE_BID)

        auction = context['auction']
        bid = context['bids'][0]

        entrypoints = {}

        pattern = '/auctions/{auction}/bids/{bid}?acc_token={token}'
        entrypoints['bid'] = pattern.format(auction=auction['data']['id'],
                                            bid=bid['data']['id'],
                                            token=bid['access']['token'])

        pattern = '/auctions/{auction}/bids/{bid}/documents?acc_token={token}'
        entrypoints['add_bid_document'] = pattern.format(auction=auction['data']['id'],
                                                         bid=bid['data']['id'],
                                                         token=bid['access']['token'])
        self.ENTRYPOINTS = entrypoints
        self.bid = bid
        self.auction = auction


class StatusActiveTenderingDraftBidsWithDocumentTest(BaseWebTest):

    test_bid_get_document_in_active_status = snitch(bid_draft_get_document)
    test_bid_patch_document_in_active_status = snitch(bid_draft_patch_document)

    def setUp(self):
        super(StatusActiveTenderingDraftBidsWithDocumentTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=AUCTION_WITH_DRAFT_BID_WITH_DOCUMENT)
        auction = context['auction']
        bid = context['bids'][0]
        bid_document = bid['data']['documents'][0]
        entrypoints = {}
        pattern = '/auctions/{}/bids/{}/documents/{}?acc_token={}'
        entrypoints['bid_document'] = pattern.format(auction['data']['id'],
                                                     bid['data']['id'],
                                                     bid_document['data']['id'],
                                                     bid['access']['token'])

        self.ENTRYPOINTS = entrypoints
        self.bid = bid
        self.auction = auction


class StatusActiveTenderingPendingBidsWithDocumentTest(BaseWebTest):

    test_bid_get_document_in_active_status = snitch(bid_pending_get_document)
    test_bid_patch_document_in_active_status = snitch(bid_pending_patch_document)

    def setUp(self):
        super(StatusActiveTenderingPendingBidsWithDocumentTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=AUCTION_WITH_PENDING_BID_WITH_DOCUMENT)
        auction = context['auction']
        bid = context['bids'][0]
        bid_document = bid['data']['documents'][0]
        entrypoints = {}
        pattern = '/auctions/{}/bids/{}/documents/{}?acc_token={}'
        entrypoints['bid_document'] = pattern.format(auction['data']['id'],
                                                     bid['data']['id'],
                                                     bid_document['data']['id'],
                                                     bid['access']['token'])

        self.ENTRYPOINTS = entrypoints
        self.bid = bid
        self.auction = auction


class StatusActiveTenderingActiveBidsWithDocumentTest(BaseWebTest):

    test_bid_get_document_in_active_status = snitch(bid_active_get_document)
    test_bid_patch_document_in_active_status = snitch(bid_active_patch_document)

    def setUp(self):
        super(StatusActiveTenderingActiveBidsWithDocumentTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=AUCTION_WITH_ACTIVE_BID_WITH_DOCUMENT)
        auction = context['auction']
        bid = context['bids'][0]
        bid_document = bid['data']['documents'][0]
        entrypoints = {}
        pattern = '/auctions/{}/bids/{}/documents/{}?acc_token={}'
        entrypoints['bid_document'] = pattern.format(auction['data']['id'],
                                                     bid['data']['id'],
                                                     bid_document['data']['id'],
                                                     bid['access']['token'])

        self.ENTRYPOINTS = entrypoints
        self.bid = bid
        self.auction = auction


class StatusActiveTenderingDocumentsTest(BaseWebTest):
    docservice = True

    test_add_offline_document = snitch(add_offline_document)
    test_add_document = snitch(add_document)

    def setUp(self):
        super(StatusActiveTenderingDocumentsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot()

        self.auction = context['auction']

        entrypoints = {}
        entrypoints['documents'] = '/auctions/{}/documents?acc_token={}'.format(self.auction['data']['id'],
                                                                                self.auction['access']['token'])

        self.ENTRYPOINTS = entrypoints


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(StatusActiveTenderingTest))
    suite.addTest(unittest.makeSuite(StatusActiveTenderingQuestionsTest))
    suite.addTest(unittest.makeSuite(StatusActiveTenderingDraftBidsTest))
    suite.addTest(unittest.makeSuite(StatusActiveTenderingPendingBidsTest))
    suite.addTest(unittest.makeSuite(StatusActiveTenderingActiveBidsTest))
    suite.addTest(unittest.makeSuite(StatusActiveTenderingDraftBidsWithDocumentTest))
    suite.addTest(unittest.makeSuite(StatusActiveTenderingPendingBidsWithDocumentTest))
    suite.addTest(unittest.makeSuite(StatusActiveTenderingActiveBidsWithDocumentTest))
    suite.addTest(unittest.makeSuite(StatusActiveTenderingDocumentsTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
