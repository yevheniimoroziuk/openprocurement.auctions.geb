import datetime
import iso8601
from mock import patch
from openprocurement.auctions.landlease.tests.helpers import set_auction_period


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


def check_tender_period_end(test_case):
    set_auction_period(test_case, test_case.auction)
    request_data = {'data': {'id': test_case.auction_id}}
    endDate = test_case.auction['tenderPeriod']['endDate']
    mock_time = iso8601.parse_date(endDate) + datetime.timedelta(minutes=5)

    import ipdb; ipdb.set_trace()  # XXX BREAKPOINT
    with patch('openprocurement.auctions.landlease.adapters.checkers.get_now',) as mock_get_now:
        mock_get_now.return_value = mock_time
        response = test_case.app.patch_json(test_case.ENTRYPOINTS['auction'], request_data)

    import ipdb; ipdb.set_trace()  # XXX BREAKPOINT
    response = test_case.app.get(test_case.ENTRYPOINTS['auction'])
    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(response.json['data']["status"], 'unsuccessful')
