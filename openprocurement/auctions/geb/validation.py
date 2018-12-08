# -*- coding: utf-8 -*-
from datetime import timedelta

from schematics.exceptions import (
    ModelValidationError,
    ModelConversionError,
    ValidationError
)
from jsonpatch import JsonPointerException
from schematics.types import BaseType
from openprocurement.auctions.core.validation import (
    validate_json_data,
    error_handler
)

from openprocurement.auctions.core.utils import (
    get_now,
    apply_data_patch,
    calculate_business_date as cbd
)
from openprocurement.auctions.geb.constants import (
    AUCTION_RECTIFICATION_PERIOD_DURATION,
    AUCTION_STATUSES_FOR_ADDING_BID_DOCUMENTS,
    AUCTION_STATUSES_FOR_ADDING_DOCUMENTS,
    AUCTION_STATUSES_FOR_ADDING_QUESTIONS,
    AUCTION_STATUSES_FOR_CHANGING_ITEMS,
    AUCTION_STATUSES_FOR_CHANGING_QUESTIONS,
    AUCTION_STATUSES_FOR_DELETING_BIDS,
    AUCTION_STATUSES_FOR_MODULE_AUCTION_ADDING_DOCUMENTS,
    AUCTION_STATUSES_FOR_PATCHING_AUCTION,
    AUCTION_STATUSES_FOR_PATCHING_BIDS,
    AUCTION_STATUSES_FOR_PATCHING_DOCUMENTS_STATUSES,
    AUCTION_STATUSES_FOR_PUT_DOCUMENTS_STATUSES,
    BID_STATUSES_FOR_ADDING_BID_DOCUMENTS,
    BID_STATUSES_FOR_DELETING,
    BID_STATUSES_FOR_PATCHING,
    CAV_PS_CODES
)

# base validators


def _get_contexture_to_patch(request, model):
    initial_data = request.context.serialize()
    contexture = model(initial_data)
    contexture.__parent__ = request.context.__parent__
    return contexture


def _get_role_to_patch(contexture):
    role = contexture.get_role()
    return role


def _revel_patch(contexture, data):
    patch = apply_data_patch(contexture.serialize(), data)
    return patch


def impose_patch(contexture, patch):
    contexture.import_data(patch, partial=True, strict=True)


def _validate_patch_data(request, model, data):
    contexture = _get_contexture_to_patch(request, model)
    request.validated['resource_src'] = contexture.serialize()

    contexture_to_patch = _get_contexture_to_patch(request, model)
    method = contexture_to_patch.to_patch
    role = _get_role_to_patch(contexture)

    patch = _revel_patch(contexture_to_patch, data)
    # check if data received make patch
    if patch:
        # apply patch to contexture
        impose_patch(contexture_to_patch, patch)
        # serialize and cut off not valid fields
        data = method(role)
        # check if patch include valid fields
        patch = _revel_patch(contexture_to_patch, data)
        if patch:
            impose_patch(contexture_to_patch, patch)
            contexture = contexture_to_patch

    contexture.validate()
    request.validated['data'] = method(role)


def validate_patch_data(request, model, data):
    """
        patch resource validator
    """
    try:
        _validate_patch_data(request, model, data)
    # handle model errors
    except (ModelValidationError, ModelConversionError) as e:
        for i in e.message:
            request.errors.add('body', i, e.message[i])
        request.errors.status = 422
        raise error_handler(request)
    # handle json errors
    except JsonPointerException as err:
        request.errors.add('body', 'data', err.message)
        request.errors.status = 422
        raise error_handler(request)


def validate_patch_resource_data(request, **kwargs):
    data = validate_json_data(request)
    validate_patch_data(request, request.context.__class__, data)


# patch bid validators


def validate_bid_patch_auction_period(request, **kwargs):
    """
        validate in which auction periods, can patch bid
    """
    if request.authenticated_role == 'Administrator':
        return True

    if request.validated['auction_status'] not in AUCTION_STATUSES_FOR_PATCHING_BIDS:
        err_msg = 'Can\'t change bid, it can be done only in {} auction statuses'.format(AUCTION_STATUSES_FOR_PATCHING_BIDS)
        request.errors.add('body', 'data', err_msg)
        request.errors.status = 403
        return False
    return True


