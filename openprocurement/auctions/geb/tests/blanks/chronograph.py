import unittest
from freezegun import freeze_time
from iso8601 import parse_date
from datetime import timedelta

from openprocurement.auctions.core.utils import (
    set_specific_hour,
    SANDBOX_MODE
)

from openprocurement.auctions.geb.tests.fixtures.active_tendering import (
    END_ACTIVE_TENDERING_AUCTION_WITH_ONE_BID,
    END_ACTIVE_TENDERING_AUCTION_WITH_TWO_BIDS,
    END_ACTIVE_TENDERING_AUCTION_WITH_TWO_BIDS_AND_ONE_DRAFT
)
from openprocurement.auctions.geb.tests.fixtures.active_enquiry import (
    END_ACTIVE_ENQUIRY_AUCTION,
    END_ACTIVE_ENQUIRY_AUCTION_QUALIFICATION,
    END_ACTIVE_ENQUIRY_UNSUCCESSFUL_NO_BIDS_ACTIVE,
    END_ACTIVE_ENQUIRY_WITH_MIN_NUMBER_BID_1_WITH_2_ACTIVE_BIDS,
    END_ACTIVE_ENQUIRY_WITH_MIN_NUMBER_BID_1_WITH_NO_ACTIVE_BIDS,
    END_ACTIVE_ENQUIRY_WITH_MIN_NUMBER_BID_2_WITH_1_ACTIVE_BID,
    END_ACTIVE_ENQUIRY_AUCTION_QUALIFICATION_WITH_1_ACTIVE_AND_UNSUCCESSFUL

)
from openprocurement.auctions.geb.utils import (
    calculate_certainly_business_date as ccbd
)


def check_rectification_period_end(test_case):
    # end active.tendering Period
    # chronograph check

    # get auctionPeriod.rectificationPeriod.EndDate
    response = test_case.app.get(test_case.ENTRYPOINTS['auction'])
    data = response.json['data']
    rectification_end = parse_date(data['rectificationPeriod']['endDate'])

    # simulate rectificationPeriod.endDate
    with freeze_time(rectification_end):
        request_data = {'data': {'id': test_case.auction['data']['id']}}
        response = test_case.app.patch_json(test_case.ENTRYPOINTS['auction'], request_data)

    response = test_case.app.get(test_case.ENTRYPOINTS['auction'])
    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(response.json['data']["status"], 'active.tendering')


# end tendering test

def tendering_switch_to_unsuccessful_only_draft_bids(test_case):
    # end active.tendering Period
    # chronograph check
    # if no any bids in status 'pending/active'
    # set procedure status 'unsuccessful'
    context = test_case.procedure.snapshot()
    auction = context['auction']
    entrypoint = '/auctions/{}'.format(auction['data']['id'])

    # get auctionPeriod.tenderPeriod.EndDate
    response = test_case.app.get(entrypoint)
    data = response.json['data']
    tendering_end = parse_date(data['tenderPeriod']['endDate'])

    # simulate tenderingPeriod.endDate
    with freeze_time(tendering_end):
        request_data = {'data': {'id': auction['data']['id']}}
        response = test_case.app.patch_json(entrypoint, request_data)

    response = test_case.app.get(entrypoint)
    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(response.json['data']["status"], 'unsuccessful')


def tendering_switch_to_unsuccessful_bid_min_number_2_bid_1_active(test_case):
    # end active.tendering Period
    # chronograph check
    # if minNumberOfQualifiedBids 2 - only 1 bid in status 'pending/active'
    # (no other bids)
    # set procedure status 'unsuccessful'
    context = test_case.procedure.snapshot(fixture=END_ACTIVE_TENDERING_AUCTION_WITH_ONE_BID)
    auction = context['auction']
    entrypoint = '/auctions/{}'.format(auction['data']['id'])

    # get auctionPeriod.tenderPeriod.EndDate
    response = test_case.app.get(entrypoint)
    data = response.json['data']
    tendering_end = parse_date(data['tenderPeriod']['endDate'])

    # simulate tenderingPeriod.endDate
    with freeze_time(tendering_end):
        request_data = {'data': {'id': auction['data']['id']}}
        response = test_case.app.patch_json(entrypoint, request_data)

    response = test_case.app.get(entrypoint)
    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(response.json['data']["status"], 'unsuccessful')


