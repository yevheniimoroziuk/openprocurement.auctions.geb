from collections import Mapping, Sequence


def get_resource_required_fields(resource_class):
    """
    Take schematics schema and recursively get required fields
    Return list of required fields, with mapping in nested schema
    """
    context = []

    if getattr(resource_class, 'fields', None):
        fields = resource_class.fields
    else:
        return None

    for field_name in fields:
        field = fields[field_name]

        if getattr(field, 'fields', None):
            required = {field_name: get_resource_required_fields(field)}
        else:
            required = field_name

        if getattr(field, 'required', None):
            context.append(required)
    return context


def get_error_description(error):
    if isinstance(error, Sequence):
        return error[0]
    elif isinstance(error, Mapping):
        return get_error_description(error.values()[0])
    return error
