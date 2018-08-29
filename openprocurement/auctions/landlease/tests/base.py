# -*- coding: utf-8 -*-
import os
from datetime import timedelta

from openprocurement.auctions.core.tests.base import (
    BaseWebTest as CoreBaseWebTest,
    BaseAuctionWebTest as CoreBaseAuctionWebTest,
)
from openprocurement.auctions.core.utils import (
    apply_data_patch, get_now, SANDBOX_MODE
)

from openprocurement.auctions.core.tests.base import MOCK_CONFIG as BASE_MOCK_CONFIG
from openprocurement.auctions.core.utils import connection_mock_config

from openprocurement.auctions.landlease.tests.fixtures import (
    PARTIAL_MOCK_CONFIG,
    test_auction_data
)


MOCK_CONFIG = connection_mock_config(PARTIAL_MOCK_CONFIG,
                                     base=BASE_MOCK_CONFIG,
                                     connector=('plugins', 'api', 'plugins',
                                                'auctions.core', 'plugins'))


class BaseWebTest(CoreBaseWebTest):

    """Base Web Test to test openprocurement.auctions.landlease.

    It setups the database before each test and delete it after.
    """

    relative_to = os.path.dirname(__file__)
    mock_config = MOCK_CONFIG


class BaseAuctionWebTest(CoreBaseAuctionWebTest):
    relative_to = os.path.dirname(__file__)
    initial_data = test_auction_data
    mock_config = MOCK_CONFIG

    def go_to_rectificationPeriod_end(self):
        now = get_now()
        self.set_status('active.tendering', {
            "rectificationPeriod": {
                "startDate": (now - timedelta(days=14)).isoformat(),
                "endDate": (now - (timedelta(minutes=6) if SANDBOX_MODE else timedelta(days=6))).isoformat()
            },
            "tenderPeriod": {
                "startDate": (now - timedelta(days=14)).isoformat(),
                "endDate": (now + (timedelta(minutes=1) if SANDBOX_MODE else timedelta(days=1))).isoformat()
            },
            "enquiryPeriod": {
                "startDate": (now - timedelta(days=14)).isoformat(),
                "endDate": (now + (timedelta(minutes=1) if SANDBOX_MODE else timedelta(days=1))).isoformat()
            },
            "auctionPeriod": {
                "startDate": (now + timedelta(days=1)).isoformat()
            }
        })

    def set_status(self, status, extra=None):
        data = {'status': status}
        now = get_now()
        if status == 'active.tendering':
            data.update({
                "enquiryPeriod": {
                    "startDate": (now).isoformat(),
                    "endDate": (now + timedelta(days=7)).isoformat()
                },
                "rectificationPeriod": {
                    "startDate": (now).isoformat(),
                    "endDate": (now + timedelta(days=1)).isoformat()
                },
                "tenderPeriod": {
                    "startDate": (now).isoformat(),
                    "endDate": (now + timedelta(days=7)).isoformat()
                }
            })
        elif status == 'active.auction':
            data.update({
                "enquiryPeriod": {
                    "startDate": (now - timedelta(days=7)).isoformat(),
                    "endDate": (now).isoformat()
                },
                "rectificationPeriod": {
                    "startDate": (now - timedelta(days=7)).isoformat(),
                    "endDate": (now - timedelta(days=6)).isoformat()
                },
                "tenderPeriod": {
                    "startDate": (now - timedelta(days=7)).isoformat(),
                    "endDate": (now).isoformat()
                },
                "auctionPeriod": {
                    "startDate": (now).isoformat()
                }
            })
            if self.initial_lots:
                data.update({
                    'lots': [
                        {
                            "auctionPeriod": {
                                "startDate": (now).isoformat()
                            }
                        }
                        for i in self.initial_lots
                    ]
                })
        elif status == 'active.qualification':
            data.update({
                "enquiryPeriod": {
                    "startDate": (now - timedelta(days=8)).isoformat(),
                    "endDate": (now - timedelta(days=1)).isoformat()
                },
                "rectificationPeriod": {
                    "startDate": (now - timedelta(days=8)).isoformat(),
                    "endDate": (now - timedelta(days=6)).isoformat()
                },
                "tenderPeriod": {
                    "startDate": (now - timedelta(days=8)).isoformat(),
                    "endDate": (now - timedelta(days=1)).isoformat()
                },
                "auctionPeriod": {
                    "startDate": (now - timedelta(days=1)).isoformat(),
                    "endDate": (now).isoformat()
                },
                "awardPeriod": {
                    "startDate": (now).isoformat()
                }
            })
            if self.initial_lots:
                data.update({
                    'lots': [
                        {
                            "auctionPeriod": {
                                "startDate": (now - timedelta(days=1)).isoformat(),
                                "endDate": (now).isoformat()
                            }
                        }
                        for i in self.initial_lots
                    ]
                })
        elif status == 'active.awarded':
            data.update({
                "enquiryPeriod": {
                    "startDate": (now - timedelta(days=8)).isoformat(),
                    "endDate": (now - timedelta(days=1)).isoformat()
                },
                "rectificationPeriod": {
                    "startDate": (now - timedelta(days=8)).isoformat(),
                    "endDate": (now - timedelta(days=6)).isoformat()
                },
                "tenderPeriod": {
                    "startDate": (now - timedelta(days=8)).isoformat(),
                    "endDate": (now - timedelta(days=1)).isoformat()
                },
                "auctionPeriod": {
                    "startDate": (now - timedelta(days=1)).isoformat(),
                    "endDate": (now).isoformat()
                },
                "awardPeriod": {
                    "startDate": (now).isoformat(),
                    "endDate": (now).isoformat()
                }
            })
            if self.initial_lots:
                data.update({
                    'lots': [
                        {
                            "auctionPeriod": {
                                "startDate": (now - timedelta(days=1)).isoformat(),
                                "endDate": (now).isoformat()
                            }
                        }
                        for i in self.initial_lots
                    ]
                })
        elif status == 'complete':
            data.update({
                "enquiryPeriod": {
                    "startDate": (now - timedelta(days=18)).isoformat(),
                    "endDate": (now - timedelta(days=11)).isoformat()
                },
                "rectificationPeriod": {
                    "startDate": (now - timedelta(days=18)).isoformat(),
                    "endDate": (now - timedelta(days=17)).isoformat()
                },
                "tenderPeriod": {
                    "startDate": (now - timedelta(days=18)).isoformat(),
                    "endDate": (now - timedelta(days=11)).isoformat()
                },
                "auctionPeriod": {
                    "startDate": (now - timedelta(days=11)).isoformat(),
                    "endDate": (now - timedelta(days=10)).isoformat()
                },
                "awardPeriod": {
                    "startDate": (now - timedelta(days=10)).isoformat(),
                    "endDate": (now - timedelta(days=10)).isoformat()
                }
            })
            if self.initial_lots:
                data.update({
                    'lots': [
                        {
                            "auctionPeriod": {
                                "startDate": (now - timedelta(days=11)).isoformat(),
                                "endDate": (now - timedelta(days=10)).isoformat()
                            }
                        }
                        for i in self.initial_lots
                    ]
                })
        if extra:
            data.update(extra)
        auction = self.db.get(self.auction_id)
        auction.update(apply_data_patch(auction, data))
        self.db.save(auction)
        authorization = self.app.authorization
        self.app.authorization = ('Basic', ('chronograph', ''))
        response = self.app.get('/auctions/{}'.format(self.auction_id))
        self.app.authorization = authorization
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        return response

    def upload_auction_protocol(self, award):
        award_id = award['id']
        response = self.app.post_json('/auctions/{}/awards/{}/documents?acc_token={}'.format(self.auction_id, award_id, self.auction_token),
                                      {'data': {
                                          'title': 'auction_protocol.pdf',
                                          'url': self.generate_docservice_url(),
                                          'hash': 'md5:' + '0' * 32,
                                          'format': 'application/msword',
                                          "description": "auction protocol",
                                          "documentType": 'auctionProtocol',
                                      }})

        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        doc_id = response.json["data"]['id']
        self.assertIn(doc_id, response.headers['Location'])
        self.assertEqual('auction_protocol.pdf', response.json["data"]["title"])
        self.assertEqual('auctionProtocol', response.json["data"]["documentType"])
        self.assertEqual('auction_owner', response.json["data"]["author"])

    def post_auction_results(self):
        authorization = self.app.authorization
        self.app.authorization = ('Basic', ('auction', ''))
        now = get_now()
        auction_result = {
            'bids': [
                {
                    "id": b['id'],
                    "date": (now - timedelta(seconds=i)).isoformat(),
                    "value": b['value']
                }
                for i, b in enumerate(self.initial_bids)
            ]
        }
        response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': auction_result})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        auction = response.json['data']
        self.assertEqual('active.qualification', auction["status"])
        self.first_award = auction['awards'][0]
        self.second_award = auction['awards'][1]
        self.first_award_id = self.first_award['id']
        self.second_award_id = self.second_award['id']
        self.app.authorization = authorization

    def check_award_status(self, auction_id, award_id, target_status):
        response = self.app.get(
            '/auctions/{0}/awards/{1}'.format(
                auction_id,
                award_id))
        current_status = response.json['data']['status']
        self.assertEqual(
            current_status,
            target_status,
            "Award status {0} isn't expected. Current status: {1}".format(
                current_status,
                target_status))

    def patch_award(self, award_id, status, bid_token=None):
        token = self.auction_token
        if bid_token:
            token = bid_token
        response = self.app.patch_json('/auctions/{}/awards/{}?acc_token={}'.format(
            self.auction_id, award_id, token
        ), {"data": {"status": status}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        return response

    def forbidden_patch_award(self, award_id, before_status, status):
        response = self.app.patch_json('/auctions/{}/awards/{}?acc_token={}'.format(
            self.auction_id, award_id, self.auction_token
        ), {"data": {"status": status}}, status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]["description"], "Can't switch award ({}) status to ({}) status".format(before_status, status))
