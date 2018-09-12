import datetime
import iso8601
from mock import patch
from openprocurement.auctions.landlease.tests.helpers import (
    set_auction_period,
    create_active_bid,
    delete_bid
)


def set_auctionPeriod(test_case):
    expected_data = 'shouldStartAfter'

    request_data = {'data': {'id': test_case.auction_id}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['auction'], request_data)
    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(response.json['data']["status"], 'active.rectification')
    test_case.assertIn(expected_data, response.json['data']['auctionPeriod'].keys())


def check_rectification_period_end(test_case):
    set_auction_period(test_case, test_case.auction)
    request_data = {'data': {'id': test_case.auction_id}}
    endDate = test_case.auction['rectificationPeriod']['endDate']
    mock_time = iso8601.parse_date(endDate) + datetime.timedelta(minutes=5)

    with patch('openprocurement.auctions.landlease.adapters.checkers.get_now',) as mock_get_now:
        mock_get_now.return_value = mock_time
        response = test_case.app.patch_json(test_case.ENTRYPOINTS['auction'], request_data)

    response = test_case.app.get(test_case.ENTRYPOINTS['auction'])
    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(response.json['data']["status"], 'active.tendering')


def check_tender_period_end_no_active_bids(test_case):
    request_data = {'data': {'id': test_case.auction_id}}
    endDate = test_case.auction['tenderPeriod']['endDate']
    mock_time = iso8601.parse_date(endDate) + datetime.timedelta(minutes=5)

    with patch('openprocurement.auctions.landlease.adapters.checkers.get_now',) as mock_get_now:
        mock_get_now.return_value = mock_time
        response = test_case.app.patch_json(test_case.ENTRYPOINTS['auction'], request_data)

    response = test_case.app.get(test_case.ENTRYPOINTS['auction'])
    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(response.json['data']["status"], 'unsuccessful')


def check_tender_period_end_no_minNumberOfQualifiedBids(test_case):
    request_data = {'data': {'id': test_case.auction_id}}

    create_active_bid(test_case, test_case.auction)

    endDate = test_case.auction['tenderPeriod']['endDate']
    mock_time = iso8601.parse_date(endDate) + datetime.timedelta(minutes=5)

    with patch('openprocurement.auctions.landlease.adapters.checkers.get_now',) as mock_get_now:
        mock_get_now.return_value = mock_time
        response = test_case.app.patch_json(test_case.ENTRYPOINTS['auction'], request_data)

    response = test_case.app.get(test_case.ENTRYPOINTS['auction'])
    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(response.json['data']["status"], 'unsuccessful')


def check_tender_period_end_successful(test_case):
    request_data = {'data': {'id': test_case.auction_id}}

    create_active_bid(test_case, test_case.auction)
    create_active_bid(test_case, test_case.auction)

    endDate = test_case.auction['tenderPeriod']['endDate']
    mock_time = iso8601.parse_date(endDate) + datetime.timedelta(minutes=5)

    with patch('openprocurement.auctions.landlease.adapters.checkers.get_now',) as mock_get_now:
        mock_get_now.return_value = mock_time
        response = test_case.app.patch_json(test_case.ENTRYPOINTS['auction'], request_data)

    response = test_case.app.get(test_case.ENTRYPOINTS['auction'])
    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(response.json['data']["status"], 'active.enquiry')


def check_enquiry_period_end_unsuccessful(test_case):
    request_data = {'data': {'id': test_case.auction_id}}

    auth = test_case.app.authorization
    for bid in test_case.extra['bids']:
        test_case.app.authorization = bid['owner']
        delete_bid(test_case, test_case.auction, bid['data'], bid['access'])

    test_case.app.authorization = auth
    endDate = test_case.auction['enquiryPeriod']['endDate']
    mock_time = iso8601.parse_date(endDate) + datetime.timedelta(minutes=5)

    with patch('openprocurement.auctions.landlease.adapters.checkers.get_now',) as mock_get_now:
        mock_get_now.return_value = mock_time
        response = test_case.app.patch_json(test_case.ENTRYPOINTS['auction'], request_data)

    response = test_case.app.get(test_case.ENTRYPOINTS['auction'])
    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(response.json['data']["status"], 'unsuccessful')


def check_enquiry_period_end_active_qualification(test_case):
    request_data = {'data': {'id': test_case.auction_id}}

    auth = test_case.app.authorization
    for bid in test_case.extra['bids']:
        test_case.app.authorization = bid['owner']
        delete_bid(test_case, test_case.auction, bid['data'], bid['access'])
        break

    auction = test_case.db.get(test_case.auction['id'])
    value = {'minNumberOfQualifiedBids': 1}
    auction.update(value)
    test_case.db.save(auction)

    test_case.app.authorization = auth
    endDate = test_case.auction['enquiryPeriod']['endDate']
    mock_time = iso8601.parse_date(endDate) + datetime.timedelta(minutes=5)

    with patch('openprocurement.auctions.landlease.adapters.checkers.get_now',) as mock_get_now:
        mock_get_now.return_value = mock_time
        response = test_case.app.patch_json(test_case.ENTRYPOINTS['auction'], request_data)

    response = test_case.app.get(test_case.ENTRYPOINTS['auction'])
    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(response.json['data']["status"], 'active.qualification')


def check_enquiry_period_end_active_auction(test_case):
    request_data = {'data': {'id': test_case.auction_id}}

    endDate = test_case.auction['enquiryPeriod']['endDate']
    mock_time = iso8601.parse_date(endDate) + datetime.timedelta(minutes=5)

    with patch('openprocurement.auctions.landlease.adapters.checkers.get_now',) as mock_get_now:
        mock_get_now.return_value = mock_time
        response = test_case.app.patch_json(test_case.ENTRYPOINTS['auction'], request_data)

    response = test_case.app.get(test_case.ENTRYPOINTS['auction'])
    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(response.json['data']["status"], 'active.auction')
