from copy import deepcopy
from openprocurement.auctions.core.tests.base import (
    test_document_data
)



def add_document(self):
    document = deepcopy(test_document_data)
    url = self.generate_docservice_url(),
    document['url'] = url[0]
    expected_http_status = '201 Created'

    request_data = {'data': document}
    response = self.app.post_json(self.entrypoint, request_data)
    self.assertEqual(expected_http_status, response.status)


def add_question(self):
    pass
