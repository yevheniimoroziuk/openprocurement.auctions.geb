from copy import deepcopy

from openprocurement.auctions.geb.tests.fixtures.common import (
    test_item,
    test_procuringEntity,
    test_lotHolder,
    test_bankAccount,
    test_contractTerms
)
from openprocurement.auctions.core.tests.base import (
    test_document_data
)


def change_title(self):
    new_title = 'Test'
    field = "title"

    request_data = {"data": {field: new_title}}
    response = self.app.patch_json(self.ENTRYPOINT, request_data)
    self.assertEqual(new_title, response.json['data'][field])


def change_desctiption(self):
    new = 'Test'
    field = "description"

    request_data = {"data": {field: new}}
    response = self.app.patch_json(self.ENTRYPOINT, request_data)
    self.assertEqual(new, response.json['data'][field])


def change_tenderAttempts(self):
    field = "tenderAttempts"
    value = 2

    request_data = {"data": {field: value}}
    response = self.app.patch_json(self.ENTRYPOINT, request_data)
    self.assertEqual(value, response.json['data'][field])


def change_lotIdentifier(self):
    new = '123456'
    field = "lotIdentifier"

    request_data = {"data": {field: new}}
    response = self.app.patch_json(self.ENTRYPOINT, request_data)
    self.assertEqual(new, response.json['data'][field])


def change_value(self):
    new = {u'currency': u'UAH', u'amount': 42.0, u'valueAddedTaxIncluded': True}
    field = "value"

    request_data = {"data": {field: new}}
    response = self.app.patch_json(self.ENTRYPOINT, request_data)
    self.assertEqual(new, response.json['data'][field])


def change_minimalStep(self):
    new = {u'currency': u'UAH', u'amount': 90.0, u'valueAddedTaxIncluded': True}
    field = "minimalStep"

    request_data = {"data": {field: new}}
    response = self.app.patch_json(self.ENTRYPOINT, request_data)
    self.assertEqual(new, response.json['data'][field])


def change_guarantee(self):
    new = {u'currency': u'UAH', u'amount': 42.0}
    field = "guarantee"

    request_data = {"data": {field: new}}
    response = self.app.patch_json(self.ENTRYPOINT, request_data)
    self.assertEqual(new, response.json['data'][field])


def change_items(self):
    item = deepcopy(test_item)
    item['quantity'] = 42
    new = item
    field = "items"

    request_data = {"data": {field: [new]}}
    response = self.app.patch_json(self.ENTRYPOINT, request_data)
    self.assertEqual(response.json['data'][field][0]['quantity'], new['quantity'])


def change_budgetSpent(self):
    new = {u'currency': u'UAH', u'amount': 42.0, u'valueAddedTaxIncluded': True}
    field = "budgetSpent"

    request_data = {"data": {field: new}}
    response = self.app.patch_json(self.ENTRYPOINT, request_data)
    self.assertEqual(new, response.json['data'][field])


def change_registrationFee(self):
    new = {u'currency': u'UAH', u'amount': 800.0, u'valueAddedTaxIncluded': True}
    field = "registrationFee"

    request_data = {"data": {field: new}}
    response = self.app.patch_json(self.ENTRYPOINT, request_data)
    self.assertEqual(new, response.json['data'][field])


def change_procuringEntity(self):
    procuringEntity = deepcopy(test_procuringEntity)
    procuringEntity['name'] = 'Test'
    new = procuringEntity
    field = "procuringEntity"

    request_data = {"data": {field: new}}
    response = self.app.patch_json(self.ENTRYPOINT, request_data)
    self.assertEqual(new, response.json['data'][field])


def change_lotHolder(self):
    lotHolder = deepcopy(test_lotHolder)
    lotHolder['name'] = 'Test'
    new = lotHolder
    field = "lotHolder"

    request_data = {"data": {field: new}}
    response = self.app.patch_json(self.ENTRYPOINT, request_data)
    self.assertEqual(new, response.json['data'][field])


def change_bankAccount(self):
    bankAccount = deepcopy(test_bankAccount)
    bankAccount['bankName'] = u'Test'
    new = bankAccount
    field = "bankAccount"

    request_data = {"data": {field: new}}
    response = self.app.patch_json(self.ENTRYPOINT, request_data)
    self.assertEqual(new, response.json['data'][field])


def change_contractTerms(self):
    contractTerms = deepcopy(test_contractTerms)
    contractTerms['leaseTerms']['leaseDuration'] = u'P20Y'
    new = contractTerms
    field = "contractTerms"

    request_data = {"data": {field: new}}
    response = self.app.patch_json(self.ENTRYPOINT, request_data)
    self.assertEqual(new, response.json['data'][field])


def add_document(self):
    document = deepcopy(test_document_data)
    url = self.generate_docservice_url(),
    document['url'] = url[0]
    expected_http_status = '201 Created'

    request_data = {'data': document}
    response = self.app.post_json(self.ENTRYPOINT, request_data)
    self.assertEqual(expected_http_status, response.status)
