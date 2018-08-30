from openprocurement.auctions.landlease.tests.helpers import (
    get_specification_fields,
    get_error_description
)

from collections import Mapping
from openprocurement.auctions.landlease.tests.specifications import (
    REQUIRED_SCHEME_DEFINITION
)


def create_auction_invalid_unsupported_media_type(self):
    request_path = '/auctions'
    expected_http_status = '415 Unsupported Media Type'

    request_data = 'data'
    response = self.app.post(request_path, request_data, status=415)
    self.assertEqual(response.status, expected_http_status)
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'],
                     [{u'description': u"Content-Type header should be one of ['application/json']",
                       u'location': u'header',
                       u'name': u'Content-Type'}])

    request_data = {'data': {'procurementMethodType': 'invalid_value'}}
    response = self.app.post_json(request_path, request_data, status=415)
    self.assertEqual(response.status, expected_http_status)
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'],
                     [{u'description': u'procurementMethodType is not implemented',
                       u'location': u'body',
                       u'name': u'data'}])


def create_auction_invalid_unprocessable_entity_common(self):
    entrypoint = '/auctions'
    expected_http_status = '422 Unprocessable Entity'

    request_data = 'data'
    response = self.app.post_json(entrypoint, expected_http_status, status=422)
    self.assertEqual(response.status, expected_http_status)
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'],
                     [{u'description': u'Data not available',
                       u'location': u'body',
                       u'name': u'data'}])

    request_data = {'not_data': {}}
    response = self.app.post_json(entrypoint, request_data, status=422)
    self.assertEqual(response.status, expected_http_status)
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'],
                     [{u'description': u'Data not available',
                       u'location': u'body',
                       u'name': u'data'}])

    request_data = {'data': []}
    response = self.app.post_json(entrypoint, request_data, status=422)
    self.assertEqual(response.status, expected_http_status)
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'],
                     [{u'description': u'Data not available',
                       u'location': u'body',
                       u'name': u'data'}])

    request_data = {
        'data': {
            'invalid_field': 'invalid_value',
            'procurementMethodType': self.initial_data['procurementMethodType']
        }
    }
    response = self.app.post_json(entrypoint, request_data, status=422)
    self.assertEqual(response.status, expected_http_status)
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'],
                     [{u'description': u'Rogue field',
                       u'location': u'body', u'name': u'invalid_field'}])


def create_auction_invalid_required_fields(self):
    entrypoint = '/auctions'
    expected_http_status = '422 Unprocessable Entity'
    response_required_fields = []
    required_fields = get_specification_fields(REQUIRED_SCHEME_DEFINITION,
                                               field_type='required')

    request_data = {'data': {'procurementMethodType': self.initial_data['procurementMethodType']}}
    response = self.app.post_json(entrypoint, request_data, status=422)
    self.assertEqual(response.status, expected_http_status)

    for error in response.json['errors']:
        if get_error_description(error['description']) == 'This field is required.':
            response_required_fields.append(error['name'])
    response_required_fields.append('procurementMethodType')

    for field in required_fields:
        if isinstance(field, Mapping):
            self.assertIn(field.keys()[0], response_required_fields)
        else:
            self.assertIn(field, response_required_fields)


def create_auction_common(self):
    response = self.app.post_json('/auctions', {"data": self.initial_data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')

    auction = response.json['data']
    self.assertIn(auction['id'], response.headers['Location'])


def create_auction(self):

    response = self.app.post_json('/auctions', {"data": self.initial_data})
    auction = response.json['data']
    self.assertEqual(response.status, '201 Created')

    response = self.app.get('/auctions/{}'.format(auction['id']))
    self.assertEqual(response.status, '200 OK')

    response = self.app.post_json('/auctions?opt_jsonp=callback', {"data": self.initial_data})
    self.assertIn('callback({"', response.body)

    response = self.app.post_json('/auctions?opt_pretty=1', {"data": self.initial_data})
    self.assertEqual(response.status, '201 Created')
    self.assertIn('{\n    "', response.body)

    response = self.app.post_json('/auctions', {"data": self.initial_data, "options": {"pretty": True}})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    self.assertIn('{\n    "', response.body)