def validate_bid_activation(request, **kwargs):
    """
        validate bid activation(patch status to 'pending')
    """

    # check if it administrator bacause he can do everything
    if request.authenticated_role == 'Administrator':
        return True

    # check if it is valid two-phase commit
    new_status = request.validated['json_data'].get('status')
    if new_status != 'pending':
        err_msg = 'Can\'t update bid, in draft status are only valid change status to pending'
        request.errors.add('body', 'data', err_msg)
        request.errors.status = 403
        return False
    return True


def validate_bid_patch_pending_make_active_status(request, **kwargs):
    """
        validate patch bid(make status 'active')
    """

    # check if it administrator bacause he can do everything
    if request.authenticated_role == 'Administrator':
        return True

    bid = kwargs['context']
    auction = request.auction

    now = get_now()
    bid_documents = bid.documents
    new_data = request.validated['json_data']

    if auction.enquiryPeriod.startDate > now or now > auction.enquiryPeriod.endDate:
        msg = 'Can`t activate bid, can only in enquiry Period Auction status'
        request.errors.add('body', 'data', msg)
        request.errors.status = 403
        return False

    if not any([document.documentType == 'eligibilityDocuments' for document in bid_documents]):
        msg = 'Can`t activate bid, need document of documentType: eligibilityDocuments'
        request.errors.add('body', 'data', msg)
        request.errors.status = 403
        return False

    if bid.qualified is not True and not new_data.get('qualified'):
        msg = 'Can`t activate bid, qualified must be True'
        request.errors.add('body', 'data', msg)
        request.errors.status = 403
        return False

    if not bid.bidNumber and not new_data.get('bidNumber'):
        msg = 'Can`t activate bid, you must add the bidNumber'
        request.errors.add('body', 'data', msg)
        request.errors.status = 403
        return False
    return True


def validate_bid_patch_pending(request, **kwargs):
    """
        validate bid patch in 'pending' status
    """

    # check if it administrator bacause he can do everything
    if request.authenticated_role == 'Administrator':
        return True

    # check if it is patch status, only to active can switch
    new_status = request.validated['json_data'].get('status')
    if new_status and new_status != 'active':
        err_msg = 'Can`t update bid status. You can only switch from pending to active.'
        request.errors.add('body', 'data', err_msg)
        request.errors.status = 403
        return False

    return True


def validate_bid_patch_draft(request, **kwargs):
    """
        validate bid patch in 'draft' status
    """

    # check if it administrator bacause he can do everything
    if request.authenticated_role == 'Administrator':
        return True

    # in bid status 'draft' can`t patch bid
    # only can change status to 'pending'
    patch_data = request.validated['json_data']
    if patch_data.keys() != ['status']:
        err_msg = 'Can\'t update bid status, in bid active status'
        request.errors.add('body', 'data', err_msg)
        request.errors.status = 403
        return False

    return True


def validate_bid_patch_active(request, **kwargs):
    """
        validate bid patch in 'active' status
    """

    # check if it administrator bacause he can do everything
    if request.authenticated_role == 'Administrator':
        return True

    # check if it is patch status, in active ca`nt patch status
    new_status = request.validated['json_data'].get('status')
    if new_status:
        err_msg = 'Can\'t update bid status, in bid active status'
        request.errors.add('body', 'data', err_msg)
        request.errors.status = 403
        return False
    return True

# delete bid validaators


def validate_bid_delete(request, **kwargs):
    bid = kwargs['context']
    auction = request.auction
    bid_status = bid.status
    auction_status = auction.status

    if request.authenticated_role == 'Administrator':
        return True

    if auction_status not in AUCTION_STATUSES_FOR_DELETING_BIDS:
        err_msg = 'Can\'t delete bid in current ({}) auction status'.format(auction_status)
        request.errors.add('body', 'data', err_msg)
        request.errors.status = 403
        return False

    if bid_status not in BID_STATUSES_FOR_DELETING:
        err_msg = 'Can\'t delete bid, it can be done only in {} statuses'.format(BID_STATUSES_FOR_PATCHING)
        request.errors.add('body', 'data', err_msg)
        request.errors.status = 403
        return False
    return True


# patch auction validators

def validate_auction_patch_draft(request, **kwargs):
    """
        Validate patch auction in 'draft' status
    """

    new_status = request.validated['json_data'].get('status')
    new_items = request.validated['json_data'].get('items')

    # can switch only to 'active.rectification'
    if new_status and new_status != 'active.rectification':
        err_msg = "Can\'t switch to ({}) only to status 'active.rectification'".format(new_status)
        request.errors.add('body', 'data', err_msg)
        request.errors.status = 403
        return False

    # in status 'draft' can patch items
    if not new_status and new_items is None:
        err_msg = "In status 'draft' can`t change fields except ['status', 'items']".format(new_status)
        request.errors.add('body', 'data', err_msg)
        request.errors.status = 403
        return False

    return True


