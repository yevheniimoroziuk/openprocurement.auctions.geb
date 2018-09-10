# -*- coding: utf-8 -*-
from openprocurement.auctions.core.validation import (
    validate_json_data,
    validate_data
)

from openprocurement.auctions.core.utils import (
    get_now
)


def validate_change_bid_check_auction_status(request):
    if request.authenticated_role == 'Administrator':
        return True
    if request.validated['auction_status'] not in ['active.tendering', 'active.tendering']:
        err_msg = 'Can\'t update bid in current ({}) auction status'.format(request.validated['auction_status'])
        request.errors.add('body', 'data', err_msg)
        request.errors.status = 403
        return False
    return True


def validate_change_bid_check_status(request):
    import ipdb; ipdb.set_trace()
    now = get_now()
    status = request.context.status
    auction_status = request.validated['auction_status']
    auction = request.validated['auction']
    new_status = request.validated['data'].get('status')

    if request.authenticated_role == 'Administrator':
        return True

    try:
        if new_status != 'pending' and status == 'draft':
            raise Exception('Can\'t update bid status, only from draft you can switch to pending')

        if new_status == 'pending' and auction_status != 'active.tendering':
            raise Exception('Can activate bid, only only in active.tendering Auction status')

        if new_status == 'active' and now > auction.enquiryPeriod.endDate:
            raise Exception('Can activate bid, only only in active.tendering Auction status')

    except Exception as err:
        request.errors.add('body', 'data', err.message)
        request.errors.status = 403
        return False
    return True


def validate_patch_auction_data(request, **kwargs):
    data = validate_json_data(request)
    validate_data(request, request.auction.__class__, data=data)
