from datetime import timedelta
from openprocurement.auctions.core.utils import get_now
from openprocurement.auctions.geb.constants import MIN_NUMBER_OF_DAY_BEFORE_AUCTION


def create_auction(self):
    expected_http_status = '201 Created'
    request_data = {"data": self.auction}

    entrypoint = '/auctions'
    response = self.app.post_json(entrypoint, request_data)
    self.assertEqual(response.status, expected_http_status)


def create_auction_invalid_auctionPeriod(self):
    expected_http_status = '422 Unprocessable Entity'
    auction = self.auction
    auction.pop('auctionPeriod')
    request_data = {"data": self.auction}

    entrypoint = '/auctions'
    response = self.app.post_json(entrypoint, request_data, status=422)
    self.assertEqual(response.status, expected_http_status)

    entrypoint = '/auctions'
    auction['auctionPeriod'] = {'startDate': None}
    response = self.app.post_json(entrypoint, request_data, status=422)
    self.assertEqual(response.status, expected_http_status)

    entrypoint = '/auctions'
    now = get_now()
    for days in range(1, MIN_NUMBER_OF_DAY_BEFORE_AUCTION):
        start_date = now + timedelta(days=days)
        auction['auctionPeriod'] = {'startDate': start_date.isoformat()}
        response = self.app.post_json(entrypoint, request_data, status=422)
        self.assertEqual(response.status, expected_http_status)
