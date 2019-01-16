from zope.interface import implementer
from openprocurement.auctions.geb.interfaces import (
    ICreationManager,
    IResourceCreator
)

# base creator factory


class CreatorsFactory(object):
    """
        Creators Factory
    """
    def __init__(self, request, context, creators):
        self.request = request
        self.context = context
        self.creators = creators

    def __call__(self, applicant):
        if 'file' in self.request.validated:
            applicant = type(self.context).documents.model_class()

        for creator in self.creators:
            if creator.resource_interface.providedBy(applicant):
                return creator

# base creators


@implementer(ICreationManager)
class BaseCreationManager(object):
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
        factory = self.factory(self.request, self.context, self.creators)
        creator_type = factory(applicant)
        creator = creator_type(self.request, self.context)
        return creator.create(applicant)


# auction resources creator

@implementer(IResourceCreator)
class BaseCreator(object):
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
