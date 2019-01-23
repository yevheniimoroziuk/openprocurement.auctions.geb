# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.geb.tests.base import (
    BaseWebTest,
)

from openprocurement.auctions.geb.tests.states import (
    ProcedureMachine
)
from openprocurement.auctions.geb.tests.blanks.mixins import (
    CancellationWorkFlowMixin,
    CancellationWorkFlowWithoutDSMixin,
    CancellationDocumentsWorkFlowMixin,
    CancellationDocumentsWorkFlowWithoutDSMixin,
    BaseAdministratorTestMixin
)
from openprocurement.auctions.geb.tests.fixtures.active_tendering import (
    AUCTION_WITH_BIDS_WITH_CANCELLATION,
    AUCTION_WITH_BID_ACTIVE,
    AUCTION_WITH_BID_ACTIVE_WITH_DOCUMENT,
    AUCTION_WITH_BID_DRAFT,
    AUCTION_WITH_BID_DRAFT_WITH_DOCUMENT,
    AUCTION_WITH_BID_PENDING,
    AUCTION_WITH_BID_PENDING_WITH_DOCUMENT,
    AUCTION_WITH_CANCELLATION,
    AUCTION_WITH_CANCELLATION_WITH_DOCUMENTS,
    AUCTION_WITH_DOCUMENTS,
    AUCTION_WITH_OFFLINE_DOCUMENTS,
    AUCTION_WITH_QUESTIONS
)

from openprocurement.auctions.geb.tests.blanks.active_tendering import (
    auction_auction_get,
    auction_bid_post,
    auction_bid_post_invalid,
    auction_document_download,
    auction_document_patch,
    auction_document_post,
    auction_document_post_offline,
    auction_document_post_without_ds,
    auction_document_put,
    auction_document_put_offline,
    auction_document_put_without_ds,
    auction_patch,
    auction_question_post,
    bid_active_get_document,
    bid_active_patch_document,
    bid_delete_in_active_status,
    bid_delete_in_draft_status,
    bid_delete_in_pending_status,
    bid_document_post,
    bid_document_post_without_ds,
    bid_document_put_without_ds,
    bid_draft_get_document,
    bid_draft_patch_document,
    bid_get_in_active_status,
    bid_get_in_draft_status,
    bid_get_in_pending_status,
    bid_make_activate,
    bid_make_pending,
    bid_make_pending_include_all_data,
    bid_patch_bid_number_invalid,
    bid_patch_in_active_status,
    bid_patch_in_draft_status,
    bid_patch_in_pending_status,
    bid_pending_get_document,
    bid_pending_patch_document,
    item_question_post,
    question_get,
    question_patch
)
from openprocurement.auctions.geb.tests.blanks.cancellations import (
    cancellation_make_clean_bids
)


class ActiveTenderingTest(BaseWebTest):
    docservice = True

    test_auction_document_post_offline = snitch(auction_document_post_offline)
    test_auction_document_post = snitch(auction_document_post)
    test_auction_question_post = snitch(auction_question_post)
    test_item_question_post = snitch(item_question_post)
    test_auction_bid_post = snitch(auction_bid_post)
    test_auction_auction_get = snitch(auction_auction_get)
    test_auction_change_fields = snitch(auction_patch)
    test_auction_bid_post_invalid = snitch(auction_bid_post_invalid)

    def setUp(self):
        super(ActiveTenderingTest, self).setUp()

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
        entrypoints['documents'] = '/auctions/{}/documents?acc_token={}'.format(self.auction['data']['id'],
                                                                                self.auction['access']['token'])

        self.ENTRYPOINTS = entrypoints


