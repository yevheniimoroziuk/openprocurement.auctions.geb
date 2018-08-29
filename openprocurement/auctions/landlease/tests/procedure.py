# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.base import snitch

from openprocurement.auctions.landlease.tests.base import (
    test_auction_data,
    BaseWebTest,
    # BaseAuctionWebTest,
)

from openprocurement.auctions.landlease.tests.blanks.procedure import (
    create_auction_common,
    create_auction,
    create_auction_invalid_required_fields,
    create_auction_invalid_unsupported_media_type,
    create_auction_invalid_unprocessable_entity_common
)


class CreateAuctionResourceTest(BaseWebTest):
    initial_data = test_auction_data

    test_create_auction = snitch(create_auction)
    test_create_auction_common = snitch(create_auction_common)


class CreateInvalidAuctionResourceTest(BaseWebTest):
    initial_data = test_auction_data

    test_create_auction_invalid_required_fields = snitch(create_auction_invalid_required_fields)
    test_create_auction_invalid_unsupported_media_type = snitch(create_auction_invalid_unsupported_media_type)
    test_create_auction_invalid_unprocessable_entity_common = snitch(create_auction_invalid_unprocessable_entity_common)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CreateAuctionResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
