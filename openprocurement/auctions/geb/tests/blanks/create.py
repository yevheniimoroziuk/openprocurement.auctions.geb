from copy import deepcopy


def create_auction(test_case):
    expected_http_status = '201 Created'
    expected_data = [
        'auctionID',
        'auctionParameters',
        'auctionPeriod',
        'contractTerms',
        'date',
        'dateModified',
        'description',
        'guarantee',
        'id',
        'items',
        'lotHolder',
        'lotIdentifier',
        'minNumberOfQualifiedBids',
        'minimalStep',
        'mode',
        'owner',
        'procurementMethod',
        'procurementMethodDetails',
        'procurementMethodType',
        'procuringEntity',
        'registrationFee',
        'status',
        'submissionMethod',
        'submissionMethodDetails',
        'tenderAttempts',
        'title',
        'value'
    ]
    request_data = {"data": test_case.auction}

    entrypoint = '/auctions'
    response = test_case.app.post_json(entrypoint, request_data)
    test_case.assertEqual(response.status, expected_http_status)

    auction = response.json['data']
    for auction_data in auction.keys():
        test_case.assertIn(auction_data, expected_data)


def create_auction_invalid_minimalStep(test_case):
    expected_http_status = '422 Unprocessable Entity'
    auction = test_case.auction
    minimalStep = {'currency': u'UAH', 'amount': 100}
    value = {'currency': u'UAH', 'amount': 100}
    auction['minimalStep'] = minimalStep
    auction['value'] = value

    entrypoint = '/auctions'
    request_data = {"data": auction}
    response = test_case.app.post_json(entrypoint, request_data, status=422)
    test_case.assertEqual(response.status, expected_http_status)

    minimalStep = {'currency': u'UAH', 'amount': 150}
    auction['minimalStep'] = minimalStep
    response = test_case.app.post_json(entrypoint, request_data, status=422)
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
    auction = deepcopy(test_case.auction)
    auction.pop('auctionPeriod')
    request_data = {"data": auction}

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
