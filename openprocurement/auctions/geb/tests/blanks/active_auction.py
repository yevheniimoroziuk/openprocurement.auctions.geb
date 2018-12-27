import unittest
from freezegun import freeze_time
from copy import deepcopy
from iso8601 import parse_date
from datetime import timedelta

from openprocurement.auctions.core.tests.base import (
    test_document_data
)
from openprocurement.auctions.core.utils import (
    set_specific_hour,
    SANDBOX_MODE
)

from openprocurement.auctions.geb.tests.fixtures.common import (
    test_question_data
)
from openprocurement.auctions.geb.tests.fixtures.active_auction import (
    AUCTION,
    AUCTION_WITH_URLS,
    AUCTION_WITH_DOCUMENT,
    AUCTION_WITH_QUESTION
)
from openprocurement.auctions.geb.utils import (
    calculate_certainly_business_date as ccbd
)


def bid_get(test_case):
    auth = test_case.app.authorization

    # build context of test
    context = test_case.procedure.snapshot(fixture=AUCTION_WITH_URLS)
    auction = context['auction']
    bid = context['bids'][0]

    # auth as bid_owner
    test_case.app.authorization = ('Basic', ('{}'.format(bid['access']['owner']), ''))

    expected_http_status = '200 OK'
    pattern = '/auctions/{}/bids/{}?acc_token={}'
    entrypoint = pattern.format(auction['data']['id'], bid['data']['id'], bid['access']['token'])
    response = test_case.app.get(entrypoint)
    test_case.assertEqual(expected_http_status, response.status)

    # auth as auction owner
    test_case.app.authorization = ('Basic', ('{}'.format(auction['access']['owner']), ''))

    # not bid owner can`t get bid in auction status 'active.auction'
    expected_http_status = '403 Forbidden'
    pattern = '/auctions/{}/bids/{}'
    entrypoint = pattern.format(auction['data']['id'], bid['data']['id'])
    response = test_case.app.get(entrypoint, status=403)
    test_case.assertEqual(expected_http_status, response.status)

    test_case.app.authorization = auth


def bid_delete(test_case):
    # can`t delete bid in auction status 'active.auction'

    # build context of test
    context = test_case.procedure.snapshot(fixture=AUCTION_WITH_URLS)
    auction = context['auction']
    bid = context['bids'][0]

    auth = test_case.app.authorization

    # auth as bid owner
    test_case.app.authorization = ('Basic', ('{}'.format(bid['access']['owner']), ''))
    # build request
    expected_http_status = '403 Forbidden'
    pattern = '/auctions/{}/bids/{}?acc_token={}'
    entrypoint = pattern.format(auction['data']['id'], bid['data']['id'], bid['access']['token'])
    # try to delete bid
    response = test_case.app.delete_json(entrypoint, status=403)
    test_case.assertEqual(expected_http_status, response.status)

    test_case.app.authorization = auth


def auction_document_post(test_case):
    # procedure owner can`t create auction document procedure status 'active.auction'

    # build context of test
    context = test_case.procedure.snapshot(fixture=AUCTION_WITH_DOCUMENT)
    auction = context['auction']

    auth = test_case.app.authorization

    # auth as auction owner
    test_case.app.authorization = ('Basic', ('{}'.format(auction['access']['owner']), ''))

    # build request
    document = deepcopy(test_document_data)
    url = test_case.generate_docservice_url(),
    document['url'] = url[0]
    request_data = {'data': document}
    pattern = '/auctions/{}/documents?acc_token={}'
    entrypoint = pattern.format(auction['data']['id'], auction['access']['token'])
    # try to post auction document
    response = test_case.app.post_json(entrypoint, request_data, status=403)
    test_case.assertEqual(response.status, '403 Forbidden')

    test_case.app.authorization = auth


def bid_document_post(test_case):
    # bid owner can`t create bid document procedure status 'active.auction'

    # build context of test
    context = test_case.procedure.snapshot(fixture=AUCTION_WITH_DOCUMENT)
    auction = context['auction']
    bid = context['bids'][0]

    auth = test_case.app.authorization

    # auth as bid owner
    test_case.app.authorization = ('Basic', ('{}'.format(bid['access']['owner']), ''))

    # build request
    document = deepcopy(test_document_data)
    url = test_case.generate_docservice_url(),
    document['url'] = url[0]
    request_data = {'data': document}
    pattern = '/auctions/{}/bids/{}/documents?acc_token={}'
    entrypoint = pattern.format(auction['data']['id'],
                                bid['data']['id'],
                                bid['access']['token'])
    # try to post bid document
    response = test_case.app.post_json(entrypoint, request_data, status=403)
    test_case.assertEqual(response.status, '403 Forbidden')

    test_case.app.authorization = auth


