# -*- coding: utf-8 -*-
import unittest
from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.geb.tests.base import (
    BaseWebTest
)
from openprocurement.auctions.geb.tests.states import (
    ProcedureMachine
)
from openprocurement.auctions.geb.tests.blanks.active_qualification import (
    organizer_uploads_the_auction_protocol,
    bid_owner_uploads_the_auction_protocol,
    organizer_activate_award
)
from openprocurement.auctions.geb.tests.fixtures.active_qualification import (
    AUCTION_WITH_AWARD_WITH_PROTOCOL
)


class StatusActiveQualificationTest(BaseWebTest):
    docservice = True

    test_organizer_downloads_the_auction_protocol = snitch(organizer_uploads_the_auction_protocol)
    test_bid_owner_downloads_the_auction_protocol = snitch(bid_owner_uploads_the_auction_protocol)

    def setUp(self):
        super(StatusActiveQualificationTest, self).setUp()
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

        pattern = '/auctions/{}/awards/{}?acc_token={}'
        entrypoints['award_patch'] = pattern.format(auction['data']['id'],
                                                    award['data']['id'],
                                                    auction['access']['token'])
        self.ENTRYPOINTS = entrypoints
        self.auction = auction
        self.award = award
        self.bid = bid


class AwardWithProtocolTest(BaseWebTest):
    test_organizer_activate_award = snitch(organizer_activate_award)

    def setUp(self):
        super(AwardWithProtocolTest, self).setUp()
        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.qualification')
        context = procedure.snapshot(fixture=AUCTION_WITH_AWARD_WITH_PROTOCOL)

        award = context['awards'][0]
        bid = context['bids'][0]
        auction = context['auction']
        entrypoints = {}

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


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(StatusActiveQualificationTest))
    suite.addTest(unittest.makeSuite(AwardWithProtocolTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
