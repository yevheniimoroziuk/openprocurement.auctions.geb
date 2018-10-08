def create_auction(self):
    expected_http_status = '201 Created'
    request_data = {"data": self.auction}

    entrypoint = '/auctions'
    response = self.app.post_json(entrypoint, request_data)
    self.assertEqual(response.status, expected_http_status)


def create_auction_check_minNumberOfQualifiedBids(self):
    expected_minNumberOfQualifiedBids = 2
    request_data = {"data": self.auction}

    entrypoint = '/auctions'
    response = self.app.post_json(entrypoint, request_data)
    self.assertEqual(response.json['data']['minNumberOfQualifiedBids'],
                     expected_minNumberOfQualifiedBids)


def create_auction_check_auctionParameters(self):
    expected_auctionParameters = {'type': 'texas'}
    request_data = {"data": self.auction}

    entrypoint = '/auctions'
    response = self.app.post_json(entrypoint, request_data)
    self.assertEqual(response.json['data']['auctionParameters'],
                     expected_auctionParameters)


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


def create_auction_dump(self):

    request_data = {"data": self.auction}
    entrypoint = '/auctions'
    response = self.app.post_json(entrypoint, request_data)
    filename = 'docs/source/tutorial/create_auction.http'

    self.dump(response.request, response, filename)
