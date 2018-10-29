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
    get_auction_auction,
    update_auction_urls,
    switch_to_qualification,
    switch_to_unsuccessful,
    get_participation_urls
)
from openprocurement.auctions.geb.tests.blanks.cancellations import (
    cancellation_make_clean_bids
)


class StatusActiveQualificationTest(BaseWebTest):

    test_get_auction_auction = snitch(get_auction_auction)

    def setUp(self):
        super(StatusActiveQualificationTest, self).setUp()
        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.qualification')
        self.procedure = procedure

        self.app.authorization = ('Basic', ('auction', ''))


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(StatusActiveQualificationTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