def auction_question_post(test_case):
    # can`t add question in procedure status 'active.auction'

    # build context of test
    context = test_case.procedure.snapshot(fixture=AUCTION_WITH_DOCUMENT)
    auction = context['auction']

    auth = test_case.app.authorization

    # auth as auction owner
    test_case.app.authorization = ('Basic', ('{}'.format(auction['access']['owner']), ''))

    # build request
    request_data = test_question_data
    pattern = '/auctions/{}/questions?acc_token={}'
    entrypoint = pattern.format(auction['data']['id'],
                                auction['access']['token'])
    # try to post question
    response = test_case.app.post_json(entrypoint, request_data, status=403)
    test_case.assertEqual(response.status, '403 Forbidden')

    test_case.app.authorization = auth


def auction_document_patch(test_case):
    context = test_case.procedure.snapshot(fixture=AUCTION_WITH_DOCUMENT)
    auction = context['auction']
    document = context['documents'][0]

    field = 'documentType'
    new = 'technicalSpecifications'
    request_data = {'data': {field: new}}

    auth = test_case.app.authorization

    # auth as auction owner
    test_case.app.authorization = ('Basic', ('{}'.format(auction['access']['owner']), ''))

    pattern = '/auctions/{}/documents/{}?acc_token={}'
    entrypoint = pattern.format(auction['data']['id'], document['data']['id'], auction['access']['token'])
    response = test_case.app.patch_json(entrypoint, request_data, status=403)
    test_case.assertEqual(response.status, '403 Forbidden')

    test_case.app.authorization = auth


def auction_item_patch(test_case):
    context = test_case.procedure.snapshot()
    auction = context['auction']
    item = context['items'][0]

    field = 'description'
    new = 'new description'
    request_data = {'data': {field: new}}

    auth = test_case.app.authorization

    # auth as auction owner
    test_case.app.authorization = ('Basic', ('{}'.format(auction['access']['owner']), ''))

    pattern = '/auctions/{}/items/{}?acc_token={}'
    entrypoint = pattern.format(auction['data']['id'], item['data']['id'], auction['access']['token'])
    response = test_case.app.patch_json(entrypoint, request_data, status=403)
    test_case.assertEqual(response.status, '403 Forbidden')

    test_case.app.authorization = auth


def auction_question_patch(test_case):
    context = test_case.procedure.snapshot(fixture=AUCTION_WITH_QUESTION)
    auction = context['auction']
    question = context['questions'][0]

    field = 'title'
    new = 'New title'
    request_data = {'data': {field: new}}

    auth = test_case.app.authorization

    # auth as auction owner
    test_case.app.authorization = ('Basic', ('{}'.format(auction['access']['owner']), ''))

    pattern = '/auctions/{}/questions/{}?acc_token={}'
    entrypoint = pattern.format(auction['data']['id'], question['data']['id'], auction['access']['token'])
    response = test_case.app.patch_json(entrypoint, request_data, status=403)
    test_case.assertEqual(response.status, '403 Forbidden')

    test_case.app.authorization = auth


def bid_patch(test_case):
    context = test_case.procedure.snapshot(fixture=AUCTION_WITH_URLS)
    auction = context['auction']
    bid = context['bids'][0]

    auth = test_case.app.authorization

    # auth as bid owner
    test_case.app.authorization = ('Basic', ('{}'.format(bid['access']['owner']), ''))

    request_data = {"data": {"value": {'amount': 102}}}
    pattern = '/auctions/{}/bids/{}?acc_token={}'
    entrypoint = pattern.format(auction['data']['id'], bid['data']['id'], bid['access']['token'])
    # path bid
    response = test_case.app.patch_json(entrypoint, request_data, status=403)
    expected_http_status = '403 Forbidden'
    test_case.assertEqual(expected_http_status, response.status)

    test_case.app.authorization = auth


