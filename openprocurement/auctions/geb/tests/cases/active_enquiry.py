
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
    AUCTION_WITH_DOCUMENTS,
    AUCTION_WITH_QUESTIONS,
    AUCTION_WITH_PENDING_BID,
    AUCTION_WITH_ACTIVE_BID,
    AUCTION_WITH_DRAFT_BID_WITH_DOCUMENT,
    AUCTION_WITH_PENDING_BID_WITH_DOCUMENT,
    AUCTION_WITH_ACTIVE_BID_WITH_DOCUMENT,
    AUCTION_WITH_CANCELLATION,
    AUCTION_WITH_CANCELLATION_WITH_DOCUMENTS,
    AUCTION_WITH_BIDS_WITH_CANCELLATION
)

from openprocurement.auctions.geb.tests.blanks.active_enquiry import (
    auction_document_patch,
    auction_document_put,
    auction_document_post,
    auction_document_post_offline,
    add_question,
    add_question_to_item,
    answer_question,
    auction_change_fields,
    get_question,
    bid_add,
    bid_add_document_in_active_status,
    bid_add_document_in_pending_status,
    bid_delete_in_active_status,
    bid_delete_in_pending_status,
    bid_get_in_active_status,
    bid_get_in_pending_status,
    bid_make_activate,
    bid_patch_in_active_status,
    bid_patch_in_pending_status,
    bid_draft_get_document,
    bid_draft_patch_document,
    bid_pending_patch_document,
    bid_pending_get_document,
    bid_active_patch_document,
    bid_active_get_document,
)
from openprocurement.auctions.geb.tests.blanks.cancellations import (
    cancellation_make_clean_bids
)


