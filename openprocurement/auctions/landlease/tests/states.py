import iso8601
from openprocurement.auctions.core.utils import (
    calculate_business_date,
    get_now,
    apply_data_patch
)
from openprocurement.auctions.core.tests.base import IsoDateTimeType

from openprocurement.auctions.landlease.tests.helpers import (
    get_next_status,
    get_period_duration,
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


class ActiveEnquiry(State):

    def __init__(self, auction, access, test):
        self._auction = auction
        self._access = access
        self.extra = {}
        self._test = test
        self._dispose()

    def _workflow(self):
        bids = []

        bids.append(create_active_bid(self._test, self._auction))
        bids.append(create_active_bid(self._test, self._auction))
        bids.append(create_bid(self._test, self._auction))
        self.extra['bids'] = bids

    def _context(self):
        context = {}
        now = get_now()
        formater = IsoDateTimeType().to_primitive
        status = get_next_status(self.status)
        duration_rectification = get_period_duration(self._auction, 'rectificationPeriod')
        duration_tendering = get_period_duration(self._auction, 'tenderPeriod')
        duration_enquiry = get_period_duration(self._auction, 'enquiryPeriod')

        start_tendering_and_enquiry = calculate_business_date(now, -duration_tendering, self.auction)

        end_date_rectification = start_tendering_and_enquiry
        end_date_tendering = now
        remainder = duration_enquiry - duration_tendering
        end_date_enquiry = calculate_business_date(now, remainder, self.auction)

        start_date_rectification = calculate_business_date(end_date_rectification, -duration_rectification, self.auction)
        start_date_tendering = start_tendering_and_enquiry
        start_date_enquiry = start_tendering_and_enquiry

        tender_period = {"startDate": formater(start_date_tendering),
                         "endDate": formater(end_date_tendering)}

        enquiry_period = {"startDate": formater(start_date_enquiry),
                          "endDate": formater(end_date_enquiry)}

        rectification_period = {"startDate": formater(start_date_rectification),
                                "endDate": formater(end_date_rectification)}

        context['status'] = status
        context['rectificationPeriod'] = rectification_period
        context['tenderPeriod'] = tender_period
        context['enquiryPeriod'] = enquiry_period
        return context

    def _db_save(self, context):
        auction = self._test.db.get(self.auction['id'])
        auction.update(apply_data_patch(auction, context))
        self._test.db.save(auction)
        return auction

    def _dispose(self):
        self._workflow()
        context = self._context()
        self._db_save(context)
        self._auction.update(context)


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

        shouldStartAfter = iso8601.parse_date(self._auction['auctionPeriod']['shouldStartAfter'])
        enquiry_period_end = iso8601.parse_date(self._auction['enquiryPeriod']['endDate'])
        odds = shouldStartAfter - enquiry_period_end

        duration_rectification = get_period_duration(self._auction, 'rectificationPeriod')
        duration_tendering = get_period_duration(self._auction, 'tenderPeriod')
        duration_enquiry = get_period_duration(self._auction, 'enquiryPeriod')

        end_date_rectification = now
        end_date_tendering = calculate_business_date(now, duration_tendering, self._auction)
        end_date_enquiry = calculate_business_date(now, duration_enquiry, self._auction)

        new_shoulfStartAfter = calculate_business_date(end_date_enquiry, odds, self._auction)

        start_date_rectification = calculate_business_date(now, -duration_rectification, self._auction)
        start_date_tendering = now
        start_date_enquiry = now

        tender_period = {"startDate": formater(start_date_tendering),
                         "endDate": formater(end_date_tendering)}
        enquiry_period = {"startDate": formater(start_date_enquiry),
                          "endDate": formater(end_date_enquiry)}

        rectification_period = {"startDate": formater(start_date_rectification),
                                "endDate": formater(end_date_rectification)}

        context['status'] = status
        context['rectificationPeriod'] = rectification_period
        context['tenderPeriod'] = tender_period
        context['enquiryPeriod'] = enquiry_period
        context['auctionPeriod'] = {}
        context['auctionPeriod']['shouldStartAfter'] = formater(new_shoulfStartAfter)
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
        return ActiveEnquiry(self._auction, self._access, self._test)


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
