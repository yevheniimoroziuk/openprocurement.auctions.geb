from zope.interface import implementer
from openprocurement.auctions.core.interfaces import (
    INamedValidators
)


@implementer(INamedValidators)
class NamedValidators():

    def __init__(self, name, validators):
        self.name = name
        self.validators = validators
