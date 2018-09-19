import os
from openprocurement.auctions.geb.tests.helpers import (
    get_next_status,
    create_pending_bid,
    activate_bid,
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

    def _update_extra(self):
        for bid in self.extra.get('bids'):
            prev_auth = self._test.app.authorization
            self._test.authorization = bid['owner']
            entrypoint = '/auctions/{}/bids/{}?acc_token={}'.format(self._auction['id'],
                                                                    bid['data']['id'],
                                                                    bid['access']['token'])
            response = self._test.app.get(entrypoint)
            bid['data'] = response.json['data']
            self._test.authorization = prev_auth


class ActiveAuction(State):

    def __init__(self, auction, access, test, extra):
        self._auction = auction
        self._access = access
        self.extra = extra
        self._test = test
        self._dispose()

    def _prev_state_workflow(self):
        for bid_number, bid in enumerate(self.extra['bids'], 1):
            activate_bid(self._test, self._auction, bid, bid_number)

    def _fake_now(self):
        destination = self._auction['enquiryPeriod']['endDate']
        os.environ['FAKE_NOW'] = destination

    def _dispose(self):
        self._prev_state_workflow()
        self._fake_now()
        self._chronograph()
        self._update_extra()
        self._update_auction()


class ActiveEnquiry(State):

    def __init__(self, auction, access, test, extra):
        self._auction = auction
        self._access = access
        self._test = test
        self.extra = extra
        self._dispose()

    def _prev_state_workflow(self):
        bids = []

        bids.append(create_pending_bid(self._test, self._auction))
        bids.append(create_pending_bid(self._test, self._auction))
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
        return ActiveAuction(self._auction, self._access, self._test, self.extra)


class ActiveTendering(State):

    def __init__(self, auction, access, test, extra):
        self._auction = auction
        self._access = access
        self._test = test
        self.extra = extra
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
        return ActiveEnquiry(self._auction, self._access, self._test, self.extra)


class ActiveRetification(State):

    def __init__(self, auction, access, test, extra):
        self._auction = auction
        self._access = access
        self._test = test
        self.extra = extra
        self._dispose()

    def _dispose(self):
        self._prev_state_workflow()
        self._solely()
        self._update_auction()

    def _next(self):
        return ActiveTendering(self._auction, self._access, self._test, self.extra)


class Draft(State):

    def __init__(self, auction, access, test, extra):
        self._auction = auction
        self._access = access
        self._test = test
        self.extra = extra
        self._dispose()

    def _next(self):
        return ActiveRetification(self._auction, self._access, self._test, self.extra)


class Create(State):
    def __init__(self, auction, access, test, extra):
        self._auction = auction
        self._access = access
        self._test = test
        self.extra = extra

    def _next(self):
        return Draft(self._auction, self._access, self._test, self.extra)


class Procedure(object):

    def __init__(self, auction, access, test):
        self._auction = auction
        self.extra = {}
        self.state = Create(self._auction, access, test, self.extra)

    def _next(self):
        self.state = self.state._next()

    def __iter__(self):
        return self

    def next(self):
        self._next()
        return self.state
