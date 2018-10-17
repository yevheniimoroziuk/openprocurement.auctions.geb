# -*- coding: utf-8 -*-

from StringIO import StringIO
import json
import os

from openprocurement.auctions.core.tests.base import (
    BaseWebTest as CoreBaseWebTest,
)
from openprocurement.auctions.core.tests.base import MOCK_CONFIG as BASE_MOCK_CONFIG
from openprocurement.auctions.core.utils import connection_mock_config

from openprocurement.auctions.geb.tests.constants import (
    PARTIAL_MOCK_CONFIG
)


MOCK_CONFIG = connection_mock_config(PARTIAL_MOCK_CONFIG,
                                     base=BASE_MOCK_CONFIG,
                                     connector=('plugins', 'api', 'plugins',
                                                'auctions.core', 'plugins'))


class BaseWebTest(CoreBaseWebTest):
    """
    Base Web Test to test openprocurement.auctions.geb.

    It setups the database before each test and delete it after.
    """

    relative_to = os.path.dirname(__file__)
    mock_config = MOCK_CONFIG


class BaseWebDocsTest(BaseWebTest):
    """
    Base Web Docs Test to dump test results to files
    """

    def setUp(self):
        super(BaseWebDocsTest, self).setUp()

        if not os.environ.get('DOCSTEST'):
            self.skipTest('not docs test')

    def construct_request(self, request):
        buff = StringIO()
        lines = []

        url = request.url.split(request.host_url)[-1]
        format_url = '{} {}'.format(request.method,  url)
        lines.append(format_url)

        auth = request.authorization
        format_auth = 'Authorization: {} {}'.format(auth[0], auth[1])
        lines.append(format_auth)

        if request.content_type:
            format_content_type = 'Content-Type: {}'.format(request.content_type)
            lines.append(format_content_type)

        if request.body:
            format_body = json.dumps(json.loads(request.body), indent=2, ensure_ascii=False).encode('utf8')

        content = '\n'.join(lines)
        buff.write(content)
        if request.body:
            buff.write('\n\n')
            buff.write(format_body)
        return buff.getvalue()

    def construct_response(self, response, request):
        buff = StringIO()
        lines = []

        format_status = '{}'.format(response.status)
        lines.append(format_status)

        format_content_type = 'Content-Type: {}'.format(response.content_type)
        lines.append(format_content_type)

        if response.location:
            location = response.location.split(request.host_url)[-1]
            format_location = 'Location: {}'.format(location)
            lines.append(format_location)

        format_body = json.dumps(json.loads(response.body), indent=2, ensure_ascii=False).encode('utf8')

        content = '\n'.join(lines)
        buff.write(content)
        buff.write('\n\n')
        buff.write(format_body)
        return buff.getvalue()

    def dump_to_file(self, request, response, filename):

        with open(filename, 'w') as fd:
            fd.write(request)
            fd.write('\n\n\n')
            fd.write(response)

    def dump(self, request, response, filename):
        format_request = self.construct_request(request)
        format_response = self.construct_response(response, request)
        self.dump_to_file(format_request, format_response, filename)
