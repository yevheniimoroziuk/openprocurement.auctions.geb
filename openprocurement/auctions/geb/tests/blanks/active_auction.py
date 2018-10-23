
from openprocurement.auctions.geb.tests.fixtures.active_auction import (
    AUCTION as ACTIVE_AUCTION_AUCTION,
    AUCTION_WITH_URLS
)


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
                    "amount": auction['data']['value']['amount'] + auction['data']['minimalStep']['amount'],
                    "currency": "UAH",
                    "valueAddedTaxIncluded": True
                }
            }
        ]
    }
    response = test_case.app.post_json(auction_url, {'data': request_data})
    test_case.assertEqual(response.status, expected_http_status)

    entrypoint = '/auctions/{}'.format(auction['data']['id'])
    response = test_case.app.get(entrypoint)
    test_case.assertEqual(response.json['data']['status'], 'active.qualification')


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
