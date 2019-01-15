# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, time
from uuid import uuid4

from schematics.exceptions import ValidationError
from schematics.types import (
    StringType,
    IntType,
    MD5Type,
    BooleanType,
    URLType,
)

from schematics.types.compound import ModelType
from schematics.types.serializable import serializable
from pyramid.security import Allow
from zope.interface import implementer

from openprocurement.auctions.core.models import (
    Administrator_bid_role,
    Auction as BaseAuction,
    BankAccount,
    BaseOrganization,
    Classification,
    Guarantee,
    DecimalType,
    IsoDateTimeType,
    IsoDurationType,
    ListType,
    Model,
    Period,
    Question as BaseQuestion,
    Value,
    dgfCDB2Complaint as BaseComplaint,
    dgfCDB2Item as BaseItem,
    dgfDocument as BaseDocument,
    dgfCancellation as BaseCancellation,
    validate_items_uniq
)
from openprocurement.auctions.core.plugins.awarding.v3_1.models import Award
from openprocurement.auctions.core.plugins.contracting.v3_1.models import Contract as BaseContract
from openprocurement.auctions.core.utils import (
    SANDBOX_MODE,
    TZ,
    get_now
)
from openprocurement.auctions.core.validation import (
    cpvs_validator,
    kvtspz_validator
)

from openprocurement.auctions.geb.interfaces import (
    IAuction,
    IBid,
    ICancellation,
    ICancellationDocument,
    IDocument,
    IBidDocument,
    IItem,
    IContract,
    IQuestion
)


from openprocurement.auctions.geb.constants import (
    AUCTION_DOCUMENT_TYPES,
    CANCELLATION_DOCUMENT_TYPES,
    AUCTION_STATUSES,
    BID_DOCUMENT_TYPES,
    BID_STATUSES,
    ITEM_ADDITIONAL_CLASSIFICATIONS_TYPES
)

from openprocurement.auctions.geb.models.roles import (
    auction_administrator_role,
    auction_contractTerms_create_role,
    auction_create_role,
    auction_draft_role,
    auction_edit_enquiry_role,
    auction_edit_rectification_role,
    auction_edit_tendering_role,
    auction_edit_draft_role,
    auction_enquiry_role,
    auction_rectification_role,
    auction_tendering_role,
    bid_active_auction_role,
    bid_active_awarded_role,
    bid_active_enquiry_role,
    bid_active_qualification_role,
    bid_active_role,
    bid_active_tendering_role,
    bid_create_role,
    bid_edit_active_role,
    bid_edit_draft_role,
    bid_edit_pending_role,
    bid_pending_role,
    bid_view_role,
    chronograph_view_role,
    item_edit_role,
    item_view_role,
    question_enquiry_role,
    question_rectification_role
)

from openprocurement.auctions.geb.validation import (
    cav_ps_code_validator
)
from openprocurement.auctions.geb.utils import (
    calc_expected_auction_end_time
)


@implementer(IDocument)
class AuctionDocument(BaseDocument):

    documentOf = StringType(required=True, choices=['auction'], default='auction')

    documentType = StringType(choices=AUCTION_DOCUMENT_TYPES)


@implementer(ICancellationDocument)
class CancellationDocument(BaseDocument):

    documentOf = StringType(required=True, choices=['cancellation'], default='cancellation')

    documentType = StringType(choices=CANCELLATION_DOCUMENT_TYPES)


@implementer(IBidDocument)
class BidDocument(BaseDocument):
    documentOf = StringType(required=True, choices=['bid'], default='bid')

    documentType = StringType(choices=BID_DOCUMENT_TYPES)


@implementer(ICancellation)
class Cancellation(BaseCancellation):
    documents = ListType(ModelType(CancellationDocument), default=list())


