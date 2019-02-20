from datetime import timedelta
from iso8601 import parse_date

from openprocurement.auctions.core.utils import (
    get_now,
    TZ
)


def auction_patch_field_mode(test_case):
    auth = test_case.app.authorization

    # auth as administrator
    test_case.app.authorization = ('Basic', ('administrator', ''))

    new_mode = 'test'

    request_data = {"data": {'mode': new_mode}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data)
    response = test_case.app.get(test_case.ENTRYPOINTS['get_auction'], request_data)

    auction = response.json['data']
    test_case.assertEqual(auction['mode'], new_mode)

    test_case.app.authorization = auth


def auction_patch_field_auction_period(test_case):
    auth = test_case.app.authorization

    # auth as administrator
    test_case.app.authorization = ('Basic', ('administrator', ''))

    # change auctionPeriod to new date
    new_auction_period_start_date = get_now() + timedelta(days=42)
    new_auction_period_start_date = new_auction_period_start_date.astimezone(TZ).isoformat()
    request_data = {"data": {'auctionPeriod': {'startDate': new_auction_period_start_date}}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data)
    response = test_case.app.get(test_case.ENTRYPOINTS['get_auction'], request_data)

    auction = response.json['data']
    test_case.assertEqual(auction['auctionPeriod']['startDate'], new_auction_period_start_date)

    # change auctionPeriod to None
    new_auction_period_start_date = None
    request_data = {"data": {'auctionPeriod': {'startDate': new_auction_period_start_date}}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data)
    response = test_case.app.get(test_case.ENTRYPOINTS['get_auction'], request_data)

    auction = response.json['data']
    auction_period = auction.get('auctionPeriod')
    if auction_period:
        test_case.assertIsNone(auction_period.get('startDate'))

    # return to default auth
    test_case.app.authorization = auth
