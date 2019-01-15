import unittest
from copy import deepcopy
from iso8601 import parse_date
from uuid import uuid4
from datetime import timedelta, time
from openprocurement.auctions.core.utils import (
    get_now,
    SANDBOX_MODE
)
from openprocurement.auctions.geb.utils import (
    calculate_certainly_business_date as ccbd
)
from openprocurement.auctions.geb.tests.fixtures.items import (
    TEST_ITEM
)


@unittest.skipIf(SANDBOX_MODE, 'If sandbox mode is it enabled generating correct periods')
def check_generated_rectification_period(test_case):
    # phase commit
    next_status = 'active.rectification'
    now = get_now()

    request_data = {"data": {'status': next_status}}
    auth = test_case.app.authorization

    test_case.app.authorization = ('Basic', ('{}'.format(test_case.auction['access']['owner']), ''))

    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data)
    test_case.app.authorization = auth

    # check duration of rectification Period
    expected_duration = timedelta(hours=48)

    rectification_period = response.json['data']['rectificationPeriod']
    start_date = parse_date(rectification_period['startDate'])
    end_date = parse_date(rectification_period['endDate'])
    received_duration = end_date - start_date

    test_case.assertEqual(received_duration, expected_duration)

    # check if start of rectification Period start directly after phase commit
    verbose_now = now.replace(microsecond=0, second=0).isoformat()
    verbose_start_date = start_date.replace(microsecond=0, second=0).isoformat()
    test_case.assertEqual(verbose_start_date, verbose_now)


@unittest.skipIf(SANDBOX_MODE, 'If sandbox mode is it enabled generating correct periods')
def check_generated_tender_period(test_case):
    # phase commit
    next_status = 'active.rectification'

    request_data = {"data": {'status': next_status}}
    auth = test_case.app.authorization

    response = test_case.app.get(test_case.ENTRYPOINTS['get_auction'], request_data)
    auction_start_date = parse_date(response.json['data']['auctionPeriod']['startDate'])

    test_case.app.authorization = ('Basic', ('{}'.format(test_case.auction['access']['owner']), ''))

    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data)
    test_case.app.authorization = auth

    tender_period = response.json['data']['tenderPeriod']
    tender_period_start_date = parse_date(tender_period['startDate'])
    tender_period_end_date = parse_date(tender_period['endDate'])

    # check if start date is equal to rectification period endDate
    rectification_period = response.json['data']['rectificationPeriod']
    rectification_period_end_date = parse_date(rectification_period['endDate'])
    test_case.assertEqual(rectification_period_end_date, tender_period_start_date)

    # check if end date ends in 20:00 hour
    expected_end_time = time(hour=20, minute=0)
    test_case.assertEqual(expected_end_time, tender_period_end_date.time())

    # check difference of tenderPeriod endDate and auction start date date
    expected_end_date = ccbd(auction_start_date, -timedelta(days=4),
                             specific_hour=20, working_days=True)
    test_case.assertEqual(expected_end_date, tender_period_end_date)


@unittest.skipIf(SANDBOX_MODE, 'If sandbox mode is it enabled generating correct periods')
def check_generated_enquiry_period(test_case):
    # phase commit
    next_status = 'active.rectification'
    request_data = {"data": {'status': next_status}}
    auth = test_case.app.authorization

    test_case.app.authorization = ('Basic', ('{}'.format(test_case.auction['access']['owner']), ''))

    response = test_case.app.get(test_case.ENTRYPOINTS['get_auction'], request_data)
    auction_start_date = parse_date(response.json['data']['auctionPeriod']['startDate'])

    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data)
    test_case.app.authorization = auth

    enquiry_period = response.json['data']['enquiryPeriod']
    enquiry_period_start_date = parse_date(enquiry_period['startDate'])
    enquiry_period_end_date = parse_date(enquiry_period['endDate'])

    # check if start date is equal to rectification period startDate
    rectification_period = response.json['data']['rectificationPeriod']
    rectification_period_start_date = parse_date(rectification_period['startDate'])
    test_case.assertEqual(rectification_period_start_date, enquiry_period_start_date)

    # check if end date ends in 20:00 hour
    expected_end_time = time(hour=20, minute=0)
    test_case.assertEqual(expected_end_time, enquiry_period_end_date.time())

    # check difference of equiryPeriod endDate and auction startDate
    expected_end_date = ccbd(auction_start_date, -timedelta(days=1),
                             specific_hour=20)
    test_case.assertEqual(expected_end_date, enquiry_period_end_date)