@implementer(IQuestion)
class Question(BaseQuestion):

    class Options:
        roles = {
            'active.enquiry': question_enquiry_role,
            'active.rectification': question_rectification_role
        }
    questionOf = StringType(required=True, choices=['tender'], default='tender')


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
        auctionPeriod = self

        # in status 'auctionPeriod.startDate' we don`t need shouldStartAfter
        if auctionPeriod.endDate:
            return

        auction = auctionPeriod.__parent__

        # in status 'draft' we don`t need shouldStartAfter
        if auction.status in ['draft'] or not auction.enquiryPeriod:
            return

        should_start_after = auction.enquiryPeriod.endDate
        if auctionPeriod.startDate:
            # calculate expected auction end time
            expected_end_time_of_auction = calc_expected_auction_end_time(auctionPeriod.startDate)
            now = get_now()
            # check if auction not happen
            if now > expected_end_time_of_auction:  # TODO test replaning
                should_start_after = expected_end_time_of_auction
        return rounding_shouldStartAfter(should_start_after, auction).isoformat()


class RectificationPeriod(Period):
    invalidationDate = IsoDateTimeType()


@implementer(IBid)
class Bid(Model):
    class Options:
        roles = {
            'Administrator': Administrator_bid_role,
            'active': bid_active_role,
            'active.auction': bid_active_auction_role,
            'active.awarded': bid_active_awarded_role,
            'active.enquiry': bid_active_enquiry_role,
            'active.qualification': bid_active_qualification_role,
            'active.tendering': bid_active_tendering_role,
            'create': bid_create_role,
            'draft': bid_view_role,
            'unsuccessful': bid_view_role,
            'edit_active': bid_edit_active_role,
            'edit_draft': bid_edit_draft_role,
            'edit_pending': bid_edit_pending_role,
            'pending': bid_pending_role,
            'view': bid_view_role,
        }

    bidNumber = IntType()
    date = IsoDateTimeType()
    documents = ListType(ModelType(BidDocument), default=list())
    id = MD5Type(required=True, default=lambda: uuid4().hex)
    changed = False
    owner = StringType()
    owner_token = StringType()
    participationUrl = URLType()
    qualified = BooleanType()
    status = StringType(choices=BID_STATUSES, default='draft')
    tenderers = ListType(ModelType(BaseOrganization), required=True, min_size=1, max_size=1)
    value = ModelType(Value)

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
        if auction.value.amount != value.amount and auction.status in ('active.tendering', 'active.enquiry'):
            raise ValidationError("Bid value amount should be equal as Auction value amount")
        if value.currency and value.currency != auction.value.currency:
            raise ValidationError("Bid value currency should be equal as Auction value currency")
        if value.valueAddedTaxIncluded != auction.value.valueAddedTaxIncluded:
            raise ValidationError("Bid value valueAddedTaxIncluded should be equal as Auction value valueAddedTaxIncluded")

    def validate_bidNumber(self, data, bidNumber):
        # validate bidNumber
        # bid owner must set the unique value of bidNumber
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


class GebClassification(Classification):
    scheme = StringType(required=True, default='CAV-PS', choices=['CAV-PS'])
    _id_field_validators = Classification._id_field_validators + (cav_ps_code_validator,)


class GebAdditionalClassification(Classification):
    scheme = StringType(required=True, choices=ITEM_ADDITIONAL_CLASSIFICATIONS_TYPES)
    _id_field_validators = Classification._id_field_validators + (cpvs_validator,
                                                                  kvtspz_validator)


@implementer(IItem)
class Item(BaseItem):
    class Options:
        roles = {
            'edit': item_edit_role,
            'view': item_view_role

        }
    classification = ModelType(GebClassification,
                               required=True)
    additionalClassifications = ListType(ModelType(GebAdditionalClassification), required=True)
    quantity = DecimalType(precision=-4)

    def validate_additionalClassifications(self, data, classificator):
        classificators = data['additionalClassifications']
        need_schemas = {'kvtspz', 'cadastralNumber'}
        schemas = set([classificator.scheme for classificator in classificators])

        if not need_schemas.issubset(schemas):
            err_msg = 'At least must be two additional classifications (kvtspz, cadastralNumber)'
            raise ValidationError(err_msg)


@implementer(IContract)
class Contract(BaseContract):

    items = ListType(ModelType(Item))


