# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, time
from uuid import uuid4

from schematics.exceptions import ValidationError
from schematics.transforms import blacklist, whitelist
from schematics.types import StringType, IntType, MD5Type, BooleanType
from schematics.types.compound import ModelType
from schematics.types.serializable import serializable
from pyramid.security import Allow
from zope.interface import implementer
from openprocurement.auctions.core.includeme import IAwardingNextCheck
from openprocurement.auctions.landlease.interfaces import IAuction, IBid
from openprocurement.auctions.core.models import (
    Model,
    Administrator_role,
    Auction as BaseAuction,
    BaseOrganization,
    BankAccount,
    Guarantee,
    IsoDateTimeType,
    IsoDurationType,
    ListType,
    Lot,
    Period, Value, calc_auction_end_time,
    dgfCDB2Complaint,
    dgfDocument,
    dgfCDB2Item,
    dgfCancellation,
    edit_role,
    get_auction,
    validate_items_uniq,
    validate_lots_uniq,
    validate_not_available,
    Administrator_bid_role
)
from openprocurement.auctions.core.plugins.awarding.v2_1.models import Award
from openprocurement.auctions.core.plugins.contracting.v2_1.models import Contract
from openprocurement.auctions.core.utils import (
    SANDBOX_MODE,
    TZ,
    get_request_from_root,
    get_now,
    AUCTIONS_COMPLAINT_STAND_STILL_TIME as COMPLAINT_STAND_STILL_TIME
)

from openprocurement.auctions.landlease.constants import (
    AUCTION_DOCUMENT_TYPES,
    AUCTION_STATUSES,
    BID_DOCUMENT_TYPES,
    BID_STATUSES,
)

from openprocurement.auctions.landlease.models.roles import (
    auction_create_role,
    auction_active_rectification_role,
    auction_edit_rectification_role,
    auction_contractTerms_create_role,
    bid_view_role,
    bid_create_role,
    bid_edit_role,
    bid_pending_role,
    bid_active_role
)


class LandLeaseAuctionDocument(dgfDocument):
    documentOf = StringType(required=True, choices=['auction'], default='auction')

    documentType = StringType(choices=AUCTION_DOCUMENT_TYPES)


class LandLeaseBidDocument(dgfDocument):
    documentOf = StringType(required=True, choices=['bid'], default='bid')

    documentType = StringType(choices=BID_DOCUMENT_TYPES)


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


def rounding_shouldStartAfter(start_after, auction, use_from=datetime(2016, 6, 1, tzinfo=TZ)):
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
        if auction.lots or auction.status not in ['active.tendering', 'active.auction']:
            return
        if self.startDate and get_now() > calc_auction_end_time(auction.numberOfBids, self.startDate):
            start_after = calc_auction_end_time(auction.numberOfBids, self.startDate)
        elif auction.tenderPeriod and auction.tenderPeriod.endDate:
            start_after = auction.tenderPeriod.endDate
        else:
            return
        return rounding_shouldStartAfter(start_after, auction).isoformat()

    def validate_startDate(self, data, startDate):
        auction = get_auction(data['__parent__'])
        if not auction.revisions and not startDate:
            raise ValidationError(u'This field is required.')


class RectificationPeriod(Period):
    invalidationDate = IsoDateTimeType()


edit_role = (edit_role + blacklist('enquiryPeriod',
                                   'tenderPeriod',
                                   'auction_value',
                                   'auction_minimalStep',
                                   'auction_guarantee',
                                   'eligibilityCriteria',
                                   'eligibilityCriteria_en',
                                   'eligibilityCriteria_ru',
                                   'awardCriteriaDetails',
                                   'awardCriteriaDetails_en',
                                   'awardCriteriaDetails_ru',
                                   'procurementMethodRationale',
                                   'procurementMethodRationale_en',
                                   'procurementMethodRationale_ru',
                                   'submissionMethodDetails',
                                   'submissionMethodDetails_en',
                                   'submissionMethodDetails_ru',
                                   'minNumberOfQualifiedBids'))

Administrator_role = (Administrator_role + whitelist('awards'))


