
def get_auction(test_case):
    test_case.app.get(test_case.entrypoint)


def patch_auction(test_case):
    pass
   # urls = get_auction_urls(test_case.auction, test_case.extra['bids'])

   # request_data = {'data': urls}
   # test_case.app.patch_json(test_case.entrypoint, request_data)
