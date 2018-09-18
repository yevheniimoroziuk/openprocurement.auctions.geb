
def get_auction(test_case):
    test_case.app.get(test_case.entrypoint)

def patch_auction(test_case):
    patch_data = {'auctionUrl': u'http://auction-sandbox.openprocurement.org/auctions/{}'.format(test_case.auction['id'])}
    import ipdb; ipdb.set_trace()  # XXX BREAKPOINT
    for bid in test_case.extra['bids']:
        dag = 4

    import ipdb; ipdb.set_trace()  # XXX BREAKPOINT
    test_case.app.get(test_case.entrypoint)
    import ipdb; ipdb.set_trace()  # XXX BREAKPOINT
