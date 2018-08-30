from copy import deepcopy
from openprocurement.auctions.landlease.tests.helpers import get_errors_names


def create_invalid_minNumberOfQualifiedBids(self):
    request_path = '/auctions'
    expected_http_status = '422 Unprocessable Entity'
    error_name = 'minNumberOfQualifiedBids'
    data = deepcopy(self.initial_data)
    invalid_values = (-1, 0, 3, 4)

    for invalid_value in invalid_values:
        data['minNumberOfQualifiedBids'] = invalid_value
        request_data = {"data": data}
        response = self.app.post_json(request_path, request_data, status=expected_http_status)
        self.assertEqual(response.status, expected_http_status)
        self.assertIn(error_name, get_errors_names(response))
