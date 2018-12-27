from zope.interface import (
    implementer,
    implementedBy
)

from openprocurement.auctions.geb.interfaces import (
    ICreatedRepresenter,
    IListingRepresenter,
    IResourceRepresenter,
    IRepresentersFactory,
    IRepresentationManager
)


@implementer(IResourceRepresenter)
class BaseResourceRepresenter(object):

    def __init__(self, request, context):
        self.request = request
        self.context = context

    def get_representation_role(self):
        pass

    def represent(self):
        role = self.get_representation_role()
        return {'data': self.context.serialize(role)}


@implementer(ICreatedRepresenter)
class BaseCreatedRepresenter(object):

    def __init__(self, request, context):
        self.request = request
        self.context = context

    def represent(self, created):
        pass


@implementer(IListingRepresenter)
class BaseListingRepresenter(object):

    def __init__(self, request, context):
        self.request = request
        self.context = context

    def represent(self):
        pass


@implementer(IRepresentersFactory)
class RepresentersFactory():
    """
        Base listings representer factory
    """

    def __init__(self, representers):
        self.representers = representers

    def __call__(self, implamented):
        for representer in self.representers:
            if representer.resource_interface in implamented:
                return representer


@implementer(IRepresentationManager)
class BaseRepresentationManager(object):
    factory = RepresentersFactory
    listings_representers = []
    created_representers = []
    representer = None

    def __init__(self, request, context):
        self.request = request
        self.context = context

    def represent_created(self, created):
        factory = self.factory(self.created_representers)
        implamented = implementedBy(created.__class__)
        representer_type = factory(implamented)
        representer = representer_type(self.request, self.context)
        return representer.represent(created)

    def represent_listing(self, implamented):
        factory = self.factory(self.listing_representers)
        representer_type = factory(implamented)
        representer = representer_type(self.request, self.context)
        return representer.represent()

    def represent(self):
        representer = self.representer(self.request, self.context)
        return representer.represent()
