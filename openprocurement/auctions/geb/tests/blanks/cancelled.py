def auction_get(test_case):
    expected_http_status = '200 OK'
    response = test_case.app.get(test_case.ENTRYPOINTS['auction_get'])

    test_case.assertEqual(response.status, expected_http_status)
