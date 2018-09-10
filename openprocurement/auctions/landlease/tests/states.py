from copy import deepcopy
from openprocurement.auctions.core.utils import (
    calculate_business_date,
    get_now,
    apply_data_patch
)
from openprocurement.auctions.core.tests.base import IsoDateTimeType
from openprocurement.auctions.landlease.tests.specifications import REQUIRED_SCHEME_DEFINITION

from openprocurement.auctions.landlease.tests.helpers import (
    get_next_status,
    get_period_duration
)


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
        now = get_now()
        formater = IsoDateTimeType().to_primitive
        status = get_next_status(self.status)
        duration = get_period_duration(REQUIRED_SCHEME_DEFINITION, 'tenderPeriod')

        end_date = calculate_business_date(now, duration, self.auction)

        tender_period = {"startDate": formater(now),
                         "endDate": formater(end_date)}

        rectification_period = deepcopy(self.auction['rectificationPeriod'])
        rectification_period["endDate"] = formater(now)

        context['status'] = status
        context['tenderPeriod'] = tender_period
        context['rectificationPeriod'] = rectification_period
        return context

    def _db_save(self, context):
        auction = self._test.db.get(self.auction['id'])
        auction.update(apply_data_patch(auction, context))
        self._test.db.save(auction)
        return auction

    def _dispose(self):
        context = self._context()
        self._db_save(context)
        self._auction.update(context)

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
