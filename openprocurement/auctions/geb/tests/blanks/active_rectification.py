from copy import deepcopy

from openprocurement.auctions.geb.tests.fixtures.common import (
    # test_item,
    test_procuringEntity,
    test_lotHolder,
    test_bankAccount,
    test_contractTerms,
    test_question_data
)
from openprocurement.auctions.geb.tests.fixtures.active_rectification import (
    ACTIVE_RECTIFICATION_AUCTION_DEFAULT_FIXTURE,
    ACTIVE_RECTIFICATION_AUCTION_WITH_DOCUMENTS
)

from openprocurement.auctions.core.tests.base import (
    test_document_data
)


def change_title(test_case):
    new_title = 'New Title'
    field = "title"

    request_data = {"data": {field: new_title}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data)

    test_case.assertEqual(new_title, response.json['data'][field])


def change_one_field_rest_same(test_case):
    new_title = 'Test'
    field = "title"

    all_data = deepcopy(ACTIVE_RECTIFICATION_AUCTION_DEFAULT_FIXTURE)
    request_data = {"data": all_data}
    request_data['data'][field] = new_title
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data)

    test_case.assertEqual(new_title, response.json['data'][field])


def change_title_dump(test_case):
    new_title = 'Test'
    field = "title"

    request_data = {"data": {field: new_title}}
    response = test_case.app.patch_json(test_case.ENTRYPOINT, request_data)

    filename = 'docs/source/tutorial/active_rectification_change_title.http'
    test_case.dump(response.request, response, filename)