def phase_commit(test_case):
    next_status = 'active.rectification'
    request_data = {"data": {'status': next_status}}
    auth = test_case.app.authorization

    test_case.app.authorization = ('Basic', ('{}'.format(test_case.auction['access']['owner']), ''))

    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data)
    test_case.app.authorization = auth

    test_case.assertEqual(next_status, response.json['data']['status'])


def phase_commit_without_items(test_case):
    """
        Can`t switch procedure to 'active.rectification' without items
    """
    auth = test_case.app.authorization
    test_case.app.authorization = ('Basic', ('{}'.format(test_case.auction['access']['owner']), ''))

    next_status = 'active.rectification'
    request_data = {"data": {'status': next_status}}

    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data, status=403)
    test_case.assertEqual(response.status, '403 Forbidden')

    test_case.app.authorization = auth


def auction_patch_items(test_case):
    """
        Can patch items in 'draft' status
    """
    auth = test_case.app.authorization
    test_case.app.authorization = ('Basic', ('{}'.format(test_case.auction['access']['owner']), ''))

    new_item = deepcopy(TEST_ITEM)
    new_item['id'] = uuid4().hex
    request_data = {"data": {'items': [new_item]}}

    test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data)
    response = test_case.app.get(test_case.ENTRYPOINTS['get_auction'])

    auction_items = [item['id'] for item in response.json['data']['items']]
    test_case.assertIn(new_item['id'], auction_items)

    test_case.app.authorization = auth


@unittest.skipIf(SANDBOX_MODE, 'If sandbox mode is it enabled generating correct periods')
def phase_commit_invalid_auctionPeriod(test_case):

    expected_http_status = '422 Unprocessable Entity'
    request_data = {"data": {'status': 'active.rectification'}}

    auth = test_case.app.authorization
    test_case.app.authorization = ('Basic', ('{}'.format(test_case.auction['access']['owner']), ''))
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data, status=422)
    test_case.app.authorization = auth

    test_case.assertEqual(expected_http_status, response.status)


def invalid_phase_commit(test_case):

    next_status = 'active.tendering'
    request_data = {"data": {'status': next_status}}
    auth = test_case.app.authorization

    test_case.app.authorization = ('Basic', ('{}'.format(test_case.auction['access']['owner']), ''))

    test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data, status=403)
    test_case.app.authorization = auth


def get_auction_dump(test_case):

    entrypoint = '/auctions/{}'.format(test_case.auction['data']['id'])
    response = test_case.app.get(entrypoint)
    filename = 'docs/source/tutorial/get_draft_auction.http'

    test_case.dump(response.request, response, filename)


def phase_commit_dump(test_case):
    next_status = 'active.rectification'
    request_data = {"data": {'status': next_status}}
    auth = test_case.app.authorization

    test_case.app.authorization = ('Basic', ('{}'.format(test_case.auction['access']['owner']), ''))
    entrypoint = '/auctions/{}?acc_token={}'.format(test_case.auction['data']['id'],
                                                    test_case.auction['access']['token'])
    response = test_case.app.patch_json(entrypoint, request_data)
    filename = 'docs/source/tutorial/phase_commit.http'
    test_case.dump(response.request, response, filename)
    test_case.app.authorization = auth


def item_post(test_case):
    expected_http_status = '201 Created'

    request_data = {'data': TEST_ITEM}
    response = test_case.app.post_json(test_case.ENTRYPOINTS['item_post'], request_data)
    test_case.assertEqual(response.status, expected_http_status)
    item = response.json['data']

    entrypoint = '/auctions/{}/items/{}'.format(test_case.auction['data']['id'], item['id'])
    response = test_case.app.get(entrypoint, request_data)
    test_case.assertEqual(response.status, '200 OK')


def item_post_collections(test_case):

    request_data = {'data': {'items': [TEST_ITEM]}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data)
    expected_http_status = '200 OK'
    test_case.assertEqual(response.status, expected_http_status)

    response = test_case.app.get(test_case.ENTRYPOINTS['get_auction'])
    items = response.json['data']['items']
    items_ids = [item['id'] for item in items]
    test_case.assertIn(TEST_ITEM['id'], items_ids)