@implementer(IBid)
class Bid(Model):
    class Options:
        roles = {
            'Administrator': Administrator_bid_role,
            'view': bid_view_role,
            'create': bid_create_role,
            'edit': bid_edit_role,
            'pending': bid_pending_role,
            'active': bid_active_role,

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

    def validate_value(self, data, value):
        auction = data['__parent__']
        if auction.value.amount != value.amount:
            raise ValidationError("Bid value amount should be equal as Auction value amount")
        if value.currency and value.currency != auction.value.currency:
            raise ValidationError("Bid value currency should be equal as Auction value currency")
        if value.valueAddedTaxIncluded != auction.value.valueAddedTaxIncluded:
            raise ValidationError("Bid value valueAddedTaxIncluded should be equal as Auction value valueAddedTaxIncluded")

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
            'active.rectification': auction_active_rectification_role,
            'edit_active.rectification': auction_edit_rectification_role,
            'edit_active.tendering': (blacklist('enquiryPeriod',
                                                'tenderPeriod',
                                                'rectificationPeriod',
                                                'auction_value',
                                                'auction_minimalStep',
                                                'auction_guarantee',
                                                'eligibilityCriteria',
                                                'eligibilityCriteria_en',
                                                'eligibilityCriteria_ru',
                                                'minNumberOfQualifiedBids') + edit_role),
            'Administrator': (whitelist('rectificationPeriod') + Administrator_role),
        }

    def __local_roles__(self):
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

    bids = ListType(ModelType(Bid), default=list())

    bankAccount = ModelType(BankAccount)

    budgetSpent = ModelType(Value, required=True)

    cancellations = ListType(ModelType(Cancellation), default=list())

    complaints = ListType(ModelType(dgfCDB2Complaint), default=list())

    contracts = ListType(ModelType(Contract), default=list())

    contractTerms = ModelType(ContractTerms,
                              required=True)

    description = StringType(required=True)

    documents = ListType(ModelType(LandLeaseAuctionDocument), default=list())

    enquiryPeriod = ModelType(Period)

    guarantee = ModelType(Guarantee, required=True)

    items = ListType(ModelType(dgfCDB2Item),
                     required=True,
                     min_size=1,
                     validators=[validate_items_uniq])

    lotIdentifier = StringType(required=True)

    lots = ListType(ModelType(Lot),
                    default=list(),
                    validators=[validate_lots_uniq, validate_not_available])

    lotHolder = ModelType(BaseOrganization, required=True)

    minNumberOfQualifiedBids = IntType(choices=[1, 2], required=True)

    mode = StringType()

    procurementMethod = StringType(choices=['open'], default='open')

    procurementMethodType = StringType(required=True)

    rectificationPeriod = ModelType(RectificationPeriod)                        # The period during which editing of main procedure fields are allowed

    registrationFee = ModelType(Value, required=True)

    status = StringType(choices=AUCTION_STATUSES, default='draft')

    submissionMethod = StringType(choices=['electronicAuction'],
                                  default='electronicAuction')

    tenderAttempts = IntType(required=True, choices=range(1, 11))

    tenderPeriod = ModelType(Period)                                            # The period when the auction is open for submissions. The end date is the closing date for auction submissions.

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
        now = get_now()
        checks = []
        if self.status == 'active.tendering' and self.tenderPeriod and self.tenderPeriod.endDate:
            checks.append(self.tenderPeriod.endDate.astimezone(TZ))
        elif not self.lots and self.status == 'active.auction' and self.auctionPeriod and self.auctionPeriod.startDate and not self.auctionPeriod.endDate:
            if now < self.auctionPeriod.startDate:
                checks.append(self.auctionPeriod.startDate.astimezone(TZ))
            elif now < calc_auction_end_time(self.numberOfBids, self.auctionPeriod.startDate).astimezone(TZ):
                checks.append(calc_auction_end_time(self.numberOfBids, self.auctionPeriod.startDate).astimezone(TZ))
        elif self.lots and self.status == 'active.auction':
            for lot in self.lots:
                if lot.status != 'active' or not lot.auctionPeriod or not lot.auctionPeriod.startDate or lot.auctionPeriod.endDate:
                    continue
                if now < lot.auctionPeriod.startDate:
                    checks.append(lot.auctionPeriod.startDate.astimezone(TZ))
                elif now < calc_auction_end_time(lot.numberOfBids, lot.auctionPeriod.startDate).astimezone(TZ):
                    checks.append(calc_auction_end_time(lot.numberOfBids, lot.auctionPeriod.startDate).astimezone(TZ))
        # Use next_check part from awarding
        request = get_request_from_root(self)
        if request is not None:
            awarding_check = request.registry.getAdapter(self, IAwardingNextCheck).add_awarding_checks(self)
            if awarding_check is not None:
                checks.append(awarding_check)
        if self.status.startswith('active'):
            from openprocurement.auctions.core.utils import calculate_business_date
            for complaint in self.complaints:
                if complaint.status == 'claim' and complaint.dateSubmitted:
                    checks.append(calculate_business_date(complaint.dateSubmitted, COMPLAINT_STAND_STILL_TIME, self))
                elif complaint.status == 'answered' and complaint.dateAnswered:
                    checks.append(calculate_business_date(complaint.dateAnswered, COMPLAINT_STAND_STILL_TIME, self))
            for award in self.awards:
                for complaint in award.complaints:
                    if complaint.status == 'claim' and complaint.dateSubmitted:
                        checks.append(calculate_business_date(complaint.dateSubmitted, COMPLAINT_STAND_STILL_TIME, self))
                    elif complaint.status == 'answered' and complaint.dateAnswered:
                        checks.append(calculate_business_date(complaint.dateAnswered, COMPLAINT_STAND_STILL_TIME, self))
        return min(checks).isoformat() if checks else None


LandLease = Auction
