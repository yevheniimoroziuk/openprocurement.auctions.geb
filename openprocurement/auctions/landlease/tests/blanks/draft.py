
from openprocurement.auctions.landlease.tests.helpers import (
    get_next_status,
)


def phase_commit(self):
    next_status = get_next_status(self.auction['status'])
    field = 'status'

    request_data = {"data": {field: next_status}}
    response = self.app.patch_json(self.entrypoint, request_data)
    self.assertEqual(next_status, response.json['data'][field])


def change_forbidden_field_in_draft(self):
    new_title = 'Test Title'
    field = 'title'

    request_data = {"data": {field: new_title}}
    response = self.app.patch_json(self.entrypoint, request_data)

    entrypoint = '/auctions/{}'.format(self.auction['id'])
    response = self.app.get(entrypoint)

    self.assertNotEqual(new_title, response.json['data'][field])
