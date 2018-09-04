# -*- coding: utf-8 -*-
import os

from openprocurement.auctions.core.tests.base import (
    BaseWebTest as CoreBaseWebTest,
    BaseAuctionWebTest as CoreBaseAuctionWebTest,
)
from openprocurement.auctions.core.tests.base import MOCK_CONFIG as BASE_MOCK_CONFIG
from openprocurement.auctions.core.utils import connection_mock_config

from openprocurement.auctions.landlease.tests.fixtures import (
    PARTIAL_MOCK_CONFIG,
    test_auction_data
)

from openprocurement.auctions.landlease.tests.helpers import get_next_status

MOCK_CONFIG = connection_mock_config(PARTIAL_MOCK_CONFIG,
                                     base=BASE_MOCK_CONFIG,
                                     connector=('plugins', 'api', 'plugins',
                                                'auctions.core', 'plugins'))


class BaseWebTest(CoreBaseWebTest):

    """Base Web Test to test openprocurement.auctions.landlease.

    It setups the database before each test and delete it after.
    """

    relative_to = os.path.dirname(__file__)
    mock_config = MOCK_CONFIG


class BaseAuctionWebTest(CoreBaseAuctionWebTest):
    relative_to = os.path.dirname(__file__)
    initial_data = test_auction_data
    mock_config = MOCK_CONFIG


class State(object):

    def next_status(self):
        """
        Handle next_status state that are delegated to this State.
        """
        pass


class ActiveRetification(State):

    def __init__(self, auction, access, test):
        self._auction = auction
        self._access = access
        self._test = test
        self._dispose()

    @property
    def auction(self):
        return self._auction

    @property
    def status(self):
        return self._auction['status']

    def _dispose(self):
        next_status = get_next_status(self._auction['status'])
        request_data = {"data": {"status": next_status}}
        entrypoint = '/auctions/{}?acc_token={}'.format(self._auction['id'],
                                                        self._access['token'])

        self._test.patch_json(entrypoint, request_data)
        response = self._test.get('/auctions/{}'.format(self._auction['id']))
        self._auction = response.json['data']

    def next_status(self, status):
        return "end"


class Draft(State):

    def __init__(self, auction, access, test):
        self._auction = auction
        self._access = access
        self._test = test
        self._dispose()

    @property
    def auction(self):
        return self._auction

    @property
    def status(self):
        return self._auction['status']

    def _dispose(self):
        pass

    def next_status(self):
        return ActiveRetification(self._auction, self._access, self._test)


class Procedure(object):

    def __init__(self, auction, access, test):
        self._auction = auction
        self._access = access
        self.state = Draft(self._auction, self._access, test)

    def next_status(self):
        self.state = self.state.next_status()
