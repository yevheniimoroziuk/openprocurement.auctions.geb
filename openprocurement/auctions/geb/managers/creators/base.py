from zope.interface import implementer
from openprocurement.auctions.geb.interfaces import (
    IAuctionCreationManager,
    ISubAuctionCreationManager,
    IAuctionCreator,
    ISubAuctionCreator
)

# base creator factory


class CreatorsFactory(object):
    """
        Creators Factory
    """
    def __init__(self, creators):
        self.creators = creators

    def __call__(self, applicant):
        for creator in self.creators:
            if creator.resource_interface.providedBy(applicant):
                return creator

# base creators


@implementer(IAuctionCreationManager)
class BaseAuctionCreationManager(object):
    """
        Auction Creator
        Creator for resource auction
    """
    creators = []
    factory = CreatorsFactory

    def __init__(self, request, context):
        self.request = request
        self.context = context

    def manage(self, applicant):
        factory = self.factory(self.creators)
        creator_type = factory(applicant)
        creator = creator_type(self.request, self.context)
        return creator.create(applicant)


@implementer(ISubAuctionCreationManager)
class BaseSubAuctionCreationManager(object):
    """
        SubAuction Creator
        Creator for subresources of auction
    """
    creators = []
    factory = CreatorsFactory

    def __init__(self, request, auction, context):
        self.request = request
        self.context = context
        self.auction = auction

    def manage(self, applicant):
        factory = self.factory(self.creators)
        creator_type = factory(applicant)
        creator = creator_type(self.request, self.auction, self.context)
        return creator.create(applicant)


# auction resources creator

@implementer(IAuctionCreator)
class BaseAuctionCreator(object):
    """
        Creator for auction resource
        such as [Item, Cancellation, Bid, Question]
    """
    resource_interface = None
    validators = []

    def __init__(self, request, context):
        self.request = request
        self.context = context

    def _validate(self):
        for validator in self.validators:
            if not validator(self.request, context=self.context):
                return False
        return True

    def _create(self, applicant):
        pass

    def create(self, applicant):
        if self._validate():
            created = self._create(applicant)
            return created

# sub-auction resources creators


@implementer(ISubAuctionCreator)
class BaseSubAuctionCreator(object):
    """
        Creator for sub-auction resources
        such as [CancellationDocument, BidDocument, ItemDocument]
    """
    resource_interface = None
    validators = []

    def __init__(self, request, auction, context):
        self.request = request
        self.context = context
        self.auction = auction

    def _validate(self):
        for validator in self.validators:
            if not validator(self.request, auction=self.auction, context=self.context):
                return False
        return True

    def _create(self, applicant):
        pass

    def create(self, applicant):
        if self._validate():
            created = self._create(applicant)
            return created