def module_auction_post_audit(test_case):
    context = test_case.procedure.snapshot(fixture=AUCTION)
    auction = context['auction']

    entrypoint = '/auctions/{}/documents'.format(auction['data']['id'])
    expected_http_status = '201 Created'
    document = deepcopy(test_document_data)
    url = test_case.generate_docservice_url(),
    document['url'] = url[0]
    request_data = {'data': document}

    response = test_case.app.post_json(entrypoint, request_data)
    test_case.assertEqual(expected_http_status, response.status)

    document = response.json['data']

    pattern = '/auctions/{}/documents/{}'
    entrypoint = pattern.format(auction['data']['id'], document['id'])
    response = test_case.app.get(entrypoint)

    test_case.assertEqual(response.status, '200 OK')


def module_auction_post_audit_without_ds(test_case):

    file_title = 'name.doc'
    file_info = ('file', file_title, 'content')
    response = test_case.app.post(test_case.ENTRYPOINTS['documents'], upload_files=[file_info])

    test_case.assertEqual(response.status, '201 Created')
    test_case.assertEqual(response.content_type, 'application/json')
    doc_id = response.json["data"]['id']
    test_case.assertIn(doc_id, response.headers['Location'])
    test_case.assertEqual(file_title, response.json["data"]["title"])


def module_auction_get_auction_auction(test_case):
    expected_http_status = '200 OK'
    context = test_case.procedure.snapshot(fixture=AUCTION)
    auction = context['auction']
    auction_url = '/auctions/{}/auction'.format(auction['data']['id'])

    response = test_case.app.get(auction_url)

    test_case.assertEqual(response.status, expected_http_status)


def get_auction_urls_dump(test_case):
    context = test_case.procedure.snapshot(fixture=AUCTION_WITH_URLS)
    auction = context['auction']
    bid = context['bids'][0]
    auction_url = '/auctions/{}'.format(auction['data']['id'])

    response = test_case.app.get(auction_url)
    filename = 'docs/source/tutorial/active_auction_auction_url.http'

    test_case.dump(response.request, response, filename)

    bids_entrypoint_pattern = '/auctions/{}/bids/{}?acc_token={}'
    entrypoint = bids_entrypoint_pattern.format(auction['data']['id'], bid['data']['id'], bid['access']['token'])
    auth = test_case.app.authorization
    test_case.app.authorization = ('Basic', ('{}'.format(bid['access']['owner']), ''))
    response = test_case.app.get(entrypoint)
    test_case.app.authorization = auth

    filename = 'docs/source/tutorial/active_auction_participation_urls.http'
    test_case.dump(response.request, response, filename)


