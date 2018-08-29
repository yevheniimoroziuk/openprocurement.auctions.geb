# -*- coding: utf-8 -*-

import unittest

from openprocurement.auctions.landlease.tests import procedure


def suite():
    suite = unittest.TestSuite()
    suite.addTest(procedure.suite())
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