def validate_auction_patch_phase_commit(request, **kwargs):
    """
        Validate patch auction phase commit
    """

    auction = kwargs['context']
    new_status = request.validated['json_data'].get('status')

    # after status 'draft' at least there should be one item
    if len(auction.items) < 1:
        err_msg = 'Can\'t switch to ({}) without items'.format(new_status)
        request.errors.add('body', 'data', err_msg)
        request.errors.status = 403
        return False
    return True


def validate_auction_patch_phase_commit_auction_period(request, **kwargs):
    """
        Validate patch auction phase commit
        check created auctionPeriod.startDate
    """
    auction = kwargs['context']
    now = get_now()

    # check enquiryPeriod
    start_date = now
    end_date = cbd(auction.auctionPeriod.startDate, -timedelta(days=1), auction, specific_hour=20)

    if start_date > end_date:
        err_msg = 'auctionPeriod.startDate is incorrect, it does not allow to create periods correctly'
        request.errors.add('body', 'data', err_msg)
        request.errors.status = 403
        return False

    # check tenderPeriod
    rectification_end_date = cbd(now, AUCTION_RECTIFICATION_PERIOD_DURATION, auction)
    start_date = rectification_end_date
    end_date = cbd(auction.auctionPeriod.startDate, -timedelta(days=4), auction, specific_hour=20, working_days=True)

    if start_date > end_date:
        err_msg = 'auctionPeriod.startDate is incorrect, it does not allow to create periods correctly'
        request.errors.add('body', 'data', err_msg)
        request.errors.status = 403
        return False

    return True


def validate_auction_patch_rectification(request, **kwargs):
    """
        Validate patch auction in 'active.rectification'
    """

    # validate period in which can edit auction item

    patch_data = request.validated['json_data']
    items = patch_data.get('items')
    if 'items' in patch_data and (not items or (type(items) == list and len(items) == 0)):
        err_msg = 'Can`t change items, at least there should be one'
        request.errors.add('body', 'data', err_msg)
        request.errors.status = 403
        return False
    return True


def validate_auction_patch_period(request, **kwargs):
    # validate auction patch fields

    auction = kwargs['context']
    status = auction['status']

    # if it is Adminsrtator patch, he can patch
    if request.authenticated_role == 'Administrator':
        return True

    # if it is Chronograph patch, he can patch
    if request.authenticated_role == 'chronograph':
        return True

    # if it is Organizator patch, he can patch only in 'active.rectification'
    if status not in AUCTION_STATUSES_FOR_PATCHING_AUCTION:
        err_msg = 'Can\'t patch auction in current ({}) auction status'.format(status)
        request.errors.add('body', 'data', err_msg)
        request.errors.status = 403
        return False
    return True

# patch bid validators


def validate_patch_bid_data(request, **kwargs):
    data = validate_json_data(request)
    validate_patch_data(request, request.context.__class__, data)


def validate_auction_document_post(request, **kwargs):
    auction = request.auction
    status = auction.status
    role = request.authenticated_role

    if role != 'auction':
        auction_not_in_editable_state = status not in AUCTION_STATUSES_FOR_ADDING_DOCUMENTS
    else:
        auction_not_in_editable_state = status not in AUCTION_STATUSES_FOR_MODULE_AUCTION_ADDING_DOCUMENTS

    if auction_not_in_editable_state:
        err_msg = 'Can\'t make document operations in current ({}) auction status'.format(status)
        request.errors.add('body', 'data', err_msg)
        request.errors.status = 403
        return False
    return True


def validate_question_post(request, **kwargs):
    """
        Validator for question post
    """
    auction = request.auction

    if auction.status not in AUCTION_STATUSES_FOR_ADDING_QUESTIONS:
        err_msg = 'Can add question only in {}'.format(AUCTION_STATUSES_FOR_ADDING_QUESTIONS)
        request.errors.add('body', 'data', err_msg)
        request.errors.status = 403
        return False
    return True


def validate_patch_questions(request, **kwargs):
    """
        Validate patch questions
    """
    auction = request.auction

    if auction.status not in AUCTION_STATUSES_FOR_CHANGING_QUESTIONS:
        err_msg = 'Can update question only in {}'.format(AUCTION_STATUSES_FOR_CHANGING_QUESTIONS)
        request.errors.add('body', 'data', err_msg)
        request.errors.status = 403
        return False
    return True


