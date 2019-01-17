# -*- coding: utf-8 -*-
from functools import partial

from openprocurement.auctions.core.utils import (
    upload_file as base_upload_file,
    set_specific_hour,
    calculate_business_date
)

from openprocurement.auctions.geb.constants import (
    DOCUMENT_BLACKLISTED_FIELDS,
    DOCUMENT_TYPE_OFFLINE
)


def get_actual_document(request):
    documents = request.validated.get('documents')
    return documents[-1] if documents else None


def upload_offline_document(request, document, blacklisted_fields):
    actual_document = get_actual_document(request)

    if actual_document:
        for attr_name in type(actual_document)._fields:
            if attr_name not in blacklisted_fields:
                setattr(document, attr_name, getattr(actual_document, attr_name))
        document.format = 'offline/on-site-examination'
        if 'document_id' in request.validated:
            document.id = request.validated['document_id']
    return document


def upload_file(request, document, blacklisted_fields=DOCUMENT_BLACKLISTED_FIELDS):
    if hasattr(document, 'documentType') and document.documentType in DOCUMENT_TYPE_OFFLINE:
        return upload_offline_document(request, document, blacklisted_fields)
    return base_upload_file(request, blacklisted_fields)

# fuction calculate business date without context arg
# is need for using in date calculation in test


calculate_certainly_business_date = partial(calculate_business_date, context=None)


def calc_expected_auction_end_time(auction_start_date):
    # calculate expected auction end time
    # it is need for checking replaning of module auction
    # if now time is more then this value and auctionPeriod.endDate is None
    # auction will be replaning
    end_time = set_specific_hour(auction_start_date, 18)
    return end_time
