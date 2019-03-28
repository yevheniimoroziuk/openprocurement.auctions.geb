from iso8601 import parse_date
from datetime import timedelta


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