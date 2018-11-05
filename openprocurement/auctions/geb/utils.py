# -*- coding: utf-8 -*-
from functools import partial

from openprocurement.auctions.core.utils import (
    upload_file as base_upload_file,
    get_file as base_get_file,
    set_specific_hour,
    API_DOCUMENT_BLACKLISTED_FIELDS as DOCUMENT_BLACKLISTED_FIELDS,
    calculate_business_date
)

from openprocurement.auctions.geb.constants import (
    DOCUMENT_TYPE_URL_ONLY,
    DOCUMENT_TYPE_OFFLINE
)


def upload_file(request, document, blacklisted_fields=DOCUMENT_BLACKLISTED_FIELDS):
    first_document = request.validated['documents'][0] if 'documents' in request.validated and request.validated['documents'] else None
    if document.documentType in (DOCUMENT_TYPE_URL_ONLY + DOCUMENT_TYPE_OFFLINE):
        if first_document:
            for attr_name in type(first_document)._fields:
                if attr_name not in blacklisted_fields:
                    setattr(document, attr_name, getattr(first_document, attr_name))
        if document.documentType in DOCUMENT_TYPE_OFFLINE:
            document.format = 'offline/on-site-examination'
        return document
    return base_upload_file(request, blacklisted_fields)


def get_file(request):
    document = request.validated['document']
    if document.documentType == 'virtualDataRoom':
        request.response.status = '302 Moved Temporarily'
        request.response.location = document.url
        return document.url
    return base_get_file(request)


calculate_certainly_business_date = partial(calculate_business_date, context=None)


def get_auction(model, interface):
    while not interface.providedBy(model):
        model = getattr(model, '__parent__', None)
        if model is None:
            return None
    return model


def calc_expected_auction_end_time(auction_start_date):
    end_time = set_specific_hour(auction_start_date, 18)
    return end_time