@unittest.skipIf(SANDBOX_MODE, 'If sandbox mode is it enabled generating correct periods')
def module_auction_switch_to_qualification(test_case):
    context = test_case.procedure.snapshot(fixture=AUCTION_WITH_URLS)
    auction = context['auction']
    bids = context['bids']
    auction_url = '/auctions/{}/auction'.format(auction['data']['id'])

    # create module auction results
    bid_value = {
        "value": {
            "currency": "UAH",
            "valueAddedTaxIncluded": True
        }
    }
    loser = deepcopy(bid_value)
    loser['id'] = bids[0]['data']['id']
    loser['value']['amount'] = auction['data']['value']['amount']

    winner = deepcopy(bid_value)
    winner['id'] = bids[1]['data']['id']
    winner['value']['amount'] = auction['data']['value']['amount'] + auction['data']['minimalStep']['amount']

    request_data = {'bids': [loser, winner]}

    # get auctionPeriod.startDate
    entrypoint = '/auctions/{}'.format(auction['data']['id'])
    response = test_case.app.get(entrypoint)
    data = response.json['data']
    auction_start_date = parse_date(data['auctionPeriod']['startDate'])

    # simulate valid auction time
    # set 'now' to 14:00 next day of auctionPeriod.startDate
    valid_auction_time = set_specific_hour(auction_start_date + timedelta(days=1), 14)
    with freeze_time(valid_auction_time):
        response = test_case.app.post_json(auction_url, {'data': request_data})
    expected_http_status = '200 OK'
    test_case.assertEqual(response.status, expected_http_status)

    # check generated auction status
    entrypoint = '/auctions/{}'.format(auction['data']['id'])
    response = test_case.app.get(entrypoint)
    test_case.assertEqual(response.json['data']['status'], 'active.qualification')

    # check generated award
    response = test_case.app.get('/auctions/{}/awards'.format(auction['data']['id']))
    awards = response.json['data']
    test_case.assertEqual(len(awards), 1)

    award = awards[0]
    test_case.assertIsNotNone(award.get('verificationPeriod'))
    test_case.assertIsNotNone(award.get('signingPeriod'))
    test_case.assertEqual(award['bid_id'], winner['id'])
    test_case.assertEqual(award['status'], 'pending')

    # check generated verificationPeriod
    entrypoint = '/auctions/{}'.format(auction['data']['id'])
    response = test_case.app.get(entrypoint)
    auction = response.json['data']
    auction_period_end_date = parse_date(auction['auctionPeriod']['endDate'])
    verification_start_date = parse_date(award['verificationPeriod']['startDate'])
    verification_end_date = parse_date(award['verificationPeriod']['endDate'])

    expected_end_date = set_specific_hour(auction_period_end_date, 18)
    test_case.assertEqual(verification_end_date, expected_end_date)

    # check generated signing
    signing_end_date = parse_date(award['signingPeriod']['endDate'])
    signing_start_date = parse_date(award['signingPeriod']['startDate'])

    expected_end_date = ccbd(verification_end_date, timedelta(days=0), specific_hour=23) + timedelta(minutes=59)
    test_case.assertEqual(signing_end_date, expected_end_date)
    test_case.assertEqual(signing_start_date, verification_start_date)

    # check generated awardPeriod
    auction = response.json['data']
    award_period_start = parse_date(auction['awardPeriod']['startDate'])
    test_case.assertEqual(award_period_start, verification_start_date)


@unittest.skipIf(SANDBOX_MODE, 'If sandbox mode is it enabled generating correct periods')
def module_auction_switch_to_qualification_outstanding(test_case):
    context = test_case.procedure.snapshot(fixture=AUCTION_WITH_URLS)
    auction = context['auction']
    bids = context['bids']
    auction_url = '/auctions/{}/auction'.format(auction['data']['id'])

    # create module auction results
    bid_value = {
        "value": {
            "currency": "UAH",
            "valueAddedTaxIncluded": True
        }
    }
    loser = deepcopy(bid_value)
    loser['id'] = bids[0]['data']['id']
    loser['value']['amount'] = auction['data']['value']['amount']

    winner = deepcopy(bid_value)
    winner['id'] = bids[1]['data']['id']
    winner['value']['amount'] = auction['data']['value']['amount'] + auction['data']['minimalStep']['amount']

    request_data = {'bids': [loser, winner]}

    # get auctionPeriod.startDate
    entrypoint = '/auctions/{}'.format(auction['data']['id'])
    response = test_case.app.get(entrypoint)
    data = response.json['data']
    auction_start_date = parse_date(data['auctionPeriod']['startDate'])

    # simulate invalid auction time
    # set 'now' to 19:00 next day of auctionPeriod.startDate
    outstanding_auction_time = set_specific_hour(auction_start_date + timedelta(days=1), 19)
    with freeze_time(outstanding_auction_time):
        response = test_case.app.post_json(auction_url, {'data': request_data})

    response = test_case.app.get('/auctions/{}/awards'.format(auction['data']['id']))
    awards = response.json['data']
    award = awards[0]

    # check generated verificationPeriod
    verification_start_date = parse_date(award['verificationPeriod']['startDate'])
    verification_end_date = parse_date(award['verificationPeriod']['endDate'])
    expected_start_date = set_specific_hour(verification_end_date, 17)
    test_case.assertEqual(verification_start_date, expected_start_date)

    # check generated signing
    signing_end_date = parse_date(award['signingPeriod']['endDate'])
    signing_start_date = parse_date(award['signingPeriod']['startDate'])
    expected_start_date = set_specific_hour(signing_end_date, 17)
    test_case.assertEqual(signing_start_date, expected_start_date)


