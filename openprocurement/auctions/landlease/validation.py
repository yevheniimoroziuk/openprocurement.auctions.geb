# -*- coding: utf-8 -*-
from openprocurement.auctions.core.validation import (
    validate_json_data,
    validate_data
)

from openprocurement.auctions.core.utils import (
    get_now
)
from openprocurement.auctions.landlease.constants import (
    AUCTION_STATUS_FOR_DELETING_BIDS,
    PROCEDURE_DOCUMENT_STATUSES,
    AUCTION_DOCUMENT_STATUSES
)


def validate_change_bid_check_auction_status(request):
    if request.authenticated_role == 'Administrator':
        return True
    if request.validated['auction_status'] not in ['active.tendering', 'active.enquiry']:
        err_msg = 'Can\'t update bid in current ({}) auction status'.format(request.validated['auction_status'])
        request.errors.add('body', 'data', err_msg)
        request.errors.status = 403
        return False
    return True


def validate_change_bid_check_status(request):
    status = request.context.status
    auction_status = request.validated['auction_status']
    new_status = request.validated['json_data'].get('status')

    if request.authenticated_role == 'Administrator':
        return True

    try:
        if new_status != 'pending' and status == 'draft':
            raise Exception('Can\'t update bid status, only from draft you can switch to pending')

        if new_status == 'pending' and auction_status != 'active.tendering':
            raise Exception('Can`t activate bid, can only in active.tendering Auction status')

    except Exception as err:
        request.errors.add('body', 'data', err.message)
        request.errors.status = 403
        return False
    return True


def validate_make_active_status_bid(request):
    now = get_now()
    bid_documents = request.context.documents
    auction = request.validated['auction']
    new_status = request.validated['json_data'].get('status')

    if request.authenticated_role == 'Administrator' or new_status != 'active':
        return True

    try:
        if now > auction.enquiryPeriod.endDate:
            raise Exception('Can`t activate bid, can only in active.tendering Auction status')

        if not any([document.documentType == 'eligibilityDocuments' for document in bid_documents]):
            raise Exception('Can`t activate bid, need document of documentType: eligibilityDocuments')

        if request.context.qualified is not True:
            raise Exception('Can`t activate bid, qualified must be True')

    except Exception as err:
        request.errors.add('body', 'data', err.message)
        request.errors.status = 403
        return False
    return True


def validate_patch_auction_data(request, **kwargs):
    data = validate_json_data(request)
    validate_data(request, request.auction.__class__, data=data)


def check_auction_status_for_deleting_bids(request):
    auction = request.context.__parent__
    status = auction['status']

    if status not in AUCTION_STATUS_FOR_DELETING_BIDS:
        err_msg = 'Can\'t delete bid in current ({}) auction status'.format(status)
        request.errors.add('body', 'data', err_msg)
        request.errors.status = 403
        return False
    return True


def validate_document_editing_period(request, *kwargs):
    status = request.context.status
    role = request.authenticated_role

    if role != 'auction':
        auction_not_in_editable_state = status not in PROCEDURE_DOCUMENT_STATUSES
    else:
        auction_not_in_editable_state = status not in AUCTION_DOCUMENT_STATUSES

    if auction_not_in_editable_state:
        err_msg = 'Can\'t make document operations in current ({}) auction status'.format(status)
        request.errors.add('body', 'data', err_msg)
        request.errors.status = 403
        return False
    return True
