from openprocurement.auctions.core.tests.base import snitch

from openprocurement.auctions.geb.tests.blanks.cancellations import (
    cancellation_get_listing,
    cancellation_get,
    cancellation_patch,
    cancellation_make_active,
)


class CancellationWorkFlowMixin(object):
    test_cancellation_get_listing = snitch(cancellation_get_listing)
    test_cancellation_get = snitch(cancellation_get)
    test_cancellation_patch = snitch(cancellation_patch)
    test_cancellation_make_active = snitch(cancellation_make_active)