def tendering_switch_to_enquiry(test_case):
    # end active.tendering Period
    # chronograph check
    # minNumberOfQualifiedBids 2 and 2 bid in status 'pending/active'
    # set procedure status 'active.enquiry'
    context = test_case.procedure.snapshot(fixture=END_ACTIVE_TENDERING_AUCTION_WITH_TWO_BIDS)
    auction = context['auction']
    entrypoint = '/auctions/{}'.format(auction['data']['id'])

    # get auctionPeriod.tenderPeriod.EndDate
    response = test_case.app.get(entrypoint)
    data = response.json['data']
    tendering_end = parse_date(data['tenderPeriod']['endDate'])

    # simulate tenderingPeriod.endDate
    with freeze_time(tendering_end):
        request_data = {'data': {'id': auction['data']['id']}}
        response = test_case.app.patch_json(entrypoint, request_data)

    response = test_case.app.get(entrypoint)
    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(response.json['data']["status"], 'active.enquiry')


def tendering_delete_draft_bids(test_case):
    # end active.tendering Period
    # chronograph check
    # if some bids in status 'draft'
    # delete this bids
    context = test_case.procedure.snapshot(fixture=END_ACTIVE_TENDERING_AUCTION_WITH_TWO_BIDS_AND_ONE_DRAFT)
    auction = context['auction']
    entrypoint = '/auctions/{}'.format(auction['data']['id'])
    bids = context['bids']
    draft_bid = [bid for bid in bids if bid['data']['status'] == 'draft'][0]

    bid_url_pattern = '/auctions/{auction}/bids/{bid}?acc_token={token}'
    bid_url = bid_url_pattern.format(auction=auction['data']['id'],
                                     bid=draft_bid['data']['id'],
                                     token=draft_bid['access']['token'])

    auth = test_case.app.authorization
    test_case.app.authorization = ('Basic', ('{}'.format(draft_bid['access']['owner']), ''))
    test_case.app.get(bid_url)
    test_case.app.authorization = auth

    # get auctionPeriod.tenderPeriod.EndDate
    response = test_case.app.get(entrypoint)
    data = response.json['data']
    tendering_end = parse_date(data['tenderPeriod']['endDate'])

    # simulate tenderingPeriod.endDate
    with freeze_time(tendering_end):
        request_data = {'data': {'id': auction['data']['id']}}
        response = test_case.app.patch_json(entrypoint, request_data)

    response = test_case.app.get(entrypoint)
    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(response.json['data']["status"], 'active.enquiry')

    test_case.app.authorization = ('Basic', ('{}'.format(draft_bid['access']['owner']), ''))
    test_case.app.get(bid_url, status=404)
    test_case.app.authorization = auth

# end enquiry tests


def enquiry_switch_to_unsuccessful_bids_min_number_2_no_bids(test_case):
    # end active.enquiry Period
    # chronograph check
    # minNumberOfQualifiedBids = 2
    # if no 2 bids in status 'active'
    # switch procedure to unsuccessful

    context = test_case.procedure.snapshot(fixture=END_ACTIVE_ENQUIRY_UNSUCCESSFUL_NO_BIDS_ACTIVE)
    auction = context['auction']
    entrypoint = '/auctions/{}'.format(auction['data']['id'])

    # get auctionPeriod.enquiryPeriod.EndDate
    response = test_case.app.get(entrypoint)
    data = response.json['data']
    enquiry_end = parse_date(data['enquiryPeriod']['endDate'])

    # simulate enquiryPeriod.endDate
    with freeze_time(enquiry_end):
        request_data = {'data': {'id': auction['data']['id']}}
        response = test_case.app.patch_json(entrypoint, request_data)

    response = test_case.app.get(entrypoint)
    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(response.json['data']["status"], 'unsuccessful')


def enquiry_switch_to_unsuccessful_bids_min_number_2_bid_1_active(test_case):
    # end active.enquiry Period
    # chronograph check
    # minNumberOfQualifiedBids = 2
    # if only 1 bid in status 'active'
    # switch procedure to unsuccessful

    context = test_case.procedure.snapshot(fixture=END_ACTIVE_ENQUIRY_WITH_MIN_NUMBER_BID_2_WITH_1_ACTIVE_BID)
    auction = context['auction']
    entrypoint = '/auctions/{}'.format(auction['data']['id'])

    # get auctionPeriod.enquiryPeriod.EndDate
    response = test_case.app.get(entrypoint)
    data = response.json['data']
    enquiry_end = parse_date(data['enquiryPeriod']['endDate'])

    # simulate enquiryPeriod.endDate
    with freeze_time(enquiry_end):
        request_data = {'data': {'id': auction['data']['id']}}
        response = test_case.app.patch_json(entrypoint, request_data)

    response = test_case.app.get(entrypoint)
    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(response.json['data']["status"], 'unsuccessful')


