# -*- coding: utf-8 -*-
import unittest
from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.geb.tests.base import (
    BaseWebTest
)
from openprocurement.auctions.geb.tests.states import (
    ProcedureMachine
)
from openprocurement.auctions.geb.tests.blanks.active_awarded import (
    organizer_uploads_the_contract,
    organizer_activate_contract
)
from openprocurement.auctions.geb.tests.fixtures.active_awarded import (
    AUCTION_WITH_CONTRACT_WITH_DOCUMENT
)


class StatusActiveAwardedTest(BaseWebTest):
    docservice = True

    test_organizer_downloads_the_contract = snitch(organizer_uploads_the_contract)

    def setUp(self):
        super(StatusActiveAwardedTest, self).setUp()
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


class ContractWithContractDocumentTest(BaseWebTest):
    test_organizer_activate_contract = snitch(organizer_activate_contract)

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
    suite.addTest(unittest.makeSuite(StatusActiveAwardedTest))
    suite.addTest(unittest.makeSuite(ContractWithContractDocumentTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
