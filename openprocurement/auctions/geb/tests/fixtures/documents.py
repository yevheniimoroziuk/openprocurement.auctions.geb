# -*- coding: utf-8 -*-
from copy import deepcopy
from datetime import datetime
from uuid import uuid4

now = datetime.now()

DOCUMENT = {
    "hash": "md5:00000000000000000000000000000000",
    "format": "application/msword",
    "url": "http://localhost/get/3ed16c4e58964858a170d38719b76996?KeyID=172d32c8&Signature=qQwkBqe5hs4MLTzh3dv7mcLRPK6JQ9O2FvXhnNzyFjyNitoOlJ%2FNvKYl9MaqExLwk1tZ9kH5aBI6Od90uPmdBw%253D%253D",
    "title": "укр.doc",
    "documentOf": "auction",
    "datePublished": now.isoformat(),
    "id": uuid4().hex,
    "dateModified": now.isoformat()
}
document = deepcopy(DOCUMENT)
document['documentOf'] = 'cancellation'
CANCELLATION_DOCUMENT = document


ELIGIBILITY_DOCUMENT = {
    "hash": "md5:00000000000000000000000000000000",
    "format": "application/msword",
    "url": "/auctions/d1bc378e15ae4e319a9154001a7c703b/bids/1775e5e75f924a879545379d4dc7b642/documents/ae4b1e94961742e4bacd4c695ecad43f?download=dd2c4773c24148bcafb37c15e48b788d",
    "title": "укр.doc",
    "documentOf": "bid",
    "datePublished": now.isoformat(),
    "documentType": "eligibilityDocuments",
    "id": uuid4().hex,
    "dateModified": now.isoformat()
}

BID_DOCUMENT = {
    "hash": "md5:00000000000000000000000000000000",
    "format": "application/msword",
    "url": "/auctions/d1bc378e15ae4e319a9154001a7c703b/bids/1775e5e75f924a879545379d4dc7b642/documents/ae4b1e94961742e4bacd4c695ecad43f?download=dd2c4773c24148bcafb37c15e48b788d",
    "title": "укр.doc",
    "documentOf": "bid",
    "datePublished": now.isoformat(),
    "documentType": "eligibilityDocuments",
    "id": uuid4().hex,
    "dateModified": now.isoformat()
}

test_document_service_url = 'http://localhost/get/6f63b414f958418082d22ec971424ca4?KeyID=172d32c8&Signature=2RWdpnpuy95Gn7E2vIDsHPPeRrtZUgtS75FsMxZBllnUUXNx%2BK7WvGeTtPvxHhcFAeW6UNfGtexCH2pNPPuzCA%3D%3D'

AUCTION_PROTOCOL_DOCUMENT = {
    "hash": "md5:00000000000000000000000000000000",
    "author": "auction_owner",
    "url": "http://localhost/get/ec59520826574794a52ab4e1e2768d4f?KeyID=172d32c8&Signature=YNMV1qHNv2Jys3OhHPlrX44eio8qLm5nW7AOuasefwQiV03CKhIeoIesXmxub7jF1PT8oQGMFtr%252ByocDj%2FrKCg%253D%253D",
    "format": "application/msword",
    "title": "Auction Protocol",
    "documentOf": "auction",
    "datePublished": now.isoformat(),
    "documentType": "auctionProtocol",
    "id": uuid4().hex,
    "dateModified": now.isoformat()
}

CONTRACT_DOCUMENT = {
    "hash": "md5:00000000000000000000000000000000",
    "author": "auction_owner",
    "url": "http://localhost/get/ec59520826574794a52ab4e1e2768d4f?KeyID=172d32c8&Signature=YNMV1qHNv2Jys3OhHPlrX44eio8qLm5nW7AOuasefwQiV03CKhIeoIesXmxub7jF1PT8oQGMFtr%252ByocDj%2FrKCg%253D%253D",
    "format": "application/msword",
    "title": "Auction Contract",
    "documentOf": "auction",
    "datePublished": now.isoformat(),
    "documentType": "contractSigned",
    "id": uuid4().hex,
    "dateModified": now.isoformat()
}

AUCTION_DOCUMENT_AUDIT = {
    "hash": "md5:00000000000000000000000000000000",
    "url": "http://localhost/get/ec59520826574794a52ab4e1e2768d4f?KeyID=172d32c8&Signature=YNMV1qHNv2Jys3OhHPlrX44eio8qLm5nW7AOuasefwQiV03CKhIeoIesXmxub7jF1PT8oQGMFtr%252ByocDj%2FrKCg%253D%253D",
    "format": "application/msword",
    "title": "Auction Audit",
    "documentOf": "auction",
    "datePublished": now.isoformat(),
    "id": uuid4().hex,
    "dateModified": now.isoformat()
}