def enquiry_switch_to_unsuccessful_bids_min_number_1_no_bids(test_case):
    # end active.enquiry Period
    # chronograph check
    # minNumberOfQualifiedBids = 1
    # if no any bids in status 'active'
    # switch procedure to unsuccessful

    context = test_case.procedure.snapshot(fixture=END_ACTIVE_ENQUIRY_WITH_MIN_NUMBER_BID_1_WITH_NO_ACTIVE_BIDS)
    auction = context['auction']
    entrypoint = '/auctions/{}'.format(auction['data']['id'])

    # get auctionPeriod.enquiryPeriod.EndDate
    response = test_case.app.get(entrypoint)
    data = response.json['data']
    enquiry_end = parse_date(data['enquiryPeriod']['endDate'])

    # simulate enquiryPeriod.endDate
    with freeze_time(enquiry_end):
        request_data = {'data': {'id': auction['data']['id']}}
        response = test_case.app.patch_json(entrypoint, request_data)

    response = test_case.app.get(entrypoint)
    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(response.json['data']["status"], 'unsuccessful')


def enquiry_switch_to_active_auction_bids_min_number_1_bids_2_active(test_case):
    # end active.enquiry Period
    # chronograph check
    # minNumberOfQualifiedBids = 1
    # if 2 or more bids in status 'active'
    # switch procedure to status 'active.auction'

    context = test_case.procedure.snapshot(fixture=END_ACTIVE_ENQUIRY_WITH_MIN_NUMBER_BID_1_WITH_2_ACTIVE_BIDS)
    auction = context['auction']
    entrypoint = '/auctions/{}'.format(auction['data']['id'])

    # get auctionPeriod.enquiryPeriod.EndDate
    response = test_case.app.get(entrypoint)
    data = response.json['data']
    enquiry_end = parse_date(data['enquiryPeriod']['endDate'])

    # simulate enquiryPeriod.endDate
    with freeze_time(enquiry_end):
        request_data = {'data': {'id': auction['data']['id']}}
        response = test_case.app.patch_json(entrypoint, request_data)

    response = test_case.app.get(entrypoint)
    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(response.json['data']["status"], 'active.auction')


@unittest.skipIf(not SANDBOX_MODE, 'If sandbox mode is it enabled generating correct periods')
def enquiry_switch_to_active_qualification_sandbox(test_case):
    # end active.enquiry Period
    # chronograph check
    # minNumberOfQualifiedBids = 1
    # if is 1 bid in status 'active'
    # switch procedure to 'active.qualification'

    context = test_case.procedure.snapshot(fixture=END_ACTIVE_ENQUIRY_AUCTION_QUALIFICATION)
    auction = context['auction']
    entrypoint = '/auctions/{}'.format(auction['data']['id'])

    # get auctionPeriod.enquiryPeriod.EndDate
    response = test_case.app.get(entrypoint)
    data = response.json['data']
    enquiry_end = parse_date(data['enquiryPeriod']['endDate'])

    # simulate enquiryPeriod.endDate
    with freeze_time(enquiry_end):
        request_data = {'data': {'id': auction['data']['id']}}
        response = test_case.app.patch_json(entrypoint, request_data)

    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(response.json['data']["status"], 'active.qualification')


