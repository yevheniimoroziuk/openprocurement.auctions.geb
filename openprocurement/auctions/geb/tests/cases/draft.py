# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.geb.tests.base import (
    BaseWebTest,
)
from openprocurement.auctions.geb.tests.blanks.draft import (
    phase_commit,
    invalid_phase_commit,
    phase_commit_invalid_auctionPeriod
)

from openprocurement.auctions.geb.tests.helpers import (
    change_machine_state
)
from openprocurement.auctions.geb.tests.states import (
    ProcedureMachine
)


class StatusDraftTest(BaseWebTest):

    test_phase_commit = snitch(phase_commit)
    test_invalid_phase_commit = snitch(invalid_phase_commit)
    test_phase_commit_invalid_auctionPeriod = snitch(phase_commit_invalid_auctionPeriod)

    def setUp(self):
        super(StatusDraftTest, self).setUp()
        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        change_machine_state(procedure, 'draft')
        self.procedure = procedure


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(StatusDraftTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
