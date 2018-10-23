def create_auction(test_case):
    expected_http_status = '201 Created'
    request_data = {"data": test_case.auction}

    entrypoint = '/auctions'
    response = test_case.app.post_json(entrypoint, request_data)
    test_case.assertEqual(response.status, expected_http_status)


def auction_create_without_items(test_case):
    expected_http_status = '201 Created'
    request_data = {"data": test_case.auction}

    entrypoint = '/auctions'
    response = test_case.app.post_json(entrypoint, request_data)
    test_case.assertEqual(response.status, expected_http_status)


def create_auction_check_minNumberOfQualifiedBids(test_case):
    expected_minNumberOfQualifiedBids = 2
    request_data = {"data": test_case.auction}

    entrypoint = '/auctions'
    response = test_case.app.post_json(entrypoint, request_data)
    test_case.assertEqual(response.json['data']['minNumberOfQualifiedBids'],
                          expected_minNumberOfQualifiedBids)


def create_auction_check_auctionParameters(test_case):
    expected_auctionParameters = {'type': 'texas'}
    request_data = {"data": test_case.auction}

    entrypoint = '/auctions'
    response = test_case.app.post_json(entrypoint, request_data)
    test_case.assertEqual(response.json['data']['auctionParameters'],
                          expected_auctionParameters)


def create_auction_invalid_auctionPeriod(test_case):
    expected_http_status = '422 Unprocessable Entity'
    auction = test_case.auction
    auction.pop('auctionPeriod')
    request_data = {"data": test_case.auction}

    entrypoint = '/auctions'
    response = test_case.app.post_json(entrypoint, request_data, status=422)
    test_case.assertEqual(response.status, expected_http_status)

    entrypoint = '/auctions'
    auction['auctionPeriod'] = {'startDate': None}
    response = test_case.app.post_json(entrypoint, request_data, status=422)
    test_case.assertEqual(response.status, expected_http_status)


def create_auction_dump(test_case):

    request_data = {"data": test_case.auction}
    entrypoint = '/auctions'
    response = test_case.app.post_json(entrypoint, request_data)
    filename = 'docs/source/tutorial/create_auction.http'

    test_case.dump(response.request, response, filename)