@unittest.skipIf(SANDBOX_MODE, 'If sandbox mode is it enabled generating correct periods')
def enquiry_switch_to_active_qualification(test_case):
    # end active.enquiry Period
    # chronograph check
    # minNumberOfQualifiedBids = 1
    # if is 1 bid in status 'active'
    # switch procedure to 'active.qualification'

    context = test_case.procedure.snapshot(fixture=END_ACTIVE_ENQUIRY_AUCTION_QUALIFICATION)
    bid = context['bids'][0]
    auction = context['auction']
    entrypoint = '/auctions/{}'.format(auction['data']['id'])

    # get auctionPeriod.enquiryPeriod.EndDate
    response = test_case.app.get(entrypoint)
    data = response.json['data']
    enquiry_end = parse_date(data['enquiryPeriod']['endDate'])

    # simulate enquiryPeriod.endDate
    with freeze_time(enquiry_end):
        request_data = {'data': {'id': auction['data']['id']}}
        response = test_case.app.patch_json(entrypoint, request_data)

    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(response.json['data']["status"], 'active.qualification')

    response = test_case.app.get('/auctions/{}/awards'.format(auction['data']['id']))

    # check generated award
    awards = response.json['data']
    award = awards[0]
    test_case.assertEqual(len(awards), 1)
    test_case.assertIsNotNone(award.get('verificationPeriod'))
    test_case.assertIsNotNone(award.get('signingPeriod'))
    test_case.assertEqual(award['status'], 'pending')
    test_case.assertEqual(award['bid_id'], bid['data']['id'])

    # check generated verificationPeriod
    entrypoint = '/auctions/{}'.format(auction['data']['id'])
    response = test_case.app.get(entrypoint)
    auction = response.json['data']
    enquiryPeriod_end_date = parse_date(auction['enquiryPeriod']['endDate'])
    expected_end_date = ccbd(enquiryPeriod_end_date, timedelta(days=1), specific_hour=18, working_days=True)
    verification_end_date = parse_date(award['verificationPeriod']['endDate'])
    test_case.assertEqual(verification_end_date, expected_end_date)

    # check generated signing
    signing_end_date = parse_date(award['signingPeriod']['endDate'])
    expected_end_date = ccbd(verification_end_date, timedelta(days=0), specific_hour=23) + timedelta(minutes=59)
    test_case.assertEqual(signing_end_date, expected_end_date)


def enquiry_switch_to_active_qualification_with_first_unsuccessful(test_case):
    # end active.enquiry Period
    # chronograph check
    # minNumberOfQualifiedBids = 1
    # if first bid is unsuccessful and second bid is in status 'active'
    # switch procedure to 'active.qualification'

    context = test_case.procedure.snapshot(fixture=END_ACTIVE_ENQUIRY_AUCTION_QUALIFICATION_WITH_1_ACTIVE_AND_UNSUCCESSFUL)
    active_bid = context['bids'][1]
    auction = context['auction']
    entrypoint = '/auctions/{}'.format(auction['data']['id'])

    # get auctionPeriod.enquiryPeriod.EndDate
    response = test_case.app.get(entrypoint)
    data = response.json['data']
    enquiry_end = parse_date(data['enquiryPeriod']['endDate'])

    # simulate enquiryPeriod.endDate
    with freeze_time(enquiry_end):
        request_data = {'data': {'id': auction['data']['id']}}
        response = test_case.app.patch_json(entrypoint, request_data)

    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(response.json['data']["status"], 'active.qualification')

    response = test_case.app.get('/auctions/{}/awards'.format(auction['data']['id']))

    # check generated award
    awards = response.json['data']
    award = awards[0]
    test_case.assertEqual(len(awards), 1)
    test_case.assertIsNotNone(award.get('verificationPeriod'))
    test_case.assertIsNotNone(award.get('signingPeriod'))
    test_case.assertEqual(award['status'], 'pending')
    test_case.assertEqual(award['bid_id'], active_bid['data']['id'])

    # check bid of award
    response = test_case.app.get('/auctions/{}/bids/{}'.format(auction['data']['id'], award['bid_id']))
    bid = response.json['data']
    test_case.assertEqual(bid['status'], 'active')


def enquiry_switch_to_active_auction(test_case):
    # end active.enquiry Period
    # chronograph check
    # minNumberOfQualifiedBids = 2
    # if is more then 2 bid in status 'active'
    # switch procedure to 'active.auction'

    context = test_case.procedure.snapshot(fixture=END_ACTIVE_ENQUIRY_AUCTION)
    auction = context['auction']
    entrypoint = '/auctions/{}'.format(auction['data']['id'])

    # get auctionPeriod.enquiryPeriod.EndDate
    response = test_case.app.get(entrypoint)
    data = response.json['data']
    enquiry_end = parse_date(data['enquiryPeriod']['endDate'])

    # simulate enquiryPeriod.endDate
    with freeze_time(enquiry_end):
        request_data = {'data': {'id': auction['data']['id']}}
        response = test_case.app.patch_json(entrypoint, request_data)

    response = test_case.app.get(entrypoint)
    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(response.json['data']["status"], 'active.auction')