class StatusActiveEnquiryTest(BaseWebTest):
    docservice = True

    test_bid_add = snitch(bid_add)
    test_add_question = snitch(add_question)
    test_auction_document_post = snitch(auction_document_post)
    test_auction_document_post_offline = snitch(auction_document_post_offline)
    test_add_question_to_item = snitch(add_question_to_item)
    test_auction_change_fields = snitch(auction_change_fields)

    def setUp(self):
        super(StatusActiveEnquiryTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.enquiry')
        context = procedure.snapshot()

        self.auction = context['auction']

        entrypoints = {}
        entrypoints['patch_auction'] = '/auctions/{}?acc_token={}'.format(self.auction['data']['id'],
                                                                          self.auction['access']['token'])
        entrypoints['get_auction'] = '/auctions/{}'.format(self.auction['data']['id'])
        entrypoints['questions'] = '/auctions/{}/questions'.format(self.auction['data']['id'])
        entrypoints['bids'] = '/auctions/{}/bids'.format(self.auction['data']['id'])
        entrypoints['documents'] = '/auctions/{}/documents?acc_token={}'.format(self.auction['data']['id'],
                                                                                self.auction['access']['token'])
        self.ENTRYPOINTS = entrypoints


class StatusActiveEnquiryQuestionsTest(BaseWebTest):

    test_answer_question = snitch(answer_question)
    test_get_question = snitch(get_question)

    def setUp(self):
        super(StatusActiveEnquiryQuestionsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.enquiry')
        context = procedure.snapshot(fixture=AUCTION_WITH_QUESTIONS)

        self.auction = context['auction']
        self.questions = context['questions']


class StatusActiveEnquiryPendingBidsTest(BaseWebTest):
    docservice = True

    test_bid_patch_in_pending_status = snitch(bid_patch_in_pending_status)
    test_bid_make_activate = snitch(bid_make_activate)
    test_bid_add_document_in_pending_status = snitch(bid_add_document_in_pending_status)
    test_bid_delete_in_pending_status = snitch(bid_delete_in_pending_status)
    test_bid_get_in_pending_status = snitch(bid_get_in_pending_status)
    test_bid_patch_in_pending_status = snitch(bid_patch_in_pending_status)

    def setUp(self):
        super(StatusActiveEnquiryPendingBidsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.enquiry')
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


class StatusActiveEnquiryActiveBidsTest(BaseWebTest):
    docservice = True

    test_bid_patch_in_active_status = snitch(bid_patch_in_active_status)
    test_bid_add_document_in_active_status = snitch(bid_add_document_in_active_status)
    test_bid_delete_in_active_status = snitch(bid_delete_in_active_status)
    test_bid_get_in_active_status = snitch(bid_get_in_active_status)
    test_bid_patch_in_active_status = snitch(bid_patch_in_active_status)

    def setUp(self):
        super(StatusActiveEnquiryActiveBidsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.enquiry')
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


class StatusActiveEnquiryDocumentsTest(BaseWebTest):
    docservice = True

    test_auction_document_patch = snitch(auction_document_patch)
    test_auction_document_put = snitch(auction_document_put)

    def setUp(self):
        super(StatusActiveEnquiryDocumentsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.enquiry')
        context = procedure.snapshot(fixture=AUCTION_WITH_DOCUMENTS)

        auction = context['auction']
        document = context['documents'][0]

        entrypoints = {}
        entrypoints['document_patch'] = '/auctions/{}/documents/{}?acc_token={}'.format(auction['data']['id'],
                                                                                        document['data']['id'],
                                                                                        auction['access']['token'])

        entrypoints['document_get'] = '/auctions/{}/documents/{}'.format(auction['data']['id'],
                                                                         document['data']['id'])
        entrypoints['document_put'] = entrypoints['document_patch']

        self.document = document
        self.auction = auction
        self.ENTRYPOINTS = entrypoints


class StatusActiveEnquiryCancellationsTest(BaseWebTest, CancellationWorkFlowMixin):
    docservice = True

    def setUp(self):
        super(StatusActiveEnquiryCancellationsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.enquiry')
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


class StatusActiveEnquiryWithBidsCancellationsTest(BaseWebTest):
    test_cancellation_make_clean_bids = snitch(cancellation_make_clean_bids)

    def setUp(self):
        super(StatusActiveEnquiryWithBidsCancellationsTest, self).setUp()

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


class StatusActiveEnquiryDraftBidsWithDocumentTest(BaseWebTest):

    test_bid_draft_get_document = snitch(bid_draft_get_document)
    test_bid_draft_patch_document = snitch(bid_draft_patch_document)

    def setUp(self):
        super(StatusActiveEnquiryDraftBidsWithDocumentTest, self).setUp()

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


class StatusActiveEnquiryPendingBidsWithDocumentTest(BaseWebTest):

    test_bid_pending_get_document = snitch(bid_pending_get_document)
    test_bid_pending_patch_document = snitch(bid_pending_patch_document)

    def setUp(self):
        super(StatusActiveEnquiryPendingBidsWithDocumentTest, self).setUp()

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


class StatusActiveEnquiryActiveBidsWithDocumentTest(BaseWebTest):

    test_bid_active_get_document = snitch(bid_active_get_document)
    test_bid_active_patch_document = snitch(bid_active_patch_document)

    def setUp(self):
        super(StatusActiveEnquiryActiveBidsWithDocumentTest, self).setUp()

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


class StatusActiveEnquiryCancellationsDocumentsTest(BaseWebTest, CancellationDocumentsWorkFlowMixin):
    docservice = True

    def setUp(self):
        super(StatusActiveEnquiryCancellationsDocumentsTest, self).setUp()

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
    suite.addTest(unittest.makeSuite(StatusActiveEnquiryTest))
    suite.addTest(unittest.makeSuite(StatusActiveEnquiryQuestionsTest))
    suite.addTest(unittest.makeSuite(StatusActiveEnquiryDocumentsTest))
    suite.addTest(unittest.makeSuite(StatusActiveEnquiryPendingBidsTest))
    suite.addTest(unittest.makeSuite(StatusActiveEnquiryActiveBidsTest))
    suite.addTest(unittest.makeSuite(StatusActiveEnquiryDraftBidsWithDocumentTest))
    suite.addTest(unittest.makeSuite(StatusActiveEnquiryPendingBidsWithDocumentTest))
    suite.addTest(unittest.makeSuite(StatusActiveEnquiryActiveBidsWithDocumentTest))
    suite.addTest(unittest.makeSuite(StatusActiveEnquiryCancellationsTest))
    suite.addTest(unittest.makeSuite(StatusActiveEnquiryCancellationsDocumentsTest))
    suite.addTest(unittest.makeSuite(StatusActiveEnquiryWithBidsCancellationsTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