class ActiveTenderingWithoutDSTest(BaseWebTest):
    docservice = False

    test_auction_document_post_without_ds = snitch(auction_document_post_without_ds)

    def setUp(self):
        super(ActiveTenderingWithoutDSTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot()

        self.auction = context['auction']

        entrypoints = {}

        entrypoint_pattern = '/auctions/{}/documents?acc_token={}'
        entrypoints['documents'] = entrypoint_pattern.format(self.auction['data']['id'], self.auction['access']['token'])

        self.ENTRYPOINTS = entrypoints


class ActiveTenderingDocumentWithoutDSTest(BaseWebTest):
    docservice = False

    test_auction_document_put_without_ds = snitch(auction_document_put_without_ds)

    def setUp(self):
        super(ActiveTenderingDocumentWithoutDSTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
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


class ActiveTenderingQuestionsTest(BaseWebTest):

    test_question_patch = snitch(question_patch)
    test_question_get = snitch(question_get)

    def setUp(self):
        super(ActiveTenderingQuestionsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
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


class ActiveTenderingBidsDraftTest(BaseWebTest):
    docservice = True

    test_bid_patch_in_draft_status = snitch(bid_patch_in_draft_status)
    test_bid_make_pending = snitch(bid_make_pending)
    test_bid_make_pending_include_all_data = snitch(bid_make_pending_include_all_data)
    test_bid_document_post = snitch(bid_document_post)
    test_bid_delete_in_draft_status = snitch(bid_delete_in_draft_status)
    test_bid_get_in_draft_status = snitch(bid_get_in_draft_status)
    test_bid_patch_in_draft_status = snitch(bid_patch_in_draft_status)

    def setUp(self):
        super(ActiveTenderingBidsDraftTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=AUCTION_WITH_BID_DRAFT)

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


class ActiveTenderingBidsPendingTest(BaseWebTest):
    docservice = True

    test_bid_patch_in_pending_status = snitch(bid_patch_in_pending_status)
    test_bid_patch_bidNumber_invalid = snitch(bid_patch_bid_number_invalid)
    test_bid_make_activate = snitch(bid_make_activate)
    test_bid_document_post = snitch(bid_document_post)
    test_bid_delete_in_pending_status = snitch(bid_delete_in_pending_status)
    test_bid_get_in_pending_status = snitch(bid_get_in_pending_status)
    test_bid_patch_in_pending_status = snitch(bid_patch_in_pending_status)

    def setUp(self):
        super(ActiveTenderingBidsPendingTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=AUCTION_WITH_BID_PENDING)

        auction = context['auction']
        bid = context['bids'][0]

        entrypoints = {}

        pattern = '/auctions/{auction}/bids/{bid}?acc_token={token}'
        entrypoints['bid'] = pattern.format(auction=auction['data']['id'],
                                            bid=bid['data']['id'],
                                            token=bid['access']['token'])

        pattern = '/auctions/{auction}/bids'
        entrypoints['bid_post'] = pattern.format(auction=auction['data']['id'])

        pattern = '/auctions/{auction}/bids/{bid}/documents?acc_token={token}'
        entrypoints['add_bid_document'] = pattern.format(auction=auction['data']['id'],
                                                         bid=bid['data']['id'],
                                                         token=bid['access']['token'])
        self.ENTRYPOINTS = entrypoints
        self.bid = bid
        self.auction = auction


class ActiveTenderingBidsActiveTest(BaseWebTest):
    docservice = True

    test_bid_patch_in_active_status = snitch(bid_patch_in_active_status)
    test_bid_document_post = snitch(bid_document_post)
    test_bid_delete_in_active_status = snitch(bid_delete_in_active_status)
    test_bid_get_in_active_status = snitch(bid_get_in_active_status)
    test_bid_patch_in_active_status = snitch(bid_patch_in_active_status)

    def setUp(self):
        super(ActiveTenderingBidsActiveTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=AUCTION_WITH_BID_ACTIVE)

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


class ActiveTenderingBidsDraftWithoutDSTest(BaseWebTest):
    docservice = False

    test_bid_document_post_without_ds = snitch(bid_document_post_without_ds)

    def setUp(self):
        super(ActiveTenderingBidsDraftWithoutDSTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=AUCTION_WITH_BID_DRAFT)

        auction = context['auction']
        bid = context['bids'][0]

        entrypoints = {}

        pattern = '/auctions/{auction}/bids/{bid}/documents?acc_token={token}'
        entrypoints['add_bid_document'] = pattern.format(auction=auction['data']['id'],
                                                         bid=bid['data']['id'],
                                                         token=bid['access']['token'])
        self.ENTRYPOINTS = entrypoints
        self.bid = bid
        self.auction = auction


class ActiveTenderingBidsPendingWithoutDSTest(BaseWebTest):
    docservice = False

    test_bid_document_post_without_ds = snitch(bid_document_post_without_ds)

    def setUp(self):
        super(ActiveTenderingBidsPendingWithoutDSTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=AUCTION_WITH_BID_PENDING)

        auction = context['auction']
        bid = context['bids'][0]

        entrypoints = {}

        pattern = '/auctions/{auction}/bids/{bid}/documents?acc_token={token}'
        entrypoints['add_bid_document'] = pattern.format(auction=auction['data']['id'],
                                                         bid=bid['data']['id'],
                                                         token=bid['access']['token'])
        self.ENTRYPOINTS = entrypoints
        self.bid = bid
        self.auction = auction


class ActiveTenderingBidsActiveWithoutDSTest(BaseWebTest):
    docservice = False

    test_bid_document_post_without_ds = snitch(bid_document_post_without_ds)

    def setUp(self):
        super(ActiveTenderingBidsActiveWithoutDSTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=AUCTION_WITH_BID_ACTIVE)

        auction = context['auction']
        bid = context['bids'][0]

        entrypoints = {}

        pattern = '/auctions/{auction}/bids/{bid}/documents?acc_token={token}'
        entrypoints['add_bid_document'] = pattern.format(auction=auction['data']['id'],
                                                         bid=bid['data']['id'],
                                                         token=bid['access']['token'])
        self.ENTRYPOINTS = entrypoints
        self.bid = bid
        self.auction = auction


class ActiveTenderingBidsDraftWithDocumentTest(BaseWebTest):
    docservice = True

    test_bid_get_document_in_active_status = snitch(bid_draft_get_document)
    test_bid_patch_document_in_active_status = snitch(bid_draft_patch_document)
    test_bid_document_put_without_ds = snitch(bid_document_put_without_ds)

    def setUp(self):
        super(ActiveTenderingBidsDraftWithDocumentTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=AUCTION_WITH_BID_DRAFT_WITH_DOCUMENT)
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


class ActiveTenderingBidsDraftWithDocumentWithoutDSTest(BaseWebTest):
    docservice = False

    test_bid_document_put_without_ds = snitch(bid_document_put_without_ds)

    def setUp(self):
        super(ActiveTenderingBidsDraftWithDocumentWithoutDSTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=AUCTION_WITH_BID_DRAFT_WITH_DOCUMENT)
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


class ActiveTenderingBidsPendingWithDocumentTest(BaseWebTest):

    test_bid_get_document_in_active_status = snitch(bid_pending_get_document)
    test_bid_patch_document_in_active_status = snitch(bid_pending_patch_document)
    test_bid_document_put_without_ds = snitch(bid_document_put_without_ds)

    def setUp(self):
        super(ActiveTenderingBidsPendingWithDocumentTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=AUCTION_WITH_BID_PENDING_WITH_DOCUMENT)
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


class ActiveTenderingBidsPendingWithDocumentWithoutDSTest(BaseWebTest):
    docservice = False

    test_bid_document_put_without_ds = snitch(bid_document_put_without_ds)

    def setUp(self):
        super(ActiveTenderingBidsPendingWithDocumentWithoutDSTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=AUCTION_WITH_BID_PENDING_WITH_DOCUMENT)
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


class ActiveTenderingBidsActiveWithDocumentTest(BaseWebTest):

    test_bid_get_document_in_active_status = snitch(bid_active_get_document)
    test_bid_patch_document_in_active_status = snitch(bid_active_patch_document)

    def setUp(self):
        super(ActiveTenderingBidsActiveWithDocumentTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=AUCTION_WITH_BID_ACTIVE_WITH_DOCUMENT)
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


class ActiveTenderingBidsActiveWithDocumentWithoutDSTest(BaseWebTest):

    docservice = False

    test_bid_document_put_without_ds = snitch(bid_document_put_without_ds)

    def setUp(self):
        super(ActiveTenderingBidsActiveWithDocumentWithoutDSTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=AUCTION_WITH_BID_ACTIVE_WITH_DOCUMENT)
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


class ActiveTenderingDocumentsTest(BaseWebTest):
    docservice = True

    test_auction_document_patch = snitch(auction_document_patch)
    test_auction_document_put = snitch(auction_document_put)
    test_auction_document_download = snitch(auction_document_download)

    def setUp(self):
        super(ActiveTenderingDocumentsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
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


class ActiveTenderingOfflineDocumentsTest(BaseWebTest):
    docservice = True

    test_auction_document_put_offline = snitch(auction_document_put_offline)

    def setUp(self):
        super(ActiveTenderingOfflineDocumentsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=AUCTION_WITH_OFFLINE_DOCUMENTS)

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


class ActiveTenderingCancellationsTest(BaseWebTest, CancellationWorkFlowMixin):
    docservice = True

    def setUp(self):
        super(ActiveTenderingCancellationsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
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


class ActiveTenderingCancellationsWithoutDSTest(BaseWebTest, CancellationWorkFlowWithoutDSMixin):

    def setUp(self):
        super(ActiveTenderingCancellationsWithoutDSTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=AUCTION_WITH_CANCELLATION)

        auction = context['auction']
        cancellation = context['cancellations'][0]

        entrypoints = {}
        entrypoint_pattern = '/auctions/{}/cancellations/{}/documents?acc_token={}'
        entrypoints['cancellation_document_post'] = entrypoint_pattern.format(auction['data']['id'],
                                                                              cancellation['data']['id'],
                                                                              auction['access']['token'])

        self.auction = auction
        self.cancellation = cancellation
        self.ENTRYPOINTS = entrypoints


class ActiveTenderingCancellationsWithBidsTest(BaseWebTest):
    test_cancellation_make_active_clean_bids = snitch(cancellation_make_clean_bids)

    def setUp(self):
        super(ActiveTenderingCancellationsWithBidsTest, self).setUp()

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


class ActiveTenderingCancellationsDocumentsTest(BaseWebTest, CancellationDocumentsWorkFlowMixin):
    docservice = True

    def setUp(self):
        super(ActiveTenderingCancellationsDocumentsTest, self).setUp()

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


class ActiveTenderingCancellationsDocumentsWithoutDSTest(BaseWebTest, CancellationDocumentsWorkFlowWithoutDSMixin):

    def setUp(self):
        super(ActiveTenderingCancellationsDocumentsWithoutDSTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=AUCTION_WITH_CANCELLATION_WITH_DOCUMENTS)

        auction = context['auction']
        cancellation = context['cancellations'][0]
        document = cancellation['data']['documents'][0]

        entrypoints = {}
        entrypoint_pattern = '/auctions/{}/cancellations/{}/documents/{}?acc_token={}'
        entrypoints['cancellation_document'] = entrypoint_pattern.format(auction['data']['id'],
                                                                         cancellation['data']['id'],
                                                                         document['id'],
                                                                         auction['access']['token'])

        self.auction = auction
        self.document = document
        self.ENTRYPOINTS = entrypoints


class ActiveTenderingAdministratorTest(BaseWebTest, BaseAdministratorTestMixin):

    def setUp(self):
        super(ActiveTenderingAdministratorTest, self).setUp()
        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot()

        auction = context['auction']

        entrypoints = {}

        entrypoints['get_auction'] = '/auctions/{}'.format(auction['data']['id'])
        entrypoints['patch_auction'] = '/auctions/{}'.format(auction['data']['id'])
        self.auction = auction
        self.ENTRYPOINTS = entrypoints


def suite():
    suite = unittest.TestSuite()
    # auction tests
    suite.addTest(unittest.makeSuite(ActiveTenderingAdministratorTest))
    suite.addTest(unittest.makeSuite(ActiveTenderingTest))
    suite.addTest(unittest.makeSuite(ActiveTenderingWithoutDSTest))
    # questions test
    suite.addTest(unittest.makeSuite(ActiveTenderingQuestionsTest))
    # auction with documents tests
    suite.addTest(unittest.makeSuite(ActiveTenderingDocumentsTest))
    suite.addTest(unittest.makeSuite(ActiveTenderingOfflineDocumentsTest))
    suite.addTest(unittest.makeSuite(ActiveTenderingDocumentWithoutDSTest))
    # cancellations tests
    suite.addTest(unittest.makeSuite(ActiveTenderingCancellationsTest))
    suite.addTest(unittest.makeSuite(ActiveTenderingCancellationsWithoutDSTest))
    suite.addTest(unittest.makeSuite(ActiveTenderingCancellationsWithBidsTest))
    # cancellations with documents tests
    suite.addTest(unittest.makeSuite(ActiveTenderingCancellationsDocumentsTest))
    suite.addTest(unittest.makeSuite(ActiveTenderingCancellationsDocumentsWithoutDSTest))
    # bids tests
    suite.addTest(unittest.makeSuite(ActiveTenderingBidsDraftTest))
    suite.addTest(unittest.makeSuite(ActiveTenderingBidsPendingTest))
    suite.addTest(unittest.makeSuite(ActiveTenderingBidsActiveTest))

    suite.addTest(unittest.makeSuite(ActiveTenderingBidsDraftWithoutDSTest))
    suite.addTest(unittest.makeSuite(ActiveTenderingBidsPendingWithoutDSTest))
    suite.addTest(unittest.makeSuite(ActiveTenderingBidsActiveWithoutDSTest))
    # bids with documents tests
    suite.addTest(unittest.makeSuite(ActiveTenderingBidsDraftWithDocumentTest))
    suite.addTest(unittest.makeSuite(ActiveTenderingBidsPendingWithDocumentTest))
    suite.addTest(unittest.makeSuite(ActiveTenderingBidsActiveWithDocumentTest))

    suite.addTest(unittest.makeSuite(ActiveTenderingBidsDraftWithDocumentWithoutDSTest))
    suite.addTest(unittest.makeSuite(ActiveTenderingBidsPendingWithDocumentWithoutDSTest))
    suite.addTest(unittest.makeSuite(ActiveTenderingBidsActiveWithDocumentWithoutDSTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
