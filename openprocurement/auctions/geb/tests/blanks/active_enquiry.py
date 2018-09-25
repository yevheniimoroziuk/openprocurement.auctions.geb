
from copy import deepcopy
from openprocurement.auctions.core.tests.base import (
    test_document_data,
)
from openprocurement.auctions.geb.tests.fixtures.common import (
    test_question_data,
    test_bid_data
)


def add_document(test_case):
    document = deepcopy(test_document_data)
    url = test_case.generate_docservice_url(),
    document['url'] = url[0]
    expected_http_status = '201 Created'

    request_data = {'data': document}
    response = test_case.app.post_json(test_case.ENTRYPOINTS['documents'], request_data)
    test_case.assertEqual(expected_http_status, response.status)


def add_question(test_case):
    expected_http_status = '201 Created'

    request_data = test_question_data
    response = test_case.app.post_json(test_case.ENTRYPOINTS['questions'], request_data)
    test_case.assertEqual(response.status, expected_http_status)

    question = response.json['data']

    question_url_pattern = '/auctions/{auction}/questions/{question}'
    question_url = question_url_pattern.format(auction=test_case.auction['data']['id'],
                                               question=question['id'])

    response = test_case.app.get(question_url)
    test_case.assertEqual(response.status, '200 OK')


def answer_question(test_case):
    expected_http_status = '200 OK'

    entrypoint = '/auctions/{}/questions/{}?acc_token={}'.format(test_case.auction['data']['id'],
                                                                 test_case.questions[0]['data']['id'],
                                                                 test_case.auction['access']['token'])

    request_data = {"data": {"answer": "Test answer"}}
    response = test_case.app.patch_json(entrypoint, request_data)
    test_case.assertEqual(response.status, expected_http_status)


def get_question(test_case):
    expected_http_status = '200 OK'
    question = test_case.questions[0]
    question_url_pattern = '/auctions/{auction}/questions/{question}'
    question_url = question_url_pattern.format(auction=test_case.auction['data']['id'],
                                               question=question['data']['id'])
    response = test_case.app.get(question_url)
    test_case.assertEqual(response.status, expected_http_status)


def add_bid(test_case):
    expected_http_status = '403 Forbidden'

    request_data = test_bid_data
    response = test_case.app.post_json(test_case.ENTRYPOINTS['bids'], request_data, status=403)
    test_case.assertEqual(response.status, expected_http_status)


def get_bid(test_case):
    expected_http_status = '200 OK'
    bid = test_case.bids[0]
    bid_url_pattern = '/auctions/{auction}/bids/{bid}?acc_token={token}'
    bid_url = bid_url_pattern.format(auction=test_case.auction['data']['id'],
                                     bid=bid['data']['id'],
                                     token=bid['access']['token'])

    response = test_case.app.get(bid_url)
    test_case.assertEqual(response.status, expected_http_status)


def add_bid_document(test_case):
    document = deepcopy(test_document_data)
    url = test_case.generate_docservice_url(),
    document['url'] = url[0]
    expected_http_status = '201 Created'
    add_bid_document_url_pattern = '/auctions/{auction}/bids/{bid}/documents?acc_token={token}'
    bid = test_case.bids[0]
    add_bid_document_url = add_bid_document_url_pattern.format(auction=test_case.auction['data']['id'],
                                                               bid=bid['data']['id'],
                                                               token=bid['access']['token'])

    request_data = {'data': document}
    response = test_case.app.post_json(add_bid_document_url, request_data)
    test_case.assertEqual(expected_http_status, response.status)

    entrypoint = '/auctions/{}/bids/{}/documents/{}?acc_token={}'.format(test_case.auction['data']['id'],
                                                                         bid['data']['id'],
                                                                         response.json['data']['id'],
                                                                         bid['access']['token'])
    response = test_case.app.get(entrypoint)
    test_case.assertEqual('200 OK', response.status)


def delete_bid(test_case):
    expected_http_status = '200 OK'

    bid_url_pattern = '/auctions/{auction}/bids/{bid}?acc_token={token}'
    bid = test_case.bids[0]
    bid_url = bid_url_pattern.format(auction=test_case.auction['data']['id'],
                                     bid=bid['data']['id'],
                                     token=bid['access']['token'])

    test_case.app.get(bid_url)
    response = test_case.app.delete_json(bid_url)

    test_case.app.get(bid_url, status=404)
    test_case.assertEqual(expected_http_status, response.status)


def make_active_status_bid(test_case):
    expected_http_status = '200 OK'

    document = deepcopy(test_document_data)
    document['documentType'] = 'eligibilityDocuments'
    url = test_case.generate_docservice_url(),
    document['url'] = url[0]
    patch_bid_url_pattern = '/auctions/{auction}/bids/{bid}?acc_token={token}'
    add_bid_document_url_pattern = '/auctions/{auction}/bids/{bid}/documents?acc_token={token}'

    bid = [bid for bid in test_case.bids if bid['data']['status'] == 'pending'][0]

    patch_bid_url = patch_bid_url_pattern.format(auction=test_case.auction['data']['id'],
                                                 bid=bid['data']['id'],
                                                 token=bid['access']['token'])

    add_bid_document_url = add_bid_document_url_pattern.format(auction=test_case.auction['data']['id'],
                                                               bid=bid['data']['id'],
                                                               token=bid['access']['token'])

    request_data = {"data": {"status": "active"}}
    response = test_case.app.patch_json(patch_bid_url, request_data, status=403)
    test_case.assertEqual('403 Forbidden', response.status)

    request_data = {'data': document}
    response = test_case.app.post_json(add_bid_document_url, request_data)

    request_data = {"data": {"status": "active"}}
    response = test_case.app.patch_json(patch_bid_url, request_data, status=403)
    test_case.assertEqual('403 Forbidden', response.status)

    request_data = {"data": {"qualified": True}}
    response = test_case.app.patch_json(patch_bid_url, request_data)
    test_case.assertEqual(expected_http_status, response.status)

    request_data = {"data": {"status": "active"}}
    response = test_case.app.patch_json(patch_bid_url, request_data, status=403)
    test_case.assertEqual('403 Forbidden', response.status)

    request_data = {"data": {"bidNumber": 1}}
    response = test_case.app.patch_json(patch_bid_url, request_data)
    test_case.assertEqual(expected_http_status, response.status)

    request_data = {"data": {"status": "active"}}
    response = test_case.app.patch_json(patch_bid_url, request_data)
    test_case.assertEqual(expected_http_status, response.status)
