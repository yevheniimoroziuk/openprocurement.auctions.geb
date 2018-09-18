import os
from openprocurement.auctions.geb.tests.helpers import (
    get_next_status,
    create_active_bid,
    create_bid
)


class State(object):

    @property
    def auction(self):
        return self._auction

    @property
    def status(self):
        return self._auction['status']

    def _dispose(self):
        pass

    def _prev_state_workflow(self):
        pass

    def _update_auction(self):
        response = self._test.app.get('/auctions/{}'.format(self.auction['id']))
        self._auction = response.json['data']

    def _solely(self):
        next_status = get_next_status(self.status)
        request_data = {"data": {"status": next_status}}
        entrypoint = '/auctions/{}?acc_token={}'.format(self._auction['id'],
                                                        self._access['token'])
        self._test.app.patch_json(entrypoint, request_data)

    def _chronograph(self):
        auth = self._test.app.authorization
        self._test.app.authorization = ('Basic', ('chronograph', ''))

        request_data = {'data': {'id': self._auction['id']}}
        entrypoint = '/auctions/{}'.format(self._auction['id'])
        self._test.app.patch_json(entrypoint, request_data)
        self._test.app.authorization = auth


class ActiveAuction(State):

    def __init__(self, auction, access, test):
        self._auction = auction
        self._access = access
        self.extra = {}
        self._test = test
        self._dispose()

    def _fake_now(self):
        destination = self._auction['enquiryPeriod']['endDate']
        os.environ['FAKE_NOW'] = destination

    def _dispose(self):
        self._prev_state_workflow()
        self._fake_now()
        self._chronograph()
        self._update_auction()


class ActiveEnquiry(State):

    def __init__(self, auction, access, test):
        self._auction = auction
        self._access = access
        self.extra = {}
        self._test = test
        self._dispose()

    def _prev_state_workflow(self):
        bids = []

        bids.append(create_active_bid(self._test, self._auction))
        bids.append(create_active_bid(self._test, self._auction))
        bids.append(create_bid(self._test, self._auction))
        self.extra['bids'] = bids

    def _fake_now(self):
        destination = self._auction['tenderPeriod']['endDate']
        os.environ['FAKE_NOW'] = destination

    def _dispose(self):
        self._prev_state_workflow()
        self._fake_now()
        self._chronograph()
        self._update_auction()

    def _next(self):
        return ActiveAuction(self._auction, self._access, self._test)


class ActiveTendering(State):

    def __init__(self, auction, access, test):
        self._auction = auction
        self._access = access
        self._test = test
        self._dispose()

    def _fake_now(self):
        destination = self._auction['rectificationPeriod']['endDate']
        os.environ['FAKE_NOW'] = destination

    def _dispose(self):
        self._prev_state_workflow()
        self._fake_now()
        self._chronograph()
        self._update_auction()

    def _next(self):
        return ActiveEnquiry(self._auction, self._access, self._test)


class ActiveRetification(State):

    def __init__(self, auction, access, test):
        self._auction = auction
        self._access = access
        self._test = test
        self._dispose()

    def _dispose(self):
        self._prev_state_workflow()
        self._solely()
        self._update_auction()

    def _next(self):
        return ActiveTendering(self._auction, self._access, self._test)


class Draft(State):

    def __init__(self, auction, access, test):
        self._auction = auction
        self._access = access
        self._test = test
        self._dispose()

    def _next(self):
        return ActiveRetification(self._auction, self._access, self._test)


class Create(State):
    def __init__(self, auction, access, test):
        self._auction = auction
        self._access = access
        self._test = test

    def _next(self):
        return Draft(self._auction, self._access, self._test)


class Procedure(object):

    def __init__(self, auction, access, test):
        self._auction = auction
        self.state = Create(self._auction, access, test)

    def _next(self):
        self.state = self.state._next()

    def __iter__(self):
        return self

    def next(self):
        self._next()
        return self.state
