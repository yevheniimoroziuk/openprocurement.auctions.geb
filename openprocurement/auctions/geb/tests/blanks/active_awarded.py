from copy import deepcopy
from openprocurement.auctions.core.tests.base import (
    test_document_data
)
from openprocurement.auctions.core.utils import (
    get_now
)


def organizer_uploads_the_contract(test_case):
    expected_http_status = '201 Created'
    document = deepcopy(test_document_data)
    document['documentType'] = 'contractSigned'
    url = test_case.generate_docservice_url(),
    document['url'] = url[0]

    request_data = {'data': document}
    response = test_case.app.post_json(test_case.ENTRYPOINTS['contract_document_post'], request_data)
    test_case.assertEqual(expected_http_status, response.status)

    document = response.json['data']
    pattern = '/auctions/{}/contracts/{}/documents/{}'

    entrypoint = pattern.format(test_case.auction['data']['id'],
                                test_case.contract['data']['id'],
                                document['id']
                                )
    response = test_case.app.get(entrypoint)
    test_case.assertEqual('200 OK', response.status)


def organizer_activate_contract(test_case):

    request_data = {"data": {"status": "active"}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['contract_patch'], request_data, status=403)
    test_case.assertEqual('Forbidden 403', response.status)

    now = get_now()
    request_data = {"data": {"dateSigned": now}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['contract_patch'], request_data)
    test_case.assertEqual('200 OK', response.status)

    response = test_case.app.get(test_case.ENTRYPOINTS['contract_get'])
