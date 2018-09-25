
from openprocurement.auctions.geb.tests.fixtures.active_tendering import (
    END_ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE_WITH_ONE_BID,
    END_ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE_WITH_TWO_BIDS,
    END_ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE_WITH_TWO_BIDS_AND_ONE_DRAFT
)
from openprocurement.auctions.geb.tests.fixtures.active_enquiry import (
    END_ACTIVE_ENQUIRY_UNSUCCESSFUL_NO_ACTIVE_BIDS
)


def check_rectification_period_end(test_case):
    request_data = {'data': {'id': test_case.auction['data']['id']}}

    response = test_case.app.patch_json(test_case.ENTRYPOINTS['auction'], request_data)

    response = test_case.app.get(test_case.ENTRYPOINTS['auction'])
    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(response.json['data']["status"], 'active.tendering')


def check_tender_period_end_no_active_bids(test_case):
    context = test_case.procedure.snapshot()
    auction = context['auction']

    request_data = {'data': {'id': auction['data']['id']}}

    entrypoint = '/auctions/{}'.format(auction['data']['id'])
    response = test_case.app.patch_json(entrypoint, request_data)

    response = test_case.app.get(entrypoint)
    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(response.json['data']["status"], 'unsuccessful')


def check_tender_period_end_no_minNumberOfQualifiedBids(test_case):
    context = test_case.procedure.snapshot(fixture=END_ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE_WITH_ONE_BID)
    auction = context['auction']

    request_data = {'data': {'id': auction['data']['id']}}

    entrypoint = '/auctions/{}'.format(auction['data']['id'])
    response = test_case.app.patch_json(entrypoint, request_data)

    response = test_case.app.get(entrypoint)
    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(response.json['data']["status"], 'unsuccessful')


def check_tender_period_end_successful(test_case):
    context = test_case.procedure.snapshot(fixture=END_ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE_WITH_TWO_BIDS)
    auction = context['auction']

    request_data = {'data': {'id': auction['data']['id']}}

    entrypoint = '/auctions/{}'.format(auction['data']['id'])
    response = test_case.app.patch_json(entrypoint, request_data)

    response = test_case.app.get(entrypoint)
    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(response.json['data']["status"], 'active.enquiry')


def check_enquiry_period_end_unsuccessful(test_case):

    context = test_case.procedure.snapshot(fixture=END_ACTIVE_ENQUIRY_UNSUCCESSFUL_NO_ACTIVE_BIDS)

    auction = context['auction']

    request_data = {'data': {'id': auction['data']['id']}}

    entrypoint = '/auctions/{}'.format(auction['data']['id'])
    response = test_case.app.patch_json(entrypoint, request_data)

    response = test_case.app.get(entrypoint)
    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(response.json['data']["status"], 'unsuccessful')


def check_enquiry_period_end_active_qualification(test_case):
    request_data = {'data': {'id': test_case.auction_id}}

    auth = test_case.app.authorization
    for bid in test_case.extra['bids']:
        test_case.app.authorization = bid['owner']
        break

    auction = test_case.db.get(test_case.auction['id'])
    value = {'minNumberOfQualifiedBids': 1}
    auction.update(value)
    test_case.db.save(auction)

    test_case.app.authorization = auth

    response = test_case.app.patch_json(test_case.ENTRYPOINTS['auction'], request_data)

    response = test_case.app.get(test_case.ENTRYPOINTS['auction'])
    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(response.json['data']["status"], 'active.qualification')


def check_enquiry_period_end_active_auction(test_case):
    request_data = {'data': {'id': test_case.auction_id}}

    response = test_case.app.patch_json(test_case.ENTRYPOINTS['auction'], request_data)

    response = test_case.app.get(test_case.ENTRYPOINTS['auction'])
    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(response.json['data']["status"], 'active.auction')


def check_enquiry_period_end_set_unsuccessful_bids(test_case):
    request_data = {'data': {'id': test_case.auction_id}}

    test_case.app.patch_json(test_case.ENTRYPOINTS['auction'], request_data)

    db_auction = test_case.db.get(test_case.auction['id'])

    for bid in db_auction['bids']:
        if bid['status'] in ['draft', 'pending']:
            err_msg = 'All bids with status draft and pendign after enquiryPeriod must be unseccessful'
            raise AssertionError(err_msg)


def chronograph(test_case, auction):
    auth = test_case.app.authorization
    test_case.app.authorization = ('Basic', ('chronograph', ''))
    request_data = {'data': {'id': auction['id']}}
    entrypoint = '/auctions/{}'.format(auction['id'])
    test_case.app.patch_json(entrypoint, request_data)
    test_case.app.authorization = auth


def check_tender_period_end_delete_draft_bids(test_case):
    context = test_case.procedure.snapshot(fixture=END_ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE_WITH_TWO_BIDS_AND_ONE_DRAFT)
    auction = context['auction']
    bids = context['bids']
    draft_bid = [bid for bid in bids if bid['data']['status'] == 'draft'][0]

    bid_url_pattern = '/auctions/{auction}/bids/{bid}?acc_token={token}'
    bid_url = bid_url_pattern.format(auction=auction['data']['id'],
                                     bid=draft_bid['data']['id'],
                                     token=draft_bid['access']['token'])

    auth = test_case.app.authorization
    test_case.app.authorization = ('Basic', ('{}'.format(draft_bid['access']['owner']), ''))
    test_case.app.get(bid_url)
    test_case.app.authorization = auth

    request_data = {'data': {'id': auction['data']['id']}}
    entrypoint = '/auctions/{}'.format(auction['data']['id'])
    response = test_case.app.patch_json(entrypoint, request_data)

    response = test_case.app.get(entrypoint)
    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(response.json['data']["status"], 'active.enquiry')

    test_case.app.authorization = ('Basic', ('{}'.format(draft_bid['access']['owner']), ''))
    test_case.app.get(bid_url, status=404)
    test_case.app.authorization = auth