@implementer(IAuction)
class Auction(BaseAuction):

    class Options:
        roles = {
            'create': auction_create_role,

            'draft': auction_draft_role,
            'edit_draft': auction_edit_draft_role,

            'active.rectification': auction_rectification_role,
            'edit_active.rectification': auction_edit_rectification_role,

            'active.tendering': auction_tendering_role,
            'edit_active.tendering': auction_edit_tendering_role,

            'chronograph_view': chronograph_view_role,


            'active.enquiry': auction_enquiry_role,
            'edit_active.enquiry': auction_edit_enquiry_role,

            'Administrator': auction_administrator_role,
        }

    def __local_roles__(self):                                                  # TODO rm black box
        roles = dict([('{}_{}'.format(self.owner, self.owner_token), 'auction_owner')])
        for i in self.bids:
            roles['{}_{}'.format(i.owner, i.owner_token)] = 'bid_owner'
        return roles

    _internal_type = "geb"
    auctionParameters = ModelType(AuctionParameters)
    auctionPeriod = ModelType(AuctionAuctionPeriod, required=True, default={})
    awardCriteria = StringType(choices=['highestCost'], default='highestCost')
    awards = ListType(ModelType(Award), default=list())
    bankAccount = ModelType(BankAccount)
    bids = ListType(ModelType(Bid), default=list())
    budgetSpent = ModelType(Value, required=True)
    cancellations = ListType(ModelType(Cancellation), default=list())
    complaints = ListType(ModelType(BaseComplaint), default=list())
    contractTerms = ModelType(ContractTerms, required=True)
    contracts = ListType(ModelType(Contract), default=list())
    dateModified = IsoDateTimeType()
    description = StringType(required=True)
    documents = ListType(ModelType(AuctionDocument), default=list())
    enquiryPeriod = ModelType(Period)
    guarantee = ModelType(Guarantee, required=True)
    items = ListType(ModelType(Item), validators=[validate_items_uniq], default=list())
    lotHolder = ModelType(BaseOrganization, required=True)
    lotIdentifier = StringType(required=True)
    minNumberOfQualifiedBids = IntType(choices=[1, 2], default=2)
    mode = StringType()
    changed = False
    procurementMethod = StringType(choices=['open'], default='open')
    procurementMethodType = StringType(required=True)
    questions = ListType(ModelType(Question), default=list())
    rectificationPeriod = ModelType(RectificationPeriod)
    registrationFee = ModelType(Guarantee, required=True)
    status = StringType(choices=AUCTION_STATUSES, default='draft')
    submissionMethod = StringType(choices=['electronicAuction'], default='electronicAuction')
    tenderAttempts = IntType(choices=range(1, 11))
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

    def validate_enquiryPeriod(self, data, period):
        if not period:
            return

    def validate_rectificationPeriod(self, data, period):
        if not period:
            return

    def validate_value(self, data, value):
        if value.currency != u'UAH':
            raise ValidationError(u"currency should be only UAH")

    def validate_minimalStep(self, data, minimalStep):
        if minimalStep.amount >= data['value'].amount:
            raise ValidationError(u"miniamalStep.amount should be less than value.amount")
        if minimalStep.valueAddedTaxIncluded != data['value'].valueAddedTaxIncluded:
            raise ValidationError(u"minimalStep.valueAddedTaxIncluded should be the same as value.valueAddedTaxIncluded")
        if minimalStep.currency != u'UAH':
            raise ValidationError(u"currency should be only UAH")

    @serializable(serialize_when_none=False)
    def next_check(self):
        check = None
        if self.status == 'active.rectification' and self.rectificationPeriod:
            check = self.rectificationPeriod.endDate.astimezone(TZ)
        elif self.status == 'active.tendering' and self.tenderPeriod:
            check = self.tenderPeriod.endDate.astimezone(TZ)
        elif self.status == 'active.enquiry' and self.enquiryPeriod:
            check = self.enquiryPeriod.endDate.astimezone(TZ)

        return check.isoformat() if check else None


Geb = Auction
