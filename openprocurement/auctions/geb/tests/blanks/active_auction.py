from openprocurement.auctions.geb.tests.helpers import get_auction_urls


def get_auction(test_case):
    test_case.app.get(test_case.entrypoint)


def patch_auction(test_case):
    import ipdb; ipdb.set_trace()  # XXX BREAKPOINT
    request_data = get_auction_urls(test_case.auction, test_case.extra['bids'])

    import ipdb; ipdb.set_trace()  # XXX BREAKPOINT
    test_case.app.patch(test_case.entrypoint, request_data)
    import ipdb; ipdb.set_trace()  # XXX BREAKPOINT
