from zope.interface import Interface
from openprocurement.auctions.core.interfaces import IAuction as BaseIAuction


# resourse interfaces

class IAuction(BaseIAuction):
    """Interface for Geb Auction"""


class IBid(Interface):
    """Interface for Geb Bid"""


class IItem(Interface):
    """Interface for Geb Item"""


class IContract(Interface):
    """Interface for Geb Contract"""


class IAuctionDocument(Interface):
    """Interface for Geb Document"""


class IBidDocument(Interface):
    """Interface for Geb Bid Document"""


class IQuestion(Interface):
    """Interface for Geb Questions"""


class ICancellation(Interface):
    """Interface for Geb Cancellations"""


class ICancellationDocument(Interface):
    """Interface for Geb Cancellation Document"""

# changers interfaces


class IResourceChanger(Interface):
    """interface for module auction changer"""


class IChangionManager(Interface):
    """Interface for resource creator"""


class IAction(Interface):
    """Interface for resource creator"""

# creators interfaces


class ICreationManager(Interface):
    """Interface for resource creator"""


class IResourceCreator(Interface):
    """Interface for resource creator"""

# deletors interfaces


class IDeletionManager(Interface):
    """Interface for resource creator"""


class IResourceDeleter(Interface):
    """Interface for resource creator"""

# representers interfaces


class IResourceRepresenter(Interface):
    """Interface for resource creator"""


class ICreatedRepresenter(Interface):
    """Interface for resource creator"""


class IListingRepresenter(Interface):
    """Interface for resource creator"""


class IRepresentersFactory(Interface):
    """Interface for resource creator"""


class IRepresentationManager(Interface):
    """Interface for resource creator"""


# logger interfaces

class IResourceLogger(Interface):
    """Interface for resource creator"""
