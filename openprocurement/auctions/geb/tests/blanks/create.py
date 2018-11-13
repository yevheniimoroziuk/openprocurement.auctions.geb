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

    response = test_case.app.post_json(test_case.ENTRYPOINTS['auction_post'], request_data)
    test_case.assertEqual(response.status, expected_http_status)

    auction = response.json['data']
    for auction_data in auction.keys():
        test_case.assertIn(auction_data, expected_data)


def create_auction_invalid_minimalStep(test_case):
    expected_http_status = '422 Unprocessable Entity'
    auction = test_case.auction

    # miniamalStep.amount should be less than value.amount
    minimalStep = {'currency': u'UAH', 'amount': 100}
    value = {'currency': u'UAH', 'amount': 100}
    auction['minimalStep'] = minimalStep
    auction['value'] = value
    request_data = {"data": auction}
    response = test_case.app.post_json(test_case.ENTRYPOINTS['auction_post'], request_data, status=422)
    test_case.assertEqual(response.status, expected_http_status)

    # minimalStep.valueAddedTaxIncluded.value should be the same as value.amount
    minimalStep = {
        'valueAddedTaxIncluded': False,
        'currency': u'UAH',
        'amount': 90
    }
    auction['minimalStep'] = minimalStep
    response = test_case.app.post_json(test_case.ENTRYPOINTS['auction_post'], request_data, status=422)
    test_case.assertEqual(response.status, expected_http_status)

    # minimalStep.value should be the same as value.amount
    minimalStep = {'currency': u'UAH', 'amount': 150}
    auction['minimalStep'] = minimalStep
    response = test_case.app.post_json(test_case.ENTRYPOINTS['auction_post'], request_data, status=422)
    test_case.assertEqual(response.status, expected_http_status)

    # currency should be only UAH
    minimalStep = {'currency': u'USD', 'amount': 32}
    auction['minimalStep'] = minimalStep
    response = test_case.app.post_json(test_case.ENTRYPOINTS['auction_post'], request_data, status=422)
    test_case.assertEqual(response.status, expected_http_status)


def auction_create_without_items(test_case):
    expected_http_status = '201 Created'
    request_data = {"data": test_case.auction}

    response = test_case.app.post_json(test_case.ENTRYPOINTS['auction_post'], request_data)
    test_case.assertEqual(response.status, expected_http_status)


def create_auction_check_minNumberOfQualifiedBids(test_case):
    expected_minNumberOfQualifiedBids = 2
    request_data = {"data": test_case.auction}

    response = test_case.app.post_json(test_case.ENTRYPOINTS['auction_post'], request_data)
    test_case.assertEqual(response.json['data']['minNumberOfQualifiedBids'],
                          expected_minNumberOfQualifiedBids)


def create_auction_check_auctionParameters(test_case):
    expected_auctionParameters = {'type': 'texas'}
    request_data = {"data": test_case.auction}

    response = test_case.app.post_json(test_case.ENTRYPOINTS['auction_post'], request_data)
    test_case.assertEqual(response.json['data']['auctionParameters'],
                          expected_auctionParameters)


def create_auction_invalid_auctionPeriod(test_case):
    expected_http_status = '422 Unprocessable Entity'
    auction = deepcopy(test_case.auction)
    auction.pop('auctionPeriod')
    request_data = {"data": auction}

    response = test_case.app.post_json(test_case.ENTRYPOINTS['auction_post'], request_data, status=422)
    test_case.assertEqual(response.status, expected_http_status)

    auction['auctionPeriod'] = {'startDate': None}
    response = test_case.app.post_json(test_case.ENTRYPOINTS['auction_post'], request_data, status=422)
    test_case.assertEqual(response.status, expected_http_status)


def create_auction_invalid_item_additional_classifications(test_case):
    # At least must be two additional classifications (kvtspz, cadastralNumber)

    # get context
    auction = deepcopy(test_case.auction)

    # change item additionalClassifications to invalid
    item = auction['items'][0]
    kvtspz_classificator = {
        'scheme': 'kvtspz',
        'id': '01.04',
        'description': 'Test'
    }
    item['additionalClassifications'][0] = kvtspz_classificator
    item['additionalClassifications'][1] = kvtspz_classificator

    request_data = {"data": auction}
    response = test_case.app.post_json(test_case.ENTRYPOINTS['auction_post'], request_data, status=422)
    expected_http_status = '422 Unprocessable Entity'
    test_case.assertEqual(response.status, expected_http_status)


def create_auction_invalid_value(test_case):
    # get context
    auction = deepcopy(test_case.auction)

    # change value to invalid
    # currency should be only UAH
    value = auction['value']
    value['currency'] = 'USD'

    request_data = {"data": auction}
    response = test_case.app.post_json(test_case.ENTRYPOINTS['auction_post'], request_data, status=422)
    expected_http_status = '422 Unprocessable Entity'
    test_case.assertEqual(response.status, expected_http_status)


def create_auction_dump(test_case):

    request_data = {"data": test_case.auction}
    response = test_case.app.post_json(test_case.ENTRYPOINTS['auction_post'], request_data)
    filename = 'docs/source/tutorial/create_auction.http'

    test_case.dump(response.request, response, filename)
