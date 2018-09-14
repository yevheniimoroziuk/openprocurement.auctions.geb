# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, time
from uuid import uuid4

from schematics.exceptions import ValidationError
from schematics.transforms import whitelist
from schematics.types import StringType, IntType, MD5Type, BooleanType
from schematics.types.compound import ModelType
from schematics.types.serializable import serializable
from pyramid.security import Allow
from zope.interface import implementer
from openprocurement.auctions.landlease.interfaces import (
    IAuction,
    IBid,
    IQuestion
)
from openprocurement.auctions.core.models import (
    Administrator_bid_role,
    Administrator_role,
    Auction as BaseAuction,
    BankAccount,
    BaseOrganization,
    Guarantee,
    Question,
    IsoDateTimeType,
    IsoDurationType,
    ListType,
    Model,
    Period,
    Value,
    dgfCDB2Item,
    dgfCancellation,
    dgfDocument,
    get_auction,
    validate_items_uniq,
)
from openprocurement.auctions.core.plugins.awarding.v2_1.models import Award
from openprocurement.auctions.core.plugins.contracting.v2_1.models import Contract
from openprocurement.auctions.core.utils import (
    SANDBOX_MODE,
    TZ,
    get_now
)

from openprocurement.auctions.landlease.constants import (
    AUCTION_DOCUMENT_TYPES,
    AUCTION_STATUSES,
    BID_DOCUMENT_TYPES,
    BID_STATUSES,
)

from openprocurement.auctions.landlease.models.roles import (
    auction_create_role,
    auction_rectification_role,
    auction_edit_rectification_role,
    auction_tendering_role,
    auction_edit_tendering_role,
    auction_enquiry_role,
    auction_edit_enquiry_role,
    auction_contractTerms_create_role,
    question_enquiry_role,
    bid_view_role,
    bid_create_role,
    bid_pending_role,
    bid_active_role,
    bid_edit_draft_role,
    bid_edit_active_role,
    bid_edit_pending_role
)


class LandLeaseAuctionDocument(dgfDocument):
    documentOf = StringType(required=True, choices=['auction'], default='auction')

    documentType = StringType(choices=AUCTION_DOCUMENT_TYPES)


class LandLeaseBidDocument(dgfDocument):
    documentOf = StringType(required=True, choices=['bid'], default='bid')

    documentType = StringType(choices=BID_DOCUMENT_TYPES)


@implementer(IQuestion)
class LandLeaseQuestion(Question):

    class Options:
        roles = {
            'active.enquiry': question_enquiry_role
        }

    questionOf = StringType(required=True, choices=['tender', 'item'], default='tender')

    def validate_relatedItem(self, data, relatedItem):
        if not relatedItem and data.get('questionOf') in ['item']:
            raise ValidationError(u'This field is required.')

        if relatedItem:
            auction = get_auction(data['__parent__'])
            if data.get('questionOf') == 'item' and relatedItem not in [item.id for item in auction.items]:
                raise ValidationError(u"relatedItem should be one of items")


class LeaseTerms(Model):
    leaseDuration = IsoDurationType(required=True)


class ContractTerms(Model):

    class Options:
        roles = {
            'create': auction_contractTerms_create_role
        }
    type = StringType(choices=['lease'])
    leaseTerms = ModelType(LeaseTerms, required=True)


class AuctionParameters(Model):
    """Configurable auction parameters"""

    type = StringType(choices=['texas'])


class Cancellation(dgfCancellation):
    documents = ListType(ModelType(LandLeaseAuctionDocument), default=list())


def rounding_shouldStartAfter(start_after, auction, use_from=datetime(2016, 6, 1, tzinfo=TZ)):  # TODO rm black box
    if (auction.enquiryPeriod and auction.enquiryPeriod.startDate or get_now()) > use_from and not (SANDBOX_MODE and auction.submissionMethodDetails and u'quick' in auction.submissionMethodDetails):
        midnigth = datetime.combine(start_after.date(), time(0, tzinfo=start_after.tzinfo))
        if start_after >= midnigth:
            start_after = midnigth + timedelta(1)
    return start_after


class AuctionAuctionPeriod(Period):
    """The auction period."""

    @serializable(serialize_when_none=False)
    def shouldStartAfter(self):
        if self.endDate:
            return
        auction = self.__parent__
        if auction.status in ['draft']:
            return
        start_after = auction.enquiryPeriod.endDate
        return rounding_shouldStartAfter(start_after, auction).isoformat()

    def validate_startDate(self, data, startDate):
        auction = get_auction(data['__parent__'])
        if not auction.revisions and not startDate:
            raise ValidationError(u'This field is required.')


class RectificationPeriod(Period):
    invalidationDate = IsoDateTimeType()


Administrator_role = (Administrator_role + whitelist('awards'))


