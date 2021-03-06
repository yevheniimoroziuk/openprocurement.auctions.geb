# -*- coding: utf-8 -*-
from copy import deepcopy

from openprocurement.auctions.core.tests.base import (
    test_document_data,
    test_organization
)
from openprocurement.auctions.geb.tests.fixtures.common import (
    test_question_data,
    test_bid_data
)


def auction_patch(test_case):
    new_data = {}

    field = "title"
    new_value = 'New Title'
    new_data[field] = new_value

    field = "bankAccount"
    new_value = {
        "bankName": "New Test bank name",
        "description": u"Test Bank Account",
        "accountIdentification": [{
            "scheme": u'UA-EDR',
            "id": u"66113000-5",
            "description": u"Test"
        }]
    }
    new_data[field] = new_value

    field = "budgetSpent"
    new_value = {
        "amount": 42,
        "currency": u"UAH"
    }
    new_data[field] = new_value

    field = "contractTerms"
    new_value = {
        "type": "lease",
        "leaseTerms": {
            "leaseDuration": "P11Y",
        }
    }
    new_data[field] = new_value

    field = "description"
    new_value = 'New description'
    new_data[field] = new_value

    field = "guarantee"
    new_value = {
        "amount": 42,
        "currency": u"UAH"
    }
    new_data[field] = new_value

    field = "guarantee"
    new_value = {
        "amount": 42,
        "currency": u"UAH"
    }

    field = "lotHolder"
    new_lotHolder = test_organization.copy()
    new_lotHolder['name'] = 'New Name'
    new_value = new_lotHolder
    new_data[field] = new_value

    field = "lotIdentifier"
    new_value = "219570"
    new_data[field] = new_value

    field = "minimalStep"
    new_value = {
        "amount": 42,
        "currency": u"UAH"
    }

    field = "procuringEntity"
    new_procuringEntity = test_organization.copy()
    new_procuringEntity['name'] = 'New Name'
    new_value = new_procuringEntity
    new_data[field] = new_value

    field = "registrationFee"
    new_value = {
        "amount": 703,
        "currency": u"UAH"
    }
    new_data[field] = new_value

    field = "tenderAttempts"
    new_value = 2
    new_data[field] = new_value

    field = "value"
    new_value = {
        "amount": 123,
        "currency": u"UAH"
    }
    new_data[field] = new_value

    request_data = {"data": new_data}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data, status=403)
    errors = response.json.get('errors')
    test_case.assertIsNotNone(errors)

    # ceck if field don`t change
    response = test_case.app.get(test_case.ENTRYPOINTS['get_auction'])
    auction = response.json['data']

    for field, value in new_data.items():
        recieve_field = auction[field]
        test_case.assertNotEqual(recieve_field, new_data[field])


def auction_document_post(test_case):
    expected_http_status = '201 Created'
    document = deepcopy(test_document_data)
    document.pop('hash')
    document['accessDetails'] = 'test accessDetails'
    document['documentType'] = 'x_dgfAssetFamiliarization'

    request_data = {'data': document}
    response = test_case.app.post_json(test_case.ENTRYPOINTS['documents'], request_data)
    test_case.assertEqual(expected_http_status, response.status)


def auction_document_post_offline(test_case):
    expected_http_status = '201 Created'
    document = deepcopy(test_document_data)
    auction_documents_type = [
        'technicalSpecifications',
        'evaluationCriteria',
        'clarifications',
        'billOfQuantity',
        'conflictOfInterest',
        'evaluationReports',
        'complaints',
        'eligibilityCriteria',
        'tenderNotice',
        'illustration',
        'x_financialLicense',
        'x_virtualDataRoom',
        'x_presentation',
        'x_nda',
        'x_qualificationDocuments',
        'cancellationDetails',
    ]
    init_document = deepcopy(test_document_data)
    url = test_case.generate_docservice_url(),
    init_document['url'] = url[0]
    for doc_type in auction_documents_type:
        document = deepcopy(init_document)
        document['documentType'] = doc_type

        request_data = {'data': document}
    response = test_case.app.post_json(test_case.ENTRYPOINTS['documents'], request_data)
    test_case.assertEqual(expected_http_status, response.status)


