from copy import deepcopy

from openprocurement.auctions.geb.tests.fixtures.create import (
    AUCTION as CREATE_AUCTION
)
from openprocurement.auctions.geb.tests.fixtures.draft import (
    AUCTION as DRAFT_AUCTION
)
from openprocurement.auctions.geb.tests.fixtures.active_rectification import (
    AUCTION as ACTIVE_RECTIFICATION_AUCTION,
    END_ACTIVE_RECTIFICATION_AUCTION
)
from openprocurement.auctions.geb.tests.fixtures.active_tendering import (
    AUCTION as ACTIVE_TENDERING_AUCTION,
    END_ACTIVE_TENDERING_AUCTION
)
from openprocurement.auctions.geb.tests.fixtures.active_enquiry import (
    AUCTION as ACTIVE_ENQUIRY_AUCTION,
    END_ACTIVE_ENQUIRY_AUCTION
)
from openprocurement.auctions.geb.tests.fixtures.active_auction import (
    AUCTION as ACTIVE_AUCTION_AUCTION,
    END_ACTIVE_AUCTION_AUCTION
)

from openprocurement.auctions.geb.tests.fixtures.active_qualification import (
    AUCTION as ACTIVE_QUALIFICATION_AUCTION
)
from openprocurement.auctions.geb.tests.fixtures.active_awarded import (
    AUCTION as ACTIVE_AWARDED_AUCTION
)


class State(object):

    def context(self, fixture):
        context = {}

        # add auction context
        context['auction'] = {}
        context['auction']['data'] = {'id': fixture['_id']}
        context['auction']['access'] = {'owner': fixture['owner'],
                                        'token': fixture['owner_token']}
        context['questions'] = []
        questions = fixture.get('questions', None)
        if questions:
            for question in questions:
                info = {}
                info['data'] = {'id': question['id']}
                context['questions'].append(info)

        # add bids context
        context['bids'] = []
        bids = fixture.get('bids', None)
        if bids:
            for bid in bids:
                info = {}

                info['data'] = {'id': bid['id'],
                                'status': bid['status']}
                info['access'] = {'token': bid['owner_token'],
                                  'owner': bid['owner']}
                # add bid document context
                if bid.get('documents', None):
                    info['data']['documents'] = []
                    for bid_document in bid['documents']:
                        document_info = {'data': {'id': bid_document['id']}}
                        info['data']['documents'].append(document_info)

                context['bids'].append(info)

        # add documents context
        context['documents'] = []
        documents = fixture.get('documents', None)
        if documents:
            for document in documents:
                info = {}
                info['data'] = {'id': document['id']}
                context['documents'].append(info)

        # add items context
        context['items'] = []
        items = fixture.get('items', None)
        if items:
            for item in items:
                info = {}
                info['data'] = deepcopy(item)
                context['items'].append(info)

        # add cancellations context
        context['cancellations'] = []
        cancellations = fixture.get('cancellations', None)
        if cancellations:
            for cancellation in cancellations:
                info = {}
                info['data'] = deepcopy(cancellation)
                context['cancellations'].append(info)

        # add awards context
        context['awards'] = []
        awards = fixture.get('awards', None)
        if awards:
            for award in awards:
                info = {}
                info['data'] = deepcopy(award)
                context['awards'].append(info)

        # add contracts context
        context['contracts'] = []
        contracts = fixture.get('contracts', None)
        if contracts:
            for contract in contracts:
                info = {}
                info['data'] = deepcopy(contract)
                context['contracts'].append(info)

        return context


# Auction States

# Active Awarded

class ActiveAwarded(State):
    fixture = ACTIVE_AWARDED_AUCTION
    status = 'active.awarded'

# Active Qualification


class ActiveQualification(State):
    fixture = ACTIVE_QUALIFICATION_AUCTION
    status = 'active.qualification'

    def _next(self, end=False):
        return ActiveAwarded()

# Active Auction


class EndActiveAuction(State):
    fixture = END_ACTIVE_AUCTION_AUCTION
    status = 'active.auction'


class ActiveAuction(State):
    fixture = ACTIVE_AUCTION_AUCTION
    status = 'active.auction'

    def context(self, fixture):
        context = {}
        context['auction'] = {}
        context['auction']['data'] = {'id': fixture['_id'],
                                      'value': fixture['value'],
                                      'minimalStep': fixture['value']}
        context['auction']['access'] = {'owner': fixture['owner'],
                                        'token': fixture['owner_token']}

        context['bids'] = []
        bids = fixture.get('bids', None)
        if bids:
            for bid in bids:
                info = {}
                info['data'] = {'id': bid['id'],
                                'status': bid['status']}
                info['access'] = {'token': bid['owner_token'],
                                  'owner': bid['owner']}
                context['bids'].append(info)
        # add cancellations context
        context['cancellations'] = []
        cancellations = fixture.get('cancellations', None)
        if cancellations:
            for cancellation in cancellations:
                info = {}
                info['data'] = deepcopy(cancellation)
                context['cancellations'].append(info)

        return context

    def _next(self, end=False):
        return ActiveQualification()

# Enquiry States


class EndActiveEnquiry(State):
    fixture = END_ACTIVE_ENQUIRY_AUCTION
    status = 'active.enquiry'


class ActiveEnquiry(State):
    fixture = ACTIVE_ENQUIRY_AUCTION
    status = 'active.enquiry'

    def _next(self, end=False):
        return ActiveAuction() if not end else EndActiveEnquiry()

# Tendering States


class EndActiveTendering(State):
    fixture = END_ACTIVE_TENDERING_AUCTION
    status = 'active.tendering'


class ActiveTendering(State):
    fixture = ACTIVE_TENDERING_AUCTION
    status = 'active.tendering'

    def _next(self, end=False):
        return ActiveEnquiry() if not end else EndActiveTendering()

# Rectification States


class EndActiveRectification(State):
    fixture = END_ACTIVE_RECTIFICATION_AUCTION
    status = 'active.rectification'


class ActiveRetification(State):
    fixture = ACTIVE_RECTIFICATION_AUCTION
    status = 'active.rectification'

    def _next(self, end=False):
        return ActiveTendering() if not end else EndActiveRectification()

# Draft States


class Draft(State):
    fixture = DRAFT_AUCTION
    status = 'draft'

    def _next(self, end=False):
        return ActiveRetification()


class Create(State):
    fixture = CREATE_AUCTION
    status = 'create'

    def context(self, fixture):
        context = {}
        context['auction'] = {}
        context['auction']['data'] = fixture
        return context

    def _next(self, end=False):
        return Draft()

# Machine


class ProcedureMachine(object):

    def __init__(self):
        self.state = Create()

    def __iter__(self):
        return self

    def _snapshot(self, dump, fixture):
        if dump:
            self._db.save(fixture)
        return self.state.context(fixture)

    def _next(self, end=False):
        self.state = self.state._next(end=end)

    def snapshot(self, dump=True, fixture=False):
        fixture = self.state.fixture if not fixture else fixture
        return self._snapshot(dump, fixture)

    def set_db_connector(self, db):
        self._db = db

    def next(self, end=False):
        try:
            self._next(end=end)
        except AttributeError:
            raise StopIteration
        return self.state

    def toggle(self, status, end=False):
        if self.state.status == status:
            return
        for state in self:
            if state.status == status:
                break
        if end:
            self.next(end=True)
