def cancellation_post(test_case):
    expected_http_status = '201 Created'
    request_data = {"data": {'reason': 'Cancel reason'}}
    auth = test_case.app.authorization

    test_case.app.authorization = ('Basic', ('{}'.format(test_case.auction['access']['owner']), ''))
    response = test_case.app.post_json(test_case.ENTRYPOINTS['post_cancellation'], request_data)
    cancellation = response.json['data']
    test_case.app.authorization = auth
    test_case.assertEqual(response.status, expected_http_status)

    entrypoint = '/auctions/{}/cancellations/{}'.format(test_case.auction['data']['id'],
                                                        cancellation['id'])
    response = test_case.app.get(entrypoint)
    cancellation = response.json['data']

    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual('pending', cancellation['status'])


def cancellation_get_listing(test_case):
    response = test_case.app.get(test_case.ENTRYPOINTS['get_auction'])
    auction = response.json['data']
    auction_cancellations = [cancellation['id'] for cancellation in auction['cancellations']]

    response = test_case.app.get(test_case.ENTRYPOINTS['get_cancellations_listing'])
    cancellations = response.json['data']
    for cancellation in cancellations:
        test_case.assertIn(cancellation['id'], auction_cancellations)


def cancellation_get(test_case):
    expected_http_status = '200 OK'
    expected_data = ['date', 'status', 'reason', 'cancellationOf', 'id']
    response = test_case.app.get(test_case.ENTRYPOINTS['get_cancellation'])
    cancellation = response.json['data']

    test_case.assertEqual(response.status, expected_http_status)
    test_case.assertEqual(cancellation.keys(), expected_data)


def cancellation_patch(test_case):
    field = "reason"
    new_value = 'New important reason'

    request_data = {'data': {field: new_value}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_cancellation'], request_data)

    response = test_case.app.get(test_case.ENTRYPOINTS['get_cancellation'])
    cancellation = response.json['data']
    test_case.assertNotEqual(cancellation[field], new_value)


def cancellation_make_active(test_case):
    new_status = 'active'

    request_data = {'data': {'status': new_status}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_cancellation'], request_data)
    cancellation = response.json['data']

    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(cancellation['status'], new_status)

    response = test_case.app.get(test_case.ENTRYPOINTS['get_cancellation'])
    cancellation = response.json['data']
    test_case.assertEqual(cancellation['status'], new_status)

    response = test_case.app.get(test_case.ENTRYPOINTS['get_auction'])
    auction = response.json['data']
    test_case.assertIn(auction['status'], ['cancelled', 'pending.cancelled'])


def cancellation_make_clean_bids(test_case):
    new_status = 'active'

    request_data = {'data': {'status': new_status}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_cancellation'], request_data)
    auth = test_case.app.authorization
    for bid in test_case.bids:

        test_case.app.authorization = ('Basic', ('{}'.format(bid['access']['owner']), ''))

        expected_http_status = '404 Not Found'

        pattern = '/auctions/{auction}/bids/{bid}?acc_token={token}'
        entrypoint = pattern.format(auction=test_case.auction['data']['id'],
                                    bid=bid['data']['id'],
                                    token=bid['access']['token'])
        response = test_case.app.get(entrypoint, status=404)
        test_case.assertEqual(expected_http_status, response.status)

    test_case.app.authorization = auth