def auction_document_patch(test_case):
    field = 'documentType'
    new = 'technicalSpecifications'

    request_data = {'data': {field: new}}

    response = test_case.app.patch_json(test_case.ENTRYPOINTS['document_patch'], request_data)
    document = response.json['data']

    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(document[field], new)

    response = test_case.app.get(test_case.ENTRYPOINTS['document_get'])
    document = response.json['data']
    test_case.assertEqual(document[field], new)


def auction_document_download(test_case):
    # get document data
    response = test_case.app.get(test_case.ENTRYPOINTS['document_get'])
    document_data = response.json['data']

    # get document key
    key = document_data["url"].split('?')[-1]

    # download document
    entrypoint_pattern = '/auctions/{}/documents/{}?download={}'
    entrypoint = entrypoint_pattern.format(test_case.auction['data']['id'],
                                           test_case.document['data']['id'],
                                           key)
    response = test_case.app.get(entrypoint)

    test_case.assertEqual(response.content_type, 'application/msword')


def auction_document_put(test_case):
    new_document = deepcopy(test_document_data)
    new_title = 'Title for new Document'
    url = test_case.generate_docservice_url(),
    new_document['url'] = url[0]
    new_document['title'] = new_title

    request_data = {'data': new_document}

    response = test_case.app.put_json(test_case.ENTRYPOINTS['document_put'], request_data)

    test_case.assertEqual(response.status, '200 OK')

    response = test_case.app.get(test_case.ENTRYPOINTS['document_get'])
    document = response.json['data']
    test_case.assertEqual(document['title'], new_title)


def auction_document_put_offline(test_case):
    new_document = deepcopy(test_document_data)
    new_title = 'Title for new Offline Document'
    new_access_details = 'New Access details'

    new_document.pop('hash')
    new_document['title'] = new_title
    new_document['accessDetails'] = new_access_details
    new_document['format'] = 'offline/on-site-examination'
    new_document['documentType'] = 'x_dgfAssetFamiliarization'

    request_data = {'data': new_document}

    response = test_case.app.put_json(test_case.ENTRYPOINTS['document_put'], request_data)

    test_case.assertEqual(response.status, '200 OK')

    response = test_case.app.get(test_case.ENTRYPOINTS['document_get'])
    document = response.json['data']
    test_case.assertEqual(document['title'], new_title)
    test_case.assertEqual(document['accessDetails'], new_access_details)


def auction_document_post_without_ds(test_case):

    file_title = 'name.doc'
    file_info = ('file', file_title, 'content')
    response = test_case.app.post(test_case.ENTRYPOINTS['documents'], upload_files=[file_info])

    test_case.assertEqual(response.status, '201 Created')
    test_case.assertEqual(response.content_type, 'application/json')
    doc_id = response.json["data"]['id']
    test_case.assertIn(doc_id, response.headers['Location'])
    test_case.assertEqual(file_title, response.json["data"]["title"])


def auction_document_put_without_ds(test_case):
    file_title = 'name.doc'
    file_info = ('file', file_title, 'content')
    response = test_case.app.put(test_case.ENTRYPOINTS['document_put'], upload_files=[file_info])

    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(response.content_type, 'application/json')
    test_case.assertEqual(file_title, response.json["data"]["title"])


def auction_auction_get(test_case):
    expected_http_status = '403 Forbidden'
    auction_url = '/auctions/{}/auction'.format(test_case.auction['data']['id'])

    auth = test_case.app.authorization

    # auth as module auction
    test_case.app.authorization = ('Basic', ('auction', ''))

    response = test_case.app.get(auction_url, status=403)
    test_case.assertEqual(response.status, expected_http_status)

    test_case.app.authorization = auth


def auction_question_post(test_case):
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


def item_question_post(test_case):
    request_data = deepcopy(test_question_data)

    request_data['data']['questionOf'] = 'item'
    response = test_case.app.post_json(test_case.ENTRYPOINTS['questions'], request_data, status=422)
    test_case.assertEqual(response.json['errors'][0]['description'][0], "Value must be one of ['tender'].")


