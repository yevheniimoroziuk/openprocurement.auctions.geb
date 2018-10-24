def auction_get(test_case):
    expected_http_status = '200 OK'
    expected_data = [
        'bankAccount',
        'auctionID',
        'minNumberOfQualifiedBids',
        'enquiryPeriod',
        'registrationFee',
        'submissionMethod',
        'procuringEntity',
        'owner',
        'id',
        'tenderPeriod',
        'title',
        'tenderAttempts',
        'budgetSpent',
        'auctionParameters',
        'guarantee',
        'dateModified',
        'status',
        'lotHolder',
        'description',
        'auctionPeriod',
        'procurementMethodType',
        'date',
        'procurementMethod',
        'lotIdentifier',
        'rectificationPeriod',
        'contractTerms',
        'minimalStep',
        'items',
        'cancellations',
        'value',
        'numberOfBids',
        'awardCriteria'
    ]
    response = test_case.app.get(test_case.ENTRYPOINTS['auction_get'])
    cancellation = response.json['data']

    test_case.assertEqual(response.status, expected_http_status)
    test_case.assertEqual(cancellation.keys(), expected_data)
