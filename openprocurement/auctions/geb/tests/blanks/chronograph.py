from iso8601 import parse_date
from datetime import timedelta
from openprocurement.auctions.geb.tests.fixtures.active_tendering import (
    END_ACTIVE_TENDERING_AUCTION_WITH_ONE_BID,
    END_ACTIVE_TENDERING_AUCTION_WITH_TWO_BIDS,
    END_ACTIVE_TENDERING_AUCTION_WITH_TWO_BIDS_AND_ONE_DRAFT
)
from openprocurement.auctions.geb.tests.fixtures.active_enquiry import (
    END_ACTIVE_ENQUIRY_AUCTION,
    END_ACTIVE_ENQUIRY_AUCTION_QUALIFICATION,
    END_ACTIVE_ENQUIRY_UNSUCCESSFUL_NO_ACTIVE_BIDS
)
from openprocurement.auctions.geb.utils import (
    calculate_certainly_business_date as ccbd
)


def check_rectification_period_end(test_case):
    request_data = {'data': {'id': test_case.auction['data']['id']}}

    response = test_case.app.patch_json(test_case.ENTRYPOINTS['auction'], request_data)

    response = test_case.app.get(test_case.ENTRYPOINTS['auction'])
    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(response.json['data']["status"], 'active.tendering')


def check_tender_period_end_no_active_bids(test_case):
    context = test_case.procedure.snapshot()
    auction = context['auction']

    request_data = {'data': {'id': auction['data']['id']}}

    entrypoint = '/auctions/{}'.format(auction['data']['id'])
    response = test_case.app.patch_json(entrypoint, request_data)

    response = test_case.app.get(entrypoint)
    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(response.json['data']["status"], 'unsuccessful')


def check_tender_period_end_no_minNumberOfQualifiedBids(test_case):
    context = test_case.procedure.snapshot(fixture=END_ACTIVE_TENDERING_AUCTION_WITH_ONE_BID)
    auction = context['auction']

    request_data = {'data': {'id': auction['data']['id']}}

    entrypoint = '/auctions/{}'.format(auction['data']['id'])
    response = test_case.app.patch_json(entrypoint, request_data)

    response = test_case.app.get(entrypoint)
    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(response.json['data']["status"], 'unsuccessful')


def check_tender_period_end_successful(test_case):
    context = test_case.procedure.snapshot(fixture=END_ACTIVE_TENDERING_AUCTION_WITH_TWO_BIDS)
    auction = context['auction']

    request_data = {'data': {'id': auction['data']['id']}}

    entrypoint = '/auctions/{}'.format(auction['data']['id'])
    response = test_case.app.patch_json(entrypoint, request_data)

    response = test_case.app.get(entrypoint)
    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(response.json['data']["status"], 'active.enquiry')


def check_enquiry_period_end_unsuccessful(test_case):

    context = test_case.procedure.snapshot(fixture=END_ACTIVE_ENQUIRY_UNSUCCESSFUL_NO_ACTIVE_BIDS)

    auction = context['auction']

    request_data = {'data': {'id': auction['data']['id']}}

    entrypoint = '/auctions/{}'.format(auction['data']['id'])
    response = test_case.app.patch_json(entrypoint, request_data)

    response = test_case.app.get(entrypoint)
    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(response.json['data']["status"], 'unsuccessful')


def check_enquiry_period_end_active_qualification(test_case):
    context = test_case.procedure.snapshot(fixture=END_ACTIVE_ENQUIRY_AUCTION_QUALIFICATION)

    bid = context['bids'][0]
    auction = context['auction']

    request_data = {'data': {'id': auction['data']['id']}}
    entrypoint = '/auctions/{}'.format(auction['data']['id'])
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


def check_enquiry_period_end_active_auction(test_case):

    context = test_case.procedure.snapshot(fixture=END_ACTIVE_ENQUIRY_AUCTION)

    auction = context['auction']

    request_data = {'data': {'id': auction['data']['id']}}

    entrypoint = '/auctions/{}'.format(auction['data']['id'])
    response = test_case.app.patch_json(entrypoint, request_data)

    response = test_case.app.get(entrypoint)
    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(response.json['data']["status"], 'active.auction')


def check_enquiry_period_end_set_unsuccessful_bids(test_case):
    context = test_case.procedure.snapshot(fixture=END_ACTIVE_ENQUIRY_UNSUCCESSFUL_NO_ACTIVE_BIDS)

    auction = context['auction']
    bids = context['bids']

    request_data = {'data': {'id': auction['data']['id']}}

    entrypoint = '/auctions/{}'.format(auction['data']['id'])
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


def check_tender_period_end_delete_draft_bids(test_case):
    context = test_case.procedure.snapshot(fixture=END_ACTIVE_TENDERING_AUCTION_WITH_TWO_BIDS_AND_ONE_DRAFT)
    auction = context['auction']
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

    request_data = {'data': {'id': auction['data']['id']}}
    entrypoint = '/auctions/{}'.format(auction['data']['id'])
    response = test_case.app.patch_json(entrypoint, request_data)

    response = test_case.app.get(entrypoint)
    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(response.json['data']["status"], 'active.enquiry')

    test_case.app.authorization = ('Basic', ('{}'.format(draft_bid['access']['owner']), ''))
    test_case.app.get(bid_url, status=404)
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
