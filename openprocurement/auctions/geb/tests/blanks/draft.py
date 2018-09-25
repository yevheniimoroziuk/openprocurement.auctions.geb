def phase_commit(test_case):
    next_status = 'active.rectification'
    request_data = {"data": {'status': next_status}}
    auth = test_case.app.authorization

    test_case.app.authorization = ('Basic', ('{}'.format(test_case.auction['access']['owner']), ''))
    response = test_case.app.patch_json(test_case.ENTRYPOINT, request_data)
    test_case.app.authorization = auth

    test_case.assertEqual(next_status, response.json['data']['status'])


def invalid_phase_commit(test_case):
    next_status = 'active.tendering'
    request_data = {"data": {'status': next_status}}
    auth = test_case.app.authorization

    test_case.app.authorization = ('Basic', ('{}'.format(test_case.auction['access']['owner']), ''))
    test_case.app.patch_json(test_case.ENTRYPOINT, request_data, status=403)
    test_case.app.authorization = auth
