from copy import deepcopy
from uuid import uuid4
from datetime import timedelta
from openprocurement.auctions.core.utils import (
    get_now
)
from openprocurement.auctions.geb.tests.fixtures.calculator import (
    ContractCalculator as Calculator
)
from openprocurement.auctions.geb.tests.fixtures.common import (
    test_organization
)
from openprocurement.auctions.geb.tests.fixtures.documents import (
    CONTRACT_DOCUMENT
)
from openprocurement.auctions.geb.tests.fixtures.items import (
    TEST_ITEM
)
from openprocurement.auctions.geb.utils import (
    calculate_certainly_business_date as ccbd
)

signing_period_start = ccbd(get_now(), -timedelta(days=1), specific_hour=16)

calculator = Calculator(signing_period_start, 'signingPeriod', 'start')


CONTRACT_PENDING = {
    "status": "pending",
    "signingPeriod": {
        "startDate": calculator.signingPeriod.startDate.isoformat(),
        "endDate": calculator.signingPeriod.endDate.isoformat()
    },
    "items": [
        TEST_ITEM
    ],
    "suppliers": [
        test_organization
    ],
    "value": {
        "currency": "UAH",
        "amount": 200,
        "valueAddedTaxIncluded": True
    },
    "date": calculator.date.isoformat(),
    "awardID": uuid4().hex,
    "id": uuid4().hex,
    "contractID": "UA-EA-2018-09-20-000001-1"
}


contract = deepcopy(CONTRACT_PENDING)
contract['id'] = uuid4().hex

CONTRACT_PENDING = contract

# contract pending with document

contract = deepcopy(CONTRACT_PENDING)
contract['id'] = uuid4().hex
contract['documents'] = [CONTRACT_DOCUMENT]

CONTRACT_PENDING_WITH_DOCUMENT = contract
