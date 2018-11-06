# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.base import snitch

from openprocurement.auctions.geb.tests.base import (
    BaseWebDocsTest
)
from openprocurement.auctions.geb.tests.blanks.create import (
    create_auction_dump
)
from openprocurement.auctions.geb.tests.blanks.draft import (
    get_auction_dump,
    phase_commit_dump
)
from openprocurement.auctions.geb.tests.blanks.active_rectification import (
    change_title_dump,
    add_document_dump
)
from openprocurement.auctions.geb.tests.blanks.active_tendering import (
    add_question_dump,
    answer_question_dump,
    bid_make_pending_dump,
    bid_delete_in_pending_status_dump,
    bid_get_in_pending_status_dump,
    bid_make_activate_dump,
    bid_add_dump
)
from openprocurement.auctions.geb.tests.blanks.active_auction import (
    get_auction_urls_dump
)
from openprocurement.auctions.geb.tests.helpers import (
    change_machine_state
)
from openprocurement.auctions.geb.tests.states import (
    ProcedureMachine
)

from openprocurement.auctions.geb.tests.blanks.active_qualification import (
    dump_bid_owner_upload_auction_protocol,
    dump_organizer_activate_award,
    dump_organizer_upload_auction_protocol
)
from openprocurement.auctions.geb.tests.blanks.active_awarded import (
    organizer_activate_contract_dump,
    organizer_uploads_the_contract_dump
)
from openprocurement.auctions.geb.tests.fixtures.active_awarded import (
    AUCTION_WITH_CONTRACT_WITH_DOCUMENT
)
from openprocurement.auctions.geb.tests.fixtures.active_tendering import (
    AUCTION_WITH_QUESTIONS as ACTIVE_TENDERING_AUCTION_WITH_QUESTION,
    AUCTION_WITH_BID_DRAFT,
    AUCTION_WITH_BID_PENDING
)


class CreateAuctionDumpTest(BaseWebDocsTest):

    test_create_auction_dump = snitch(create_auction_dump)

    def setUp(self):
        super(CreateAuctionDumpTest, self).setUp()
        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        change_machine_state(procedure, 'create')
        context = procedure.snapshot(dump=False)
        self.auction = context['auction']['data']