def enquiry_set_unsuccessful_bids(test_case):
    # in the end of enquiry period
    # all bids that are in status 'draft/pending'
    # switch to 'unsuccessful' status
    context = test_case.procedure.snapshot(fixture=END_ACTIVE_ENQUIRY_UNSUCCESSFUL_NO_BIDS_ACTIVE)
    auction = context['auction']
    bids = context['bids']
    entrypoint = '/auctions/{}'.format(auction['data']['id'])

    # get auctionPeriod.enquiryPeriod.EndDate
    response = test_case.app.get(entrypoint)
    data = response.json['data']
    enquiry_end = parse_date(data['enquiryPeriod']['endDate'])

    # simulate enquiryPeriod.endDate
    with freeze_time(enquiry_end):
        request_data = {'data': {'id': auction['data']['id']}}
        response = test_case.app.patch_json(entrypoint, request_data)

    bid_url_pattern = '/auctions/{auction}/bids/{bid}?acc_token={token}'

    for bid in bids:
        bid_url = bid_url_pattern.format(auction=auction['data']['id'],
                                         bid=bid['data']['id'],
                                         token=bid['access']['token'])
        response = test_case.app.get(bid_url)
        test_case.assertEqual(response.status, '200 OK')
        test_case.assertEqual(response.json['data']["status"], 'unsuccessful')


def chronograph(test_case, auction):
    auth = test_case.app.authorization
    test_case.app.authorization = ('Basic', ('chronograph', ''))
    request_data = {'data': {'id': auction['id']}}
    entrypoint = '/auctions/{}'.format(auction['id'])
    test_case.app.patch_json(entrypoint, request_data)
    test_case.app.authorization = auth


def set_auctionPeriod_startDate_rectification(test_case):
    response = test_case.app.get(test_case.ENTRYPOINTS['auction'])
    auction = response.json['data']
    should_start_after = auction['auctionPeriod']['shouldStartAfter']
    start_date = parse_date(should_start_after) + timedelta(days=1)
    auction_period = {'auctionPeriod': {'startDate': start_date.isoformat()}}

    request_data = {"data": auction_period}
    test_case.app.patch_json(test_case.ENTRYPOINTS['auction'], request_data)

    response = test_case.app.get(test_case.ENTRYPOINTS['auction'])
    auction = response.json['data']
    test_case.assertEqual(start_date, parse_date(auction['auctionPeriod']['startDate']))


def set_auctionPeriod_startDate_tendering(test_case):
    context = test_case.procedure.snapshot()
    auction = context['auction']

    entrypoint = '/auctions/{}'.format(auction['data']['id'])

    response = test_case.app.get(entrypoint)
    auction = response.json['data']

    should_start_after = auction['auctionPeriod']['shouldStartAfter']
    start_date = parse_date(should_start_after) + timedelta(days=1)
    auction_period = {'auctionPeriod': {'startDate': start_date.isoformat()}}

    request_data = {"data": auction_period}
    test_case.app.patch_json(entrypoint, request_data)

    response = test_case.app.get(entrypoint)
    auction = response.json['data']
    test_case.assertEqual(start_date, parse_date(auction['auctionPeriod']['startDate']))


def set_auctionPeriod_startDate_enquiring(test_case):
    context = test_case.procedure.snapshot()
    auction = context['auction']
    entrypoint = '/auctions/{}'.format(auction['data']['id'])

    response = test_case.app.get(entrypoint)
    auction = response.json['data']

    should_start_after = auction['auctionPeriod']['shouldStartAfter']
    start_date = parse_date(should_start_after) + timedelta(days=1)
    auction_period = {'auctionPeriod': {'startDate': start_date.isoformat()}}

    request_data = {"data": auction_period}
    test_case.app.patch_json(entrypoint, request_data)

    response = test_case.app.get(entrypoint)
    auction = response.json['data']
    test_case.assertEqual(start_date, parse_date(auction['auctionPeriod']['startDate']))


def replaning_auction(test_case):

    # get auctionPeriod.startDate
    response = test_case.app.get(test_case.ENTRYPOINTS['auction_get'])
    auction = response.json['data']
    auction_start_date = parse_date(auction['auctionPeriod']['startDate'])

    # simulate outstanding auction time
    # set 'now' to 19:00 day of auctionPeriod.startDate
    outstanding_auction_time = set_specific_hour(auction_start_date, 19)
    with freeze_time(outstanding_auction_time):
        request_data = {'data': {'id': test_case.auction['data']['id']}}
        response = test_case.app.patch_json(test_case.ENTRYPOINTS['auction_patch'], request_data)
    auction = response.json['data']
    should_start_after = parse_date(auction['auctionPeriod']['shouldStartAfter'])
    auction_start_date = parse_date(auction['auctionPeriod']['startDate'])

    # check new shouldStartAfter
    should_start_after = parse_date(auction['auctionPeriod']['shouldStartAfter'])
    test_case.assertLess(auction_start_date, should_start_after)
