from zope.interface import implementer
from openprocurement.auctions.geb.interfaces import (
    IDeletionManager,
    IResourceDeleter
)


@implementer(IResourceDeleter)
class BaseResourceDeleter(object):
    validators = []

    def validate(self):
        for validator in self.validators:
            if not validator(self.request, context=self.context):
                return False
        return True

    def __init__(self, request, context):
        self.request = request
        self.context = context

    def delete(self):
        pass


@implementer(IDeletionManager)
class BaseDeletionManager(object):
    deleter = None

    def __init__(self, request, context):
        self.request = request
        self.context = context

    def manage(self):
        deleter = self.deleter(self.request, self.context)
        return deleter.delete()
