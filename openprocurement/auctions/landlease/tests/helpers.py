from collections import Mapping, Sequence


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
