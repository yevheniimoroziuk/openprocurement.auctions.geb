from contextlib import nested
from mock import patch
from copy import deepcopy
from iso8601 import parse_date
from datetime import timedelta

from openprocurement.auctions.core.tests.base import (
    test_document_data
)
from openprocurement.auctions.core.utils import (
    set_specific_hour
)

from openprocurement.auctions.geb.tests.fixtures.active_auction import (
    AUCTION as ACTIVE_AUCTION_AUCTION,
    AUCTION_WITH_URLS
)
from openprocurement.auctions.geb.utils import (
    calculate_certainly_business_date as ccbd
)


def post_auction_document_audit(test_case):
    context = test_case.procedure.snapshot(fixture=ACTIVE_AUCTION_AUCTION)
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


def get_auction_auction(test_case):
    expected_http_status = '200 OK'
    context = test_case.procedure.snapshot(fixture=ACTIVE_AUCTION_AUCTION)
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


def switch_to_qualification(test_case):
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
    # set 'now' to 14:00 day of auctionPeriod.startDate
    valid_auction_time = set_specific_hour(auction_start_date, 14)
    with nested(
        patch('openprocurement.auctions.geb.managers.auctioneers.get_now', return_value=valid_auction_time),
        patch('openprocurement.auctions.core.plugins.awarding.base.adapters.get_now', return_value=valid_auction_time),
    ) as (auction_periond_end, award_period_start):
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
    enquiryPeriod_end_date = parse_date(auction['enquiryPeriod']['endDate'])
    verification_start_date = parse_date(award['verificationPeriod']['startDate'])
    verification_end_date = parse_date(award['verificationPeriod']['endDate'])

    expected_end_date = ccbd(enquiryPeriod_end_date, timedelta(days=1), specific_hour=18, working_days=True)
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


def switch_to_qualification_outstanding(test_case):
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
    # set 'now' to 14:00 day of auctionPeriod.startDate
    outstanding_auction_time = set_specific_hour(auction_start_date, 19)
    with nested(
        patch('openprocurement.auctions.geb.managers.auctioneers.get_now', return_value=outstanding_auction_time),
        patch('openprocurement.auctions.core.plugins.awarding.base.adapters.get_now', return_value=outstanding_auction_time),
    ) as (auction_periond_end, award_period_start):
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


def switch_to_unsuccessful(test_case):
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
    # set 'now' to 14:00 day of auctionPeriod.startDate
    valid_auction_time = set_specific_hour(auction_start_date, 14)
    with patch('openprocurement.auctions.geb.managers.auctioneers.get_now', return_value=valid_auction_time):
        response = test_case.app.post_json(auction_url, {'data': request_data})
    test_case.assertEqual(response.status, expected_http_status)

    entrypoint = '/auctions/{}'.format(auction['data']['id'])
    response = test_case.app.get(entrypoint)
    test_case.assertEqual(response.json['data']['status'], 'unsuccessful')


def update_auction_urls(test_case):
    context = test_case.procedure.snapshot(fixture=ACTIVE_AUCTION_AUCTION)
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


def get_participation_urls(test_case):
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
