# -*- coding: utf-8 -*-
from functools import partial

from openprocurement.auctions.core.utils import (
    upload_file as base_upload_file,
    set_specific_hour,
    API_DOCUMENT_BLACKLISTED_FIELDS as DOCUMENT_BLACKLISTED_FIELDS,
    calculate_business_date
)

from openprocurement.auctions.geb.constants import (
    DOCUMENT_TYPE_OFFLINE
)


def upload_file(request, document, blacklisted_fields=DOCUMENT_BLACKLISTED_FIELDS):
    # offline document upload
    if hasattr(document, 'documentType') and document.documentType in DOCUMENT_TYPE_OFFLINE:
        document.format = 'offline/on-site-examination'
        return document
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
