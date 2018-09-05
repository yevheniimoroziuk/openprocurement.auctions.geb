from openprocurement.auctions.landlease.tests.helpers import get_next_status
from datetime import datetime, timedelta
from openprocurement.auctions.core.utils import apply_data_patch


class State(object):

    @property
    def auction(self):
        return self._auction

    @property
    def status(self):
        return self._auction['status']


class ActiveTendering(State):

    def __init__(self, auction, access, test):
        self._auction = auction
        self._access = access
        self._test = test
        self._dispose()

    def _context(self):
        context = {}
        now = datetime.now()
        status = get_next_status(self.status)
        tender_period = {"startDate": (now).isoformat(),
                         "endDate": (now + timedelta(days=7)).isoformat()}

        context['status'] = status
        context['tenderPeriod'] = tender_period
        return context

    def _db_save(self, context):
        auction = self._test.db.get(self.auction['id'])
        auction.update(apply_data_patch(auction, context))
        self._test.db.save(auction)
        return auction

    def _dispose(self):
        context = self._context()
        self._auction = self._db_save(context)

    def _next(self):
        return ActiveTendering(self._auction, self._access, self._test)


class ActiveRetification(State):

    def __init__(self, auction, access, test):
        self._auction = auction
        self._access = access
        self._test = test
        self._dispose()

    def _dispose(self):
        next_status = get_next_status(self.status)
        request_data = {"data": {"status": next_status}}
        entrypoint = '/auctions/{}?acc_token={}'.format(self.auction['id'],
                                                        self._access['token'])

        self._test.app.patch_json(entrypoint, request_data)
        response = self._test.app.get('/auctions/{}'.format(self.auction['id']))
        self._auction = response.json['data']

    def _next(self):
        return ActiveTendering(self.auction, self._access, self._test)


class Draft(State):

    def __init__(self, auction, access, test):
        self._auction = auction
        self._access = access
        self._test = test
        self._dispose()

    def _dispose(self):
        pass

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