class DraftAuctionDumpTest(BaseWebDocsTest):

    test_get_auction_dump = snitch(get_auction_dump)
    test_phase_commit_dump = snitch(phase_commit_dump)

    def setUp(self):
        super(DraftAuctionDumpTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        change_machine_state(procedure, 'draft')
        context = procedure.snapshot()
        self.auction = context['auction']


class RectificationAuctionDumpTest(BaseWebDocsTest):

    test_change_title_dump = snitch(change_title_dump)

    def setUp(self):
        super(RectificationAuctionDumpTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        change_machine_state(procedure, 'active.rectification')
        context = procedure.snapshot()
        self.auction = context['auction']
        self.ENTRYPOINT = '/auctions/{}?acc_token={}'.format(self.auction['data']['id'],
                                                             self.auction['access']['token'])


class RectificationAuctionDocumentsDumpTest(BaseWebDocsTest):
    docservice = True

    test_add_document_dump = snitch(add_document_dump)

    def setUp(self):
        super(RectificationAuctionDocumentsDumpTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        change_machine_state(procedure, 'active.rectification')
        context = procedure.snapshot()
        self.auction = context['auction']
        self.ENTRYPOINT = '/auctions/{}/documents?acc_token={}'.format(self.auction['data']['id'],
                                                                       self.auction['access']['token'])


class TenderingAuctionDumpTest(BaseWebDocsTest):

    test_add_question_dump = snitch(add_question_dump)
    test_bid_add_dump = snitch(bid_add_dump)

    def setUp(self):
        super(TenderingAuctionDumpTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot()
        self.auction = context['auction']
        entrypoints = {}
        entrypoints['questions'] = '/auctions/{}/questions'.format(self.auction['data']['id'])
        entrypoints['bids'] = '/auctions/{}/bids'.format(self.auction['data']['id'])

        self.ENTRYPOINTS = entrypoints


class TenderingAuctionQuestionsDumpTest(BaseWebDocsTest):

    test_answer_question_dump = snitch(answer_question_dump)

    def setUp(self):
        super(TenderingAuctionQuestionsDumpTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=ACTIVE_TENDERING_AUCTION_WITH_QUESTION)

        self.auction = context['auction']
        self.questions = context['questions']


class TenderingAuctionBidsDraftDumpTest(BaseWebDocsTest):

    test_bid_make_pending_dump = snitch(bid_make_pending_dump)

    def setUp(self):
        super(TenderingAuctionBidsDraftDumpTest, self).setUp()

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

        self.ENTRYPOINTS = entrypoints
        self.bid = bid
        self.auction = auction


class TenderingAuctionBidsPendingDumpTest(BaseWebDocsTest):
    docservice = True

    test_bid_delete_in_pending_status_dump = snitch(bid_delete_in_pending_status_dump)
    test_bid_make_activate_dump = snitch(bid_make_activate_dump)
    test_bid_get_in_pending_status_dump = snitch(bid_get_in_pending_status_dump)

    def setUp(self):
        super(TenderingAuctionBidsPendingDumpTest, self).setUp()

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

        pattern = '/auctions/{auction}/bids/{bid}/documents?acc_token={token}'
        entrypoints['add_bid_document'] = pattern.format(auction=auction['data']['id'],
                                                         bid=bid['data']['id'],
                                                         token=bid['access']['token'])
        self.ENTRYPOINTS = entrypoints
        self.bid = bid
        self.auction = auction


class ActiveAuctionDumpTest(BaseWebDocsTest):
    docservice = True

    test_get_auction_urls_dump = snitch(get_auction_urls_dump)

    def setUp(self):
        super(ActiveAuctionDumpTest, self).setUp()
        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.auction')
        self.procedure = procedure

        self.app.authorization = ('Basic', ('auction', ''))


class ActiveQualificationDumpTest(BaseWebDocsTest):
    docservice = True

    test_dump_bid_owner_upload_auction_protocol = snitch(dump_bid_owner_upload_auction_protocol)
    test_dump_organizer_activate_award = snitch(dump_organizer_activate_award)
    test_dump_organizer_upload_auction_protocol = snitch(dump_organizer_upload_auction_protocol)

    def setUp(self):
        super(ActiveQualificationDumpTest, self).setUp()
        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.qualification')
        context = procedure.snapshot()

        award = context['awards'][0]
        bid = context['bids'][0]
        auction = context['auction']
        entrypoints = {}
        pattern = '/auctions/{}/awards/{}/documents?acc_token={}'
        entrypoints['award_document_post'] = pattern.format(auction['data']['id'],
                                                            award['data']['id'],
                                                            auction['access']['token'])

        pattern = '/auctions/{}'
        entrypoints['auction_get'] = pattern.format(auction['data']['id'])

        pattern = '/auctions/{}/contracts'
        entrypoints['contracts_get'] = pattern.format(auction['data']['id'])

        pattern = '/auctions/{}/awards/{}'
        entrypoints['award_get'] = pattern.format(auction['data']['id'],
                                                  award['data']['id'])

        pattern = '/auctions/{}/awards/{}?acc_token={}'
        entrypoints['award_patch'] = pattern.format(auction['data']['id'],
                                                    award['data']['id'],
                                                    auction['access']['token'])
        self.ENTRYPOINTS = entrypoints
        self.auction = auction
        self.award = award
        self.bid = bid
        self.ENTRYPOINTS = entrypoints
        self.auction = auction
        self.award = award
        self.bid = bid


class StatusActiveAwardedDumpTest(BaseWebDocsTest):
    docservice = True
    test_organizer_uploads_the_contract_dump = snitch(organizer_uploads_the_contract_dump)

    def setUp(self):
        super(StatusActiveAwardedDumpTest, self).setUp()
        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.awarded')
        context = procedure.snapshot()

        contract = context['contracts'][0]
        award = context['awards'][0]
        auction = context['auction']
        entrypoints = {}
        pattern = '/auctions/{}/contracts/{}/documents?acc_token={}'
        entrypoints['contract_document_post'] = pattern.format(auction['data']['id'],
                                                               contract['data']['id'],
                                                               auction['access']['token'])

        pattern = '/auctions/{}/contracts/{}?acc_token={}'
        entrypoints['contract_patch'] = pattern.format(auction['data']['id'],
                                                       contract['data']['id'],
                                                       auction['access']['token'])
        self.ENTRYPOINTS = entrypoints
        self.auction = auction
        self.contract = contract
        self.award = award


class ContractWithContractDocumentTest(BaseWebDocsTest):
    test_organizer_activate_contract = snitch(organizer_activate_contract_dump)

    def setUp(self):
        super(ContractWithContractDocumentTest, self).setUp()
        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.awarded')
        context = procedure.snapshot(fixture=AUCTION_WITH_CONTRACT_WITH_DOCUMENT)

        contract = context['contracts'][0]
        bid = context['bids'][0]
        auction = context['auction']
        entrypoints = {}

        pattern = '/auctions/{}'
        entrypoints['auction_get'] = pattern.format(auction['data']['id'])

        pattern = '/auctions/{}/contracts/{}'
        entrypoints['contract_get'] = pattern.format(auction['data']['id'],
                                                     contract['data']['id'])

        pattern = '/auctions/{}/contracts/{}?acc_token={}'
        entrypoints['contract_patch'] = pattern.format(auction['data']['id'],
                                                       contract['data']['id'],
                                                       auction['access']['token'])
        self.ENTRYPOINTS = entrypoints
        self.auction = auction
        self.contract = contract
        self.bid = bid


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CreateAuctionDumpTest))
    suite.addTest(unittest.makeSuite(DraftAuctionDumpTest))
    suite.addTest(unittest.makeSuite(RectificationAuctionDumpTest))
    suite.addTest(unittest.makeSuite(RectificationAuctionDocumentsDumpTest))
    suite.addTest(unittest.makeSuite(TenderingAuctionDumpTest))
    suite.addTest(unittest.makeSuite(TenderingAuctionBidsDraftDumpTest))
    suite.addTest(unittest.makeSuite(TenderingAuctionBidsPendingDumpTest))
    suite.addTest(unittest.makeSuite(TenderingAuctionQuestionsDumpTest))
    suite.addTest(unittest.makeSuite(ActiveAuctionDumpTest))
    suite.addTest(unittest.makeSuite(ActiveQualificationDumpTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