def question_patch(test_case):
    expected_http_status = '200 OK'
    answer = 'This is very original answer'

    request_data = {"data": {"answer": answer}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_question'], request_data)
    test_case.assertEqual(response.status, expected_http_status)

    # check answer
    response = test_case.app.get(test_case.ENTRYPOINTS['get_question'])
    question = response.json['data']
    test_case.assertEqual(question['answer'], answer)


def question_get(test_case):
    expected_http_status = '200 OK'

    response = test_case.app.get(test_case.ENTRYPOINTS['get_question'])

    test_case.assertEqual(response.status, expected_http_status)


def auction_bid_post(test_case):
    expected_http_status = '403 Forbidden'

    request_data = test_bid_data
    response = test_case.app.post_json(test_case.ENTRYPOINTS['bids'], request_data, status=403)
    test_case.assertEqual(response.status, expected_http_status)


def bid_document_post(test_case):
    document = deepcopy(test_document_data)
    url = test_case.generate_docservice_url(),
    document['url'] = url[0]
    expected_http_status = '201 Created'

    request_data = {'data': document}
    response = test_case.app.post_json(test_case.ENTRYPOINTS['add_bid_document'], request_data)
    test_case.assertEqual(expected_http_status, response.status)


def bid_document_post_without_ds(test_case):
    file_title = 'name.doc'
    file_info = ('file', file_title, 'content')
    response = test_case.app.post(test_case.ENTRYPOINTS['add_bid_document'], upload_files=[file_info])
    test_case.assertEqual(response.status, '201 Created')
    test_case.assertEqual(response.content_type, 'application/json')
    doc_id = response.json["data"]['id']
    test_case.assertIn(doc_id, response.headers['Location'])
    test_case.assertEqual(file_title, response.json["data"]["title"])


def bid_document_put_without_ds(test_case):
    file_title = 'name.doc'
    file_info = ('file', file_title, 'content')
    response = test_case.app.put(test_case.ENTRYPOINTS['bid_document'], upload_files=[file_info], status=403)
    test_case.assertEqual(response.status, '403 Forbidden')
    # test_case.assertEqual(response.content_type, 'application/json')
    # test_case.assertEqual(file_title, response.json["data"]["title"])


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

    # not bid owner get bid
    expected_http_status = '403 Forbidden'
    pattern = '/auctions/{}/bids/{}'
    entrypoint = pattern.format(test_case.auction['data']['id'], test_case.bid['data']['id'])
    response = test_case.app.get(entrypoint, status=403)
    test_case.assertEqual(expected_http_status, response.status)


def bid_get_in_active_status(test_case):
    auth = test_case.app.authorization

    test_case.app.authorization = ('Basic', ('{}'.format(test_case.bid['access']['owner']), ''))

    expected_http_status = '200 OK'
    response = test_case.app.get(test_case.ENTRYPOINTS['bid'])
    test_case.assertEqual(expected_http_status, response.status)

    test_case.app.authorization = auth

    # not bid owner get bid
    expected_http_status = '403 Forbidden'
    pattern = '/auctions/{}/bids/{}'
    entrypoint = pattern.format(test_case.auction['data']['id'], test_case.bid['data']['id'])
    response = test_case.app.get(entrypoint, status=403)
    test_case.assertEqual(expected_http_status, response.status)


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


def bid_pending_patch_document(test_case):
    patch_field = 'documentType'
    new = 'eligibilityDocuments'
    expected_http_status = '200 OK'

    auth = test_case.app.authorization

    request_data = {'data': {patch_field: new}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['bid_document'], request_data)
    test_case.assertEqual(expected_http_status, response.status)
    response = test_case.app.get(test_case.ENTRYPOINTS['bid_document'], request_data)
    bid_document = response.json['data']
    test_case.assertEqual(bid_document[patch_field], new)

    test_case.app.authorization = auth


def bid_pending_get_document(test_case):
    pass


def bid_active_patch_document(test_case):
    patch_field = 'documentType'
    new = 'commercialProposal'
    expected_http_status = '200 OK'

    auth = test_case.app.authorization

    # patch bid document
    request_data = {'data': {patch_field: new}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['bid_document'], request_data)
    test_case.assertEqual(expected_http_status, response.status)

    # get bid document
    response = test_case.app.get(test_case.ENTRYPOINTS['bid_document'], request_data)
    bid_document = response.json['data']
    test_case.assertEqual(bid_document[patch_field], new)

    test_case.app.authorization = auth


def bid_active_get_document(test_case):
    pass
