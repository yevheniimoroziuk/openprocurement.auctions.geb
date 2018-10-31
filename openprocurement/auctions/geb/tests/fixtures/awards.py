from copy import deepcopy
from uuid import uuid4
from datetime import timedelta
from openprocurement.auctions.core.utils import (
    get_now
)
from openprocurement.auctions.geb.tests.fixtures.calculator import (
    AwardCalculator as Calculator
)
from openprocurement.auctions.geb.tests.fixtures.common import (
    test_organization
)
from openprocurement.auctions.geb.tests.fixtures.documents import (
    AUCTION_PROTOCOL_DOCUMENT
)
from openprocurement.auctions.geb.utils import (
    calculate_certainly_business_date as ccbd
)

verification_period_start = ccbd(get_now(), -timedelta(days=1), specific_hour=16)

calculator = Calculator(verification_period_start, 'verificationPeriod', 'start')

AWARD_PENDING = {
    "status": "pending",
    "verificationPeriod": {
        "startDate": calculator.verificationPeriod.startDate.isoformat(),
        "endDate": calculator.verificationPeriod.endDate.isoformat()
    },
    "complaintPeriod": {
        "startDate": calculator.complaintPeriod.startDate.isoformat(),
    },
    "suppliers": [
        test_organization
    ],
    "signingPeriod": {
        "startDate": calculator.signingPeriod.startDate.isoformat(),
        "endDate": calculator.signingPeriod.endDate.isoformat()
    },
    "value": {
        "currency": "UAH",
        "amount": 200,
        "valueAddedTaxIncluded": True
    },
    "date": calculator.date.isoformat(),
    "id": uuid4().hex
}

award = deepcopy(AWARD_PENDING)
award['id'] = uuid4().hex

award['documents'] = [AUCTION_PROTOCOL_DOCUMENT]
AWARD_PENDING_WITH_PROTOCOL = award
