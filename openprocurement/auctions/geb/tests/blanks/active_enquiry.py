
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

    auction_entrypoint = '/auctions/{}'.format(test_case.auction['data']['id'])
    response = test_case.app.get(auction_entrypoint)
    auction = response.json['data']
    questions = [question['id'] for question in auction['questions']]
    test_case.assertIn(question['id'], questions)

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


def bid_add(test_case):
    expected_http_status = '403 Forbidden'

    request_data = test_bid_data
    response = test_case.app.post_json(test_case.ENTRYPOINTS['bids'], request_data, status=403)
    test_case.assertEqual(response.status, expected_http_status)


def bid_add_document_in_pending_status(test_case):
    document = deepcopy(test_document_data)
    url = test_case.generate_docservice_url(),
    document['url'] = url[0]
    expected_http_status = '201 Created'

    request_data = {'data': document}
    response = test_case.app.post_json(test_case.ENTRYPOINTS['add_bid_document'], request_data)
    test_case.assertEqual(expected_http_status, response.status)


def bid_add_document_in_active_status(test_case):
    document = deepcopy(test_document_data)
    url = test_case.generate_docservice_url(),
    document['url'] = url[0]
    expected_http_status = '201 Created'

    request_data = {'data': document}
    response = test_case.app.post_json(test_case.ENTRYPOINTS['add_bid_document'], request_data)
    test_case.assertEqual(expected_http_status, response.status)


def bid_delete_in_pending_status(test_case):
    expected_http_status = '200 OK'
    response = test_case.app.delete_json(test_case.ENTRYPOINTS['bid'])
    test_case.assertEqual(expected_http_status, response.status)

    expected_http_status = '404 Not Found'
    response = test_case.app.get(test_case.ENTRYPOINTS['bid'], status=404)
    test_case.assertEqual(expected_http_status, response.status)


def bid_delete_in_active_status(test_case):
    expected_http_status = '200 OK'
    response = test_case.app.delete_json(test_case.ENTRYPOINTS['bid'])
    test_case.assertEqual(expected_http_status, response.status)

    expected_http_status = '404 Not Found'
    response = test_case.app.get(test_case.ENTRYPOINTS['bid'], status=404)
    test_case.assertEqual(expected_http_status, response.status)


def bid_patch_in_pending_status(test_case):
    auth = test_case.app.authorization

    test_case.app.authorization = ('Basic', ('{}'.format(test_case.bid['access']['owner']), ''))

    expected_http_status = '403 Forbidden'
    request_data = {"data": {"status": "draft"}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['bid'], request_data, status=403)
    test_case.assertEqual(expected_http_status, response.status)

    request_data = {"data": {"status": "active"}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['bid'], request_data, status=403)
    test_case.assertEqual(expected_http_status, response.status)

    expected_http_status = '200 OK'
    request_data = {"data": {'qualified': True}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['bid'], request_data)
    test_case.assertEqual(expected_http_status, response.status)

    test_case.app.authorization = auth


def bid_patch_in_active_status(test_case):
    auth = test_case.app.authorization

    test_case.app.authorization = ('Basic', ('{}'.format(test_case.bid['access']['owner']), ''))

    expected_http_status = '403 Forbidden'
    request_data = {"data": {"status": "pending"}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['bid'], request_data, status=403)
    test_case.assertEqual(expected_http_status, response.status)

    test_case.app.authorization = auth


def bid_get_in_pending_status(test_case):
    auth = test_case.app.authorization

    test_case.app.authorization = ('Basic', ('{}'.format(test_case.bid['access']['owner']), ''))

    expected_http_status = '200 OK'
    response = test_case.app.get(test_case.ENTRYPOINTS['bid'])
    test_case.assertEqual(expected_http_status, response.status)

    test_case.app.authorization = auth


def bid_get_in_active_status(test_case):
    auth = test_case.app.authorization

    test_case.app.authorization = ('Basic', ('{}'.format(test_case.bid['access']['owner']), ''))

    expected_http_status = '200 OK'
    response = test_case.app.get(test_case.ENTRYPOINTS['bid'])
    test_case.assertEqual(expected_http_status, response.status)

    test_case.app.authorization = auth


def bid_make_activate(test_case):
    document = deepcopy(test_document_data)
    document['documentType'] = 'eligibilityDocuments'
    url = test_case.generate_docservice_url(),
    document['url'] = url[0]

    request_data = {'data': document}
    response = test_case.app.post_json(test_case.ENTRYPOINTS['add_bid_document'], request_data)

    request_data = {"data": {"status": "active"}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['bid'], request_data, status=403)
    test_case.assertEqual('403 Forbidden', response.status)

    request_data = {"data": {"qualified": True}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['bid'], request_data)

    request_data = {"data": {"status": "active"}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['bid'], request_data, status=403)
    test_case.assertEqual('403 Forbidden', response.status)

    request_data = {"data": {"bidNumber": 1}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['bid'], request_data)

    request_data = {"data": {"status": "active"}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['bid'], request_data)
    test_case.assertEqual('200 OK', response.status)

    response = test_case.app.get(test_case.ENTRYPOINTS['bid'])
    bid = response.json['data']
    test_case.assertEqual('active', bid['status'])