def cav_ps_code_validator(data, code):
    if code not in CAV_PS_CODES:
        raise ValidationError(BaseType.MESSAGES['choices'].format(CAV_PS_CODES))


def validate_auction_post(request, **kwargs):
    """
        check if auction initial data has auctionPeriod.startDate
        auctionPeriod.startDate is required for creating auction
        if don`t have add errors and return False
    """
    auction = request.validated['json_data']
    if not auction.get('auctionPeriod') or not auction['auctionPeriod'].get('startDate'):
        err_msg = 'You must set auctionPeriod start date'
        request.errors.add('body', 'data', err_msg)
        request.errors.status = 422
        return False
    return True


def validate_auction_status_for_adding_bid_document(request, **kwargs):
    auction = request.auction

    if auction.status not in AUCTION_STATUSES_FOR_ADDING_BID_DOCUMENTS:
        err_msg = 'Can\'t document in current ({}) auction status'.format(auction.status)
        request.errors.add('body', 'data', err_msg)
        request.errors.status = 403
        return
    return True


def validate_bid_document_post(request, **kwargs):
    bid = kwargs['context']
    auction = request.auction

    if auction.status not in AUCTION_STATUSES_FOR_ADDING_BID_DOCUMENTS:
        err_msg = 'Can\'t document in current ({}) auction status'.format(auction.status)
        request.errors.add('body', 'data', err_msg)
        request.errors.status = 403
        return

    if bid.status not in BID_STATUSES_FOR_ADDING_BID_DOCUMENTS:
        err_msg = 'Can\'t add document in current ({}) bid status'.format(bid.status)
        request.errors.add('body', 'data', err_msg)
        request.errors.status = 403
        return
    return True


# validate module auction actions


def validate_auction_auction_status(request, **kwargs):
    """
        Validate in wich auction 'status'
        module auction can  brings results, and update auction urls
    """
    auction = kwargs.get('context')

    if auction.status != 'active.auction':
        msg = 'Not valid auction status'
        request.errors.add('body', 'data', msg)
        request.errors.status = 403
        return False
    return True


def validate_auction_number_of_bids(request, **kwargs):
    """
        Validate correctness of request data
        check number of bids
    """
    auction = kwargs.get('context')
    bids = request.validated['data'].get('bids', [])

    if len(bids) != len(auction.bids):
        err_msg = "Number of auction results did not match the number of auction bids"
        request.errors.add('body', 'bids', err_msg)
        request.errors.status = 422
        return False
    return True


def validate_auction_identity_of_bids(request, **kwargs):
    """
        When module auction update auction urls or brings results
        check patch data for adentity to auction.bids.
    """
    auction = kwargs.get('context')
    bids = request.validated['data'].get('bids', [])

    if set([bid['id'] for bid in bids]) != set([bid.id for bid in auction.bids]):
        request.errors.add('body', 'bids', "Auction bids should be identical to the auction bids")
        request.errors.status = 422
        return False
    return True


# auction document validators


def validate_auction_document_patch(request, **kwargs):
    """
        Validate patch auction document
    """
    auction = request.auction

    # check auction period for put auction document
    if auction.status not in AUCTION_STATUSES_FOR_PATCHING_DOCUMENTS_STATUSES:
        err_msg = 'Can`t update document in {}'.format(auction.status)
        request.errors.add('body', 'data', err_msg)
        request.errors.status = 403
        return False
    return True


def validate_auction_document_put(request, **kwargs):
    """
        Validate patch auction document
    """
    auction = request.auction

    # check auction period for put auction document
    if auction.status not in AUCTION_STATUSES_FOR_PUT_DOCUMENTS_STATUSES:
        err_msg = 'Can update document only in {}'.format(AUCTION_STATUSES_FOR_PUT_DOCUMENTS_STATUSES)
        request.errors.add('body', 'data', err_msg)
        request.errors.status = 403
        return False
    return True


# patch item validators

def validate_item_patch_auction_period(request, **kwargs):
    """
    Validate period in which can edit auction item
    """
    auction = request.auction

    if auction.status not in AUCTION_STATUSES_FOR_CHANGING_ITEMS:
        err_msg = 'Can update question only in {}'.format(AUCTION_STATUSES_FOR_CHANGING_ITEMS)
        request.errors.add('body', 'data', err_msg)
        request.errors.status = 403
        return False
    return True