def change_desctiption(test_case):
    new = 'Test'
    field = "description"

    request_data = {"data": {field: new}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])

    response = test_case.app.get(test_case.ENTRYPOINTS['get_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])


def change_tenderAttempts(test_case):
    field = "tenderAttempts"
    new = 2

    request_data = {"data": {field: new}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])

    response = test_case.app.get(test_case.ENTRYPOINTS['get_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])


def change_lotIdentifier(test_case):
    new = '123456'
    field = "lotIdentifier"

    request_data = {"data": {field: new}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])

    response = test_case.app.get(test_case.ENTRYPOINTS['get_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])


def change_value(test_case):
    new = {u'currency': u'UAH', u'amount': 42.0, u'valueAddedTaxIncluded': True}
    field = "value"

    request_data = {"data": {field: new}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])

    response = test_case.app.get(test_case.ENTRYPOINTS['get_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])


def change_minimalStep(test_case):
    new = {u'currency': u'UAH', u'amount': 90.0, u'valueAddedTaxIncluded': True}
    field = "minimalStep"

    request_data = {"data": {field: new}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])

    response = test_case.app.get(test_case.ENTRYPOINTS['get_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])


def change_guarantee(test_case):
    new = {u'currency': u'UAH', u'amount': 42.0}
    field = "guarantee"

    request_data = {"data": {field: new}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])

    response = test_case.app.get(test_case.ENTRYPOINTS['get_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])


def change_items(test_case):
    pass
#    item = deepcopy(test_item)
#    new = 42
#    field = "quantity"
#    item[field] = new
#
#    import ipdb; ipdb.set_trace()  # XXX BREAKPOINT
#    request_data = {"data": {['items': [new]}}
#    response = test_case.app.patch_json(test_case.ENTRYPOINT, request_data)
#    test_case.assertEqual(response.json['data'][field][0]['quantity'], new['quantity'])
#
#    auction_entrypoint = '/auctions/{}'.format(test_case.auction['data']['id'])
#    response = test_case.app.get(auction_entrypoint, request_data)
#    test_case.assertEqual([new], response.json['data']['items'][field])


def change_budgetSpent(test_case):
    new = {u'currency': u'UAH', u'amount': 42.0, u'valueAddedTaxIncluded': True}
    field = "budgetSpent"

    request_data = {"data": {field: new}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])

    response = test_case.app.get(test_case.ENTRYPOINTS['get_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])


def change_registrationFee(test_case):
    new = {u'currency': u'UAH', u'amount': 800.0, u'valueAddedTaxIncluded': True}
    field = "registrationFee"

    request_data = {"data": {field: new}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])

    response = test_case.app.get(test_case.ENTRYPOINTS['get_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])


def change_procuringEntity(test_case):
    procuringEntity = deepcopy(test_procuringEntity)
    procuringEntity['name'] = 'Test'
    new = procuringEntity
    field = "procuringEntity"

    request_data = {"data": {field: new}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])

    response = test_case.app.get(test_case.ENTRYPOINTS['get_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])


def change_lotHolder(test_case):
    lotHolder = deepcopy(test_lotHolder)
    lotHolder['name'] = 'Test'
    new = lotHolder
    field = "lotHolder"

    request_data = {"data": {field: new}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])

    response = test_case.app.get(test_case.ENTRYPOINTS['get_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])


def change_bankAccount(test_case):
    bankAccount = deepcopy(test_bankAccount)
    bankAccount['bankName'] = u'Test'
    new = bankAccount
    field = "bankAccount"

    request_data = {"data": {field: new}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])

    response = test_case.app.get(test_case.ENTRYPOINTS['get_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])


def change_contractTerms(test_case):
    contractTerms = deepcopy(test_contractTerms)
    contractTerms['leaseTerms']['leaseDuration'] = u'P20Y'
    new = contractTerms
    field = "contractTerms"

    request_data = {"data": {field: new}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])

    auction_entrypoint = '/auctions/{}'.format(test_case.auction['data']['id'])
    response = test_case.app.get(auction_entrypoint, request_data)
    test_case.assertEqual(new, response.json['data'][field])


def add_document(test_case):
    context = test_case.procedure.snapshot()
    auction = context['auction']

    entrypoint_pattern = '/auctions/{}/documents?acc_token={}'
    entrypoint = entrypoint_pattern.format(auction['data']['id'], auction['access']['token'])

    document = deepcopy(test_document_data)
    url = test_case.generate_docservice_url(),
    document['url'] = url[0]
    document['documentType'] = 'technicalSpecifications'
    expected_http_status = '201 Created'

    request_data = {'data': document}
    response = test_case.app.post_json(entrypoint, request_data)
    test_case.assertEqual(expected_http_status, response.status)


def patch_document(test_case):
    context = test_case.procedure.snapshot(fixture=ACTIVE_RECTIFICATION_AUCTION_WITH_DOCUMENTS)
    auction = context['auction']
    document = context['documents'][0]
    field = 'documentType'
    new = 'technicalSpecifications'

    entrypoint_pattern = '/auctions/{}/documents/{}?acc_token={}'
    entrypoint = entrypoint_pattern.format(auction['data']['id'], document['data']['id'], auction['access']['token'])
    request_data = {'data': {field: new}}

    response = test_case.app.patch_json(entrypoint, request_data)
    document = response.json['data']

    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(document[field], new)

    response = test_case.app.get(entrypoint)
    document = response.json['data']
    test_case.assertEqual(document[field], new)


def add_document_dump(test_case):
    document = deepcopy(test_document_data)
    url = test_case.generate_docservice_url(),
    document['url'] = url[0]

    request_data = {'data': document}
    response = test_case.app.post_json(test_case.ENTRYPOINT, request_data)

    filename = 'docs/source/tutorial/active_rectification_add_document.http'
    test_case.dump(response.request, response, filename)


def add_question(test_case):
    expected_http_status = '201 Created'

    request_data = test_question_data
    response = test_case.app.post_json(test_case.ENTRYPOINTS['post_question'], request_data)
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

    request_data = {"data": {"answer": "Test answer"}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_question'], request_data)

    test_case.assertEqual(response.status, expected_http_status)


def get_question(test_case):
    expected_http_status = '200 OK'

    response = test_case.app.get(test_case.ENTRYPOINTS['question'])

    test_case.assertEqual(response.status, expected_http_status)
