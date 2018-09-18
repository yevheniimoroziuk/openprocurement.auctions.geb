# -*- coding: utf-8 -*-
from schematics.exceptions import ValidationError
from schematics.types import BaseType
from openprocurement.auctions.core.validation import (
    validate_json_data,
    validate_data
)

from openprocurement.auctions.core.utils import (
    get_now
)
from openprocurement.auctions.geb.constants import (
    AUCTION_DOCUMENT_STATUSES,
    AUCTION_STATUS_FOR_ADDING_QUESTIONS,
    AUCTION_STATUS_FOR_CHANGING_QUESTIONS,
    AUCTION_STATUS_FOR_DELETING_BIDS,
    BID_STATUSES_FOR_ADDING_DOCUMENTS,
    CAV_PS_CODES,
    PROCEDURE_DOCUMENT_STATUSES
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
    bid = request.context
    bid_documents = bid.documents
    auction = bid.__parent__
    new_status = request.validated['json_data'].get('status')

    if request.authenticated_role == 'Administrator' or new_status != 'active':
        return True

    try:
        if auction.enquiryPeriod.startDate > now or now > auction.enquiryPeriod.endDate:
            raise Exception('Can`t activate bid, can only in enquiry Period Auction status')

        if not any([document.documentType == 'eligibilityDocuments' for document in bid_documents]):
            raise Exception('Can`t activate bid, need document of documentType: eligibilityDocuments')

        if bid.qualified is not True:
            raise Exception('Can`t activate bid, qualified must be True')

        if not bid.bidNumber:
            raise Exception('Can`t activate bid, you must add the bidNumber')

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


def validate_question_adding_period(request):
    auction = request.context

    if auction.status not in AUCTION_STATUS_FOR_ADDING_QUESTIONS:
        err_msg = 'Can add question only in {}'.format(AUCTION_STATUS_FOR_ADDING_QUESTIONS)
        request.errors.add('body', 'data', err_msg)
        request.errors.status = 403
        return False
    return True


def validate_question_changing_period(request):
    auction = request.context.__parent__

    if auction.status not in AUCTION_STATUS_FOR_CHANGING_QUESTIONS:
        err_msg = 'Can update question only in {}'.format(AUCTION_STATUS_FOR_CHANGING_QUESTIONS)
        request.errors.add('body', 'data', err_msg)
        request.errors.status = 403
        return False
    return True


def cav_ps_code_validator(data, code):
    if code not in CAV_PS_CODES:
        raise ValidationError(BaseType.MESSAGES['choices'].format(CAV_PS_CODES))


def validate_first_auction_status(request):
    status = request.json_body['data'].get('status')
    if status and status != 'draft':
        err_msg = "Auction status must be draft"
        request.errors.add('body', 'data', err_msg)
        request.errors.status = 403
        return False
    return True


def validate_bid_document(request):
    auction = request.context.__parent__

    if auction.status not in BID_STATUSES_FOR_ADDING_DOCUMENTS:
        err_msg = 'Can\'t document in current ({}) auction status'.format(auction.status)
        request.errors.add('body', 'data', err_msg)
        request.errors.status = 403
        return
    return True