@implementer(IBid)
class LandLeaseBid(Model):
    class Options:
        roles = {
            'Administrator': Administrator_bid_role,
            'view': bid_view_role,
            'create': bid_create_role,
            'draft': bid_view_role,
            'edit_draft': bid_edit_draft_role,
            'pending': bid_pending_role,
            'edit_pending': bid_edit_pending_role,
            'active': bid_active_role,
            'edit_active': bid_edit_active_role,

        }

    tenderers = ListType(ModelType(BaseOrganization), required=True, min_size=1, max_size=1)
    date = IsoDateTimeType()
    id = MD5Type(required=True, default=lambda: uuid4().hex)
    status = StringType(choices=BID_STATUSES, default='draft')
    value = ModelType(Value)
    documents = ListType(ModelType(LandLeaseBidDocument), default=list())
    owner_token = StringType()
    owner = StringType()
    qualified = BooleanType()
    bidNumber = IntType()

    def get_role(self):
        auction = self.__parent__
        root = auction.__parent__
        request = root.request
        if request.authenticated_role == 'Administrator':
            role = 'Administrator'
        else:
            role = 'edit_{}'.format(request.context.status)
        return role

    def validate_value(self, data, value):
        auction = data['__parent__']
        if auction.value.amount != value.amount:
            raise ValidationError("Bid value amount should be equal as Auction value amount")
        if value.currency and value.currency != auction.value.currency:
            raise ValidationError("Bid value currency should be equal as Auction value currency")
        if value.valueAddedTaxIncluded != auction.value.valueAddedTaxIncluded:
            raise ValidationError("Bid value valueAddedTaxIncluded should be equal as Auction value valueAddedTaxIncluded")

    def validate_bidNumber(self, data, bidNumber):
        auction = data['__parent__']
        if not bidNumber:
            return
        for bid in auction.bids:
            if data['id'] != bid.id and bidNumber == bid.bidNumber:
                raise ValidationError("bidNumber must be unique")

    def __local_roles__(self):
        return dict(
            [('{}_{}'.format(self.owner, self.owner_token), 'bid_owner')])

    def __acl__(self):
        return [
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'edit_bid')
        ]


@implementer(IAuction)
class Auction(BaseAuction):

    class Options:
        roles = {
            'create': auction_create_role,

            'active.rectification': auction_rectification_role,
            'edit_active.rectification': auction_edit_rectification_role,

            'active.tendering': auction_tendering_role,
            'edit_active.tendering': auction_edit_tendering_role,

            'active.enquiry': auction_enquiry_role,
            'edit_active.enquiry': auction_edit_enquiry_role,

            'Administrator': (whitelist('rectificationPeriod') + Administrator_role),
        }

    def __local_roles__(self):                                                  # TODO rm black box
        roles = dict([('{}_{}'.format(self.owner, self.owner_token), 'auction_owner')])
        for i in self.bids:
            roles['{}_{}'.format(i.owner, i.owner_token)] = 'bid_owner'
        return roles

    _internal_type = "landlease"

    auctionPeriod = ModelType(AuctionAuctionPeriod, required=True, default={})
    auctionParameters = ModelType(AuctionParameters)
    awardCriteria = StringType(choices=['highestCost'],
                               default='highestCost')

    awards = ListType(ModelType(Award), default=list())

    bids = ListType(ModelType(LandLeaseBid), default=list())

    questions = ListType(ModelType(LandLeaseQuestion), default=list())

    bankAccount = ModelType(BankAccount)

    budgetSpent = ModelType(Value, required=True)

    cancellations = ListType(ModelType(Cancellation), default=list())

    contracts = ListType(ModelType(Contract), default=list())

    contractTerms = ModelType(ContractTerms,
                              required=True)

    lotIdentifier = StringType(required=True)

    lotHolder = ModelType(BaseOrganization, required=True)

    description = StringType(required=True)

    documents = ListType(ModelType(LandLeaseAuctionDocument), default=list())

    enquiryPeriod = ModelType(Period)

    guarantee = ModelType(Guarantee, required=True)

    items = ListType(ModelType(dgfCDB2Item),
                     required=True,
                     min_size=1,
                     validators=[validate_items_uniq])

    minNumberOfQualifiedBids = IntType(choices=[1, 2], required=True)

    mode = StringType()

    procurementMethod = StringType(choices=['open'], default='open')

    procurementMethodType = StringType(required=True)

    rectificationPeriod = ModelType(RectificationPeriod)

    registrationFee = ModelType(Value, required=True)

    status = StringType(choices=AUCTION_STATUSES, default='draft')

    submissionMethod = StringType(choices=['electronicAuction'],
                                  default='electronicAuction')

    tenderAttempts = IntType(required=True, choices=range(1, 11))

    tenderPeriod = ModelType(Period)

    def __acl__(self):
        return [
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'edit_auction'),
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'edit_auction_award'),
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'upload_auction_documents'),
        ]

    def validate_tenderPeriod(self, data, period):
        if not period:
            return

    def validate_rectificationPeriod(self, data, period):
        if not period:
            return

    def validate_value(self, data, value):
        if value.currency != u'UAH':
            raise ValidationError(u"currency should be only UAH")

    def validate_minimalStep(self, data, value):
        if value.amount > data['value'].amount:
            raise ValidationError(u"minimalStep amount must be should be more then value amount")
        if value.valueAddedTaxIncluded != data['value'].valueAddedTaxIncluded:
            raise ValidationError(u"minimalStep.valueAddedTaxIncluded must be the same as value.valueAddedTaxIncluded")
        if value.currency != u'UAH':
            raise ValidationError(u"currency should be only UAH")

    @serializable(serialize_when_none=False)
    def next_check(self):
        check = None

        if self.status == 'active.rectification':
            check = self.rectificationPeriod.endDate.astimezone(TZ)
        elif self.status == 'active.tendering':
            check = self.tenderPeriod.endDate.astimezone(TZ)
        elif self.status == 'active.enquiry':
            check = self.tenderPeriod.endDate.astimezone(TZ)

        return check.isoformat() if check else None


LandLease = Auction