def module_auction_switch_to_unsuccessful(test_case):
    expected_http_status = '200 OK'
    context = test_case.procedure.snapshot(fixture=AUCTION_WITH_URLS)
    auction = context['auction']
    bids = context['bids']
    auction_url = '/auctions/{}/auction'.format(auction['data']['id'])

    request_data = {
        'bids': [
            {
                "id": bids[0]['data']['id'],
                "value": {
                    "amount": auction['data']['value']['amount'],
                    "currency": "UAH",
                    "valueAddedTaxIncluded": True
                }
            },
            {
                "id": bids[1]['data']['id'],
                "value": {
                    "amount": auction['data']['value']['amount'],
                    "currency": "UAH",
                    "valueAddedTaxIncluded": True
                }
            }
        ]
    }

    # get auctionPeriod.startDate
    entrypoint = '/auctions/{}'.format(auction['data']['id'])
    response = test_case.app.get(entrypoint)
    data = response.json['data']
    auction_start_date = parse_date(data['auctionPeriod']['startDate'])

    # simulate valid auction time
    # set 'now' to 14:00 next day of auctionPeriod.startDate
    valid_auction_time = set_specific_hour(auction_start_date + timedelta(days=1), 14)
    with freeze_time(valid_auction_time):
        response = test_case.app.post_json(auction_url, {'data': request_data})
    test_case.assertEqual(response.status, expected_http_status)

    entrypoint = '/auctions/{}'.format(auction['data']['id'])
    response = test_case.app.get(entrypoint)
    test_case.assertEqual(response.json['data']['status'], 'unsuccessful')


def module_auction_post_result_invalid_number_of_bids(test_case):
    expected_http_status = '422 Unprocessable Entity'
    context = test_case.procedure.snapshot(fixture=AUCTION_WITH_URLS)
    auction = context['auction']
    bids = context['bids']
    auction_url = '/auctions/{}/auction'.format(auction['data']['id'])

    request_data = {
        'bids': [
            {
                "id": bids[0]['data']['id'],
                "value": {
                    "amount": auction['data']['value']['amount'],
                    "currency": "UAH",
                    "valueAddedTaxIncluded": True
                }
            }
        ]
    }

    # get auctionPeriod.startDate
    entrypoint = '/auctions/{}'.format(auction['data']['id'])
    response = test_case.app.get(entrypoint)
    data = response.json['data']
    auction_start_date = parse_date(data['auctionPeriod']['startDate'])

    # simulate valid auction time
    # set 'now' to 14:00 day of auctionPeriod.startDate
    valid_auction_time = set_specific_hour(auction_start_date, 14)
    with freeze_time(valid_auction_time):
        response = test_case.app.post_json(auction_url, {'data': request_data}, status=422)
    test_case.assertEqual(response.status, expected_http_status)


def module_auction_update_auction_urls(test_case):
    context = test_case.procedure.snapshot(fixture=AUCTION)
    expected_http_status = '200 OK'
    request_data = {}
    auction = context['auction']
    bids = context['bids']
    auction_url = '/auctions/{}/auction'.format(auction['data']['id'])

    request_data['auctionUrl'] = u'http://auction-sandbox.openprocurement.org/auctions/{}'.format(auction['data']['id'])
    bids_info = []
    for bid in bids:
        participation_url_pattern = 'http://auction-sandbox.openprocurement.org/auctions/{}?key_for_bid={}'
        bids_info.append({
                "id": bid['data']['id'],
                "participationUrl": participation_url_pattern.format(auction['data']['id'], bid['data']['id'])
            })

    request_data['bids'] = bids_info
    response = test_case.app.patch_json(auction_url, {'data': request_data})
    test_case.assertEqual(response.status, expected_http_status)


def bid_get_participation_urls(test_case):
    context = test_case.procedure.snapshot(fixture=AUCTION_WITH_URLS)
    auction = context['auction']
    bids = context['bids']

    bids_entrypoint_pattern = '/auctions/{}/bids/{}?acc_token={}'
    for bid in bids:

        entrypoint = bids_entrypoint_pattern.format(auction['data']['id'], bid['data']['id'], bid['access']['token'])

        auth = test_case.app.authorization
        test_case.app.authorization = ('Basic', ('{}'.format(bid['access']['owner']), ''))
        response = test_case.app.get(entrypoint)
        test_case.app.authorization = auth

        test_case.assertIsNotNone(response.json['data'].get('participationUrl'))
