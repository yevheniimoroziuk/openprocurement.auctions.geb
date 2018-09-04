from copy import deepcopy
from collections import Mapping, Sequence
from openprocurement.auctions.landlease.tests.specifications import STATUS_CHANGES
from openprocurement.auctions.core.tests.base import (
    test_document_data
)


def get_error_description(error):
    if isinstance(error, Sequence):
        return error[0]
    elif isinstance(error, Mapping):
        return get_error_description(error.values()[0])

    return error


def get_errors_names(response):
    context = []
    errors = response.json.get('errors')

    if not errors:
        return None
    for error in errors:
        context.append(error['name'])

    return context


def get_specification_fields(scheme, field_type=None):
    context = []

    for field in scheme:
        field_name = field['name']

        if not field.get(field_type):
            continue
        if field.get('model'):
            required = {field_name: get_specification_fields(field['model'],
                                                             field_type=field_type)}
        else:
            required = field_name
        context.append(required)

    return context


def get_expected_value(scheme, check, order=0):

    def get_field():
        value = check[order] if isinstance(check, tuple) else check

        for field in scheme:
            if field.get('name') == value:
                return field
        return None

    field = get_field()
    if field.get('model'):
        return get_expected_value(field['model'], check, order=order + 1)
    else:
        return field.get('value')


def check_affilation(main, expected):
    for item in expected:
        if isinstance(item, Mapping):
            check_affilation(main.get(item.keys()[0]), item.values()[0])
        else:
            if not main.get(item):
                return item



def get_next_status(current):
    status = STATUS_CHANGES.get(current)
    if status:
        next_status = status.get('next_status')
        if next_status:
            return next_status[0]


def post_document(test_case, contract, **kwargs):
    data = {}
    if not kwargs.get('data'):
        data = deepcopy(test_document_data)
        data.update({
            'url': test_case.generate_docservice_url(),
            'documentOf': 'lot',
            'relatedItem': '01' * 16
        })
    else:
        data.update(kwargs['data'])

    target_status = 201
    if kwargs.get('status_code'):
        target_status = kwargs['status_code']

    url = CORE_ENDPOINTS['documents_collection'].format( contract_id=contract.data.id) + "?acc_token={}".format(contract.access.token)

    response = test_case.app.post_json(url, {'data': data}, status=target_status)
    return response
