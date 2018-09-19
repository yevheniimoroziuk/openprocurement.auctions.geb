#
#def validate_auction_auction_data(request, **kwargs):
#    data = validate_patch_auction_data(request)
#    auction = request.validated['auction']
#    if auction.status != 'active.auction':
#        request.errors.add('body', 'data', 'Can\'t {} in current ({}) auction status'.format('report auction results' if request.method == 'POST' else 'update auction urls', auction.status))
#        request.errors.status = 403
#        return
#    lot_id = request.matchdict.get('auction_lot_id')
#    if auction.lots and any([i.status != 'active' for i in auction.lots if i.id == lot_id]):
#        request.errors.add('body', 'data', 'Can {} only in active lot status'.format('report auction results' if request.method == 'POST' else 'update auction urls'))
#        request.errors.status = 403
#        return
#    if data is not None:
#        bids = data.get('bids', [])
#        auction_bids_ids = [i.id for i in auction.bids]
#        if len(bids) != len(auction.bids):
#            request.errors.add('body', 'bids', "Number of auction results did not match the number of auction bids")
#            request.errors.status = 422
#            return
#        if set([i['id'] for i in bids]) != set(auction_bids_ids):
#            request.errors.add('body', 'bids', "Auction bids should be identical to the auction bids")
#            request.errors.status = 422
#            return
#        data['bids'] = [x for (_, x) in sorted(zip([auction_bids_ids.index(i['id']) for i in bids], bids))]
#        if data.get('lots'):
#            auction_lots_ids = [i.id for i in auction.lots]
#            if len(data.get('lots', [])) != len(auction.lots):
#                request.errors.add('body', 'lots', "Number of lots did not match the number of auction lots")
#                request.errors.status = 422
#                return
#            if set([i['id'] for i in data.get('lots', [])]) != set([i.id for i in auction.lots]):
#                request.errors.add('body', 'lots', "Auction lots should be identical to the auction lots")
#                request.errors.status = 422
#                return
#            data['lots'] = [
#                x if x['id'] == lot_id else {}
#                for (y, x) in sorted(zip([auction_lots_ids.index(i['id']) for i in data.get('lots', [])], data.get('lots', [])))
#            ]
#        if auction.lots:
#            for index, bid in enumerate(bids):
#                if (getattr(auction.bids[index], 'status', 'active') or 'active') == 'active':
#                    if len(bid.get('lotValues', [])) != len(auction.bids[index].lotValues):
#                        request.errors.add('body', 'bids', [{u'lotValues': [u'Number of lots of auction results did not match the number of auction lots']}])
#                        request.errors.status = 422
#                        return
#                    for lot_index, lotValue in enumerate(auction.bids[index].lotValues):
#                        if lotValue.relatedLot != bid.get('lotValues', [])[lot_index].get('relatedLot', None):
#                            request.errors.add('body', 'bids', [{u'lotValues': [{u'relatedLot': ['relatedLot should be one of lots of bid']}]}])
#                            request.errors.status = 422
#                            return
#            for bid_index, bid in enumerate(data['bids']):
#                if 'lotValues' in bid:
#                    bid['lotValues'] = [
#                        x if x['relatedLot'] == lot_id and (getattr(auction.bids[bid_index].lotValues[lotValue_index], 'status', 'active') or 'active') == 'active' else {}
#                        for lotValue_index, x in enumerate(bid['lotValues'])
#                    ]
#
#    else:
#        data = {}
#    if request.method == 'POST':
#        now = get_now().isoformat()
#        if SANDBOX_MODE \ and auction.submissionMethodDetails \ and auction.submissionMethodDetails in [u'quick(mode:no-auction)', u'quick(mode:fast-forward)'] \ and auction._internal_type in ENGLISH_AUCTION_PROCUREMENT_METHOD_TYPES:
#            if auction.lots:
#                data['lots'] = [{'auctionPeriod': {'startDate': now, 'endDate': now}} if i.id == lot_id else {} for i in auction.lots]
#            else:
#                data['auctionPeriod'] = {'startDate': now, 'endDate': now}
#        else:
#            if auction.lots:
#                data['lots'] = [{'auctionPeriod': {'endDate': now}} if i.id == lot_id else {} for i in auction.lots]
#            else:
#                data['auctionPeriod'] = {'endDate': now}
#    request.validated['data'] = data
#
#
#def validate_status_in_which_can_use_auction_of_procedure(request, **kwargs):
#    auction = request.context
#
#    if auction.status != 'active.auction':
#        msg = 'Can\'t {} in current ({}) auction status'.format('report auction results' if request.method == 'POST' else 'update auction urls', auction.status)
#        request.errors.add('body', 'data', msg)
#        request.errors.status = 403
