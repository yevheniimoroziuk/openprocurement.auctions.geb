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


def dump_organizer_upload_auction_protocol(test_case):
    document = deepcopy(test_document_data)
    document['documentType'] = 'auctionProtocol'
    url = test_case.generate_docservice_url(),
    document['url'] = url[0]

    request_data = {'data': document}
    response = test_case.app.post_json(test_case.ENTRYPOINTS['award_document_post'], request_data)

    filename = 'docs/source/tutorial/active_qualification_organizer_upload_protocol.http'
    test_case.dump(response.request, response, filename)


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


def dump_bid_owner_upload_auction_protocol(test_case):
    document = deepcopy(test_document_data)
    document['documentType'] = 'auctionProtocol'
    url = test_case.generate_docservice_url(),
    document['url'] = url[0]

    request_data = {'data': document}

    auth = test_case.app.authorization
    test_case.app.authorization = ('Basic', ('{}'.format(test_case.bid['access']['owner']), ''))

    response = test_case.app.post_json(test_case.ENTRYPOINTS['award_document_post'], request_data)

    filename = 'docs/source/tutorial/active_qualification_bid_owner_upload_protocol.http'
    test_case.dump(response.request, response, filename)

    test_case.app.authorization = auth


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


def organizer_rejection_award(test_case):
    # organizer can reject award only if award status 'pending'

    auth = test_case.app.authorization

    # auth as auction owner
    test_case.app.authorization = ('Basic', ('{}'.format(test_case.auction['access']['owner']), ''))

    # try to reject award
    request_data = {"data": {"status": "unsuccessful"}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['award_patch'],
                                        request_data,
                                        status=403)
    # get 403 because, need to upload rejection protocol(document) before patch status
    test_case.assertEqual(response.status, '403 Forbidden')

    # upload rejection protocol
    document = deepcopy(test_document_data)
    document['documentType'] = 'rejectionProtocol'
    url = test_case.generate_docservice_url(),
    document['url'] = url[0]

    request_data = {'data': document}
    response = test_case.app.post_json(test_case.ENTRYPOINTS['award_document_post'], request_data)

    # try to reject award
    request_data = {"data": {"status": "unsuccessful"}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['award_patch'], request_data)

    # check auction
    response = test_case.app.get(test_case.ENTRYPOINTS['auction_get'], request_data)
    auction = response.json['data']

    test_case.assertEqual(auction['status'], 'unsuccessful')

    # check award
    response = test_case.app.get(test_case.ENTRYPOINTS['award_get'], request_data)
    award = response.json['data']

    test_case.assertEqual(award['status'], 'unsuccessful')

    test_case.app.authorization = auth


def dump_organizer_activate_award(test_case):
    document = deepcopy(test_document_data)
    document['documentType'] = 'auctionProtocol'
    url = test_case.generate_docservice_url(),
    document['url'] = url[0]

    request_data = {'data': document}
    test_case.app.post_json(test_case.ENTRYPOINTS['award_document_post'], request_data)

    auth = test_case.app.authorization
    request_data = {"data": {"status": "active"}}
    test_case.app.authorization = ('Basic', ('{}'.format(test_case.bid['access']['owner']), ''))
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['award_patch'], request_data)
    test_case.app.authorization = auth

    filename = 'docs/source/tutorial/active_qualification_activate_award.http'
    test_case.dump(response.request, response, filename)

    # current award
    response = test_case.app.get(test_case.ENTRYPOINTS['award_get'])

    filename = 'docs/source/tutorial/active_qualification_award_after_activation.http'
    test_case.dump(response.request, response, filename)

    # current contract
    response = test_case.app.get(test_case.ENTRYPOINTS['contracts_get'])

    filename = 'docs/source/tutorial/active_qualification_contract_after_activation.http'
    test_case.dump(response.request, response, filename)

    # current auction
    response = test_case.app.get(test_case.ENTRYPOINTS['auction_get'])

    filename = 'docs/source/tutorial/active_qualification_auction_after_activation.http'
    test_case.dump(response.request, response, filename)


def bid_get(test_case):
    # in auction status 'active.qualification'
    # anybody can get bid without access token

    expected_http_status = '200 OK'
    expected_data = (
        'id',
        'status',
        'tenderers',
        'value',
        'date',
        'id',
        'owner',
        'qualified',
        'bidNumber',
        'documents',
        'participationUrl'

    )
    response = test_case.app.get(test_case.ENTRYPOINTS['bid_get'])
    test_case.assertEqual(expected_http_status, response.status)
    bid = response.json['data']
    test_case.assertEqual(set(bid.keys()), set(expected_data))
