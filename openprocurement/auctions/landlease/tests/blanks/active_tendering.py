from copy import deepcopy
from openprocurement.auctions.core.tests.base import (
    test_document_data,
)
from openprocurement.auctions.landlease.tests.fixtures import (
    test_question_data,
    test_bid_data
)
from openprocurement.auctions.landlease.tests.helpers import (
    create_question,
    get_errors_names
)


def add_document(test_case):
    document = deepcopy(test_document_data)
    url = test_case.generate_docservice_url(),
    document['url'] = url[0]
    expected_http_status = '201 Created'

    request_data = {'data': document}
    response = test_case.app.post_json(test_case.entrypoint, request_data)
    test_case.assertEqual(expected_http_status, response.status)


def add_question(test_case):
    expected_http_status = '201 Created'

    request_data = test_question_data
    response = test_case.app.post_json(test_case.entrypoint, request_data)
    test_case.assertEqual(response.status, expected_http_status)


def answer_question(test_case):
    expected_http_status = '200 OK'

    question = create_question(test_case, test_case.auction)
    entrypoint = '/auctions/{}/questions/{}?acc_token={}'.format(test_case.auction['id'],
                                                                 question['id'],
                                                                 test_case.auction_token)

    request_data = {"data": {"answer": "Test answer"}}
    response = test_case.app.patch_json(entrypoint, request_data)
    test_case.assertEqual(response.status, expected_http_status)


def add_bid(test_case):
    expected_http_status = '201 Created'

    request_data = test_bid_data
    response = test_case.app.post_json(test_case.ENTRYPOINTS['create_bid'], request_data)
    test_case.assertEqual(response.status, expected_http_status)


def add_invalid_bid(test_case):
    expected_http_status = '422 Unprocessable Entity'
    expected_error = 'value'

    invalid_bid = deepcopy(test_bid_data)
    invalid_bid['data']['value']['amount'] = 42
    request_data = invalid_bid
    response = test_case.app.post_json(test_case.ENTRYPOINTS['create_bid'], request_data, status=422)
    errors = get_errors_names(response)
    test_case.assertEqual(response.status, expected_http_status)
    test_case.assertIn(expected_error, errors)

    invalid_bid = deepcopy(test_bid_data)
    invalid_bid['data']['value']['currency'] = 'BTC'
    request_data = invalid_bid
    response = test_case.app.post_json(test_case.ENTRYPOINTS['create_bid'], request_data, status=422)
    errors = get_errors_names(response)
    test_case.assertEqual(response.status, expected_http_status)
    test_case.assertIn(expected_error, errors)

    invalid_bid = deepcopy(test_bid_data)
    invalid_bid['data']['value']['valueAddedTaxIncluded'] = False
    request_data = invalid_bid
    response = test_case.app.post_json(test_case.ENTRYPOINTS['create_bid'], request_data, status=422)
    errors = get_errors_names(response)
    test_case.assertEqual(response.status, expected_http_status)
    test_case.assertIn(expected_error, errors)


def add_document_to_bid(test_case):
    document = deepcopy(test_document_data)
    url = test_case.generate_docservice_url(),
    document['url'] = url[0]
    expected_http_status = '201 Created'

    request_data = {'data': document}
    response = test_case.app.post_json(test_case.ENTRYPOINTS['add_document'], request_data)
    test_case.assertEqual(expected_http_status, response.status)


def activate_bid(test_case):
    expected_http_status = '200 OK'
    expected_data = ['date', 'owner', 'id', 'qualified', 'value', 'status', 'tenderers']

    request_data = {"data": {"status": "pending"}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_bid'], request_data)
    test_case.assertEqual(expected_http_status, response.status)
    test_case.assertSetEqual(set(expected_data), set(response.json['data'].keys()))


def make_active_status_bid(test_case):
    expected_http_status = '200 OK'

    request_data = {"data": {"status": "pending"}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_bid'], request_data)


    import ipdb; ipdb.set_trace()  # XXX BREAKPOINT
    request_data = {"data": {"status": "active"}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_bid'], request_data)
    test_case.assertEqual(expected_http_status, response.status)

