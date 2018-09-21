def create_auction(self):
    expected_http_status = '201 Created'
    request_data = {"data": self.auction}

    entrypoint = '/auctions'
    response = self.app.post_json(entrypoint, request_data)
    self.assertEqual(response.status, expected_http_status)
