from iso8601 import parse_date
from copy import deepcopy
from openprocurement.auctions.core.tests.base import (
    test_document_data
)
from openprocurement.auctions.core.utils import (
    get_now
)


def auction_put_auction_document_audit(test_case):
    expected_http_status = '200 OK'
    document = deepcopy(test_document_data)
    url = test_case.generate_docservice_url(),
    document['url'] = url[0]
    request_data = {'data': document}

    response = test_case.app.put_json(test_case.ENTRYPOINTS['auction_audit_put'], request_data)
    test_case.assertEqual(expected_http_status, response.status)

    document = response.json['data']
    pattern = '/auctions/{}/documents/{}'
    entrypoint = pattern.format(test_case.auction['data']['id'], document['id'])
    response = test_case.app.get(entrypoint)
    test_case.assertEqual(response.status, '200 OK')


def organizer_uploads_the_auction_protocol(test_case):
    expected_http_status = '201 Created'
    document = deepcopy(test_document_data)
    document['documentType'] = 'auctionProtocol'
    url = test_case.generate_docservice_url(),
    document['url'] = url[0]

    request_data = {'data': document}
    response = test_case.app.post_json(test_case.ENTRYPOINTS['award_document_post'], request_data)
    test_case.assertEqual(expected_http_status, response.status)

    document = response.json['data']
    pattern = '/auctions/{}/awards/{}/documents/{}'

    entrypoint = pattern.format(test_case.auction['data']['id'],
                                test_case.award['data']['id'],
                                document['id']
                                )
    response = test_case.app.get(entrypoint)
    test_case.assertEqual('200 OK', response.status)


def bid_owner_uploads_the_auction_protocol(test_case):
    expected_http_status = '201 Created'
    document = deepcopy(test_document_data)
    document['documentType'] = 'auctionProtocol'
    url = test_case.generate_docservice_url(),
    document['url'] = url[0]

    request_data = {'data': document}

    auth = test_case.app.authorization
    test_case.app.authorization = ('Basic', ('{}'.format(test_case.bid['access']['owner']), ''))

    response = test_case.app.post_json(test_case.ENTRYPOINTS['award_document_post'], request_data)
    test_case.assertEqual(expected_http_status, response.status)

    document = response.json['data']
    pattern = '/auctions/{}/awards/{}/documents/{}'

    entrypoint = pattern.format(test_case.auction['data']['id'],
                                test_case.award['data']['id'],
                                document['id']
                                )
    response = test_case.app.get(entrypoint)

    test_case.app.authorization = auth
    test_case.assertEqual('200 OK', response.status)


def organizer_activate_award(test_case):
    expected_http_status = '200 OK'

    request_data = {"data": {"status": "active"}}

    auth = test_case.app.authorization
    test_case.app.authorization = ('Basic', ('{}'.format(test_case.bid['access']['owner']), ''))
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['award_patch'], request_data)
    test_case.app.authorization = auth
    test_case.assertEqual(expected_http_status, response.status)

    response = test_case.app.get(test_case.ENTRYPOINTS['award_get'])
    now = get_now().replace(second=0, microsecond=0)
    award = response.json['data']

    # check award verificationPeriod end
    end_date = parse_date(award['verificationPeriod']['endDate']).replace(second=0, microsecond=0)
    test_case.assertEqual(end_date, now)

    # check award complaint end

    end_date = parse_date(award['complaintPeriod']['endDate']).replace(second=0, microsecond=0)
    test_case.assertEqual(end_date, now)

    # check contract

    response = test_case.app.get(test_case.ENTRYPOINTS['contracts_get'])
    contracts = response.json['data']
    test_case.assertEqual(len(contracts), 1)
    contract = contracts[0]

    test_case.assertEqual(contract['status'], 'pending')

    # check auction status
    response = test_case.app.get(test_case.ENTRYPOINTS['auction_get'])
    auction = response.json['data']

    test_case.assertEqual(auction['status'], 'active.awarded')

    # check auction awardPeriod end

    end_date = parse_date(auction['awardPeriod']['endDate']).replace(second=0, microsecond=0)
    test_case.assertEqual(end_date, now)
