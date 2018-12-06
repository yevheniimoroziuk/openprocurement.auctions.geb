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

# actions interfaces


class IResourceAction(Interface):
    """Interface for Resource action"""


class ISubResourceAction(Interface):
    """Interface for SubResource action"""


class IAuctionAction(IResourceAction):
    """Interface for Auction Action"""


class IAuctionDocumentAction(ISubResourceAction):
    """Interface for Auction Document Action"""


class IBidDocumentAction(ISubResourceAction):
    """Interface for Bid Document Action"""


class ICancellationDocumentAction(ISubResourceAction):
    """Interface for Cancellation Document Action"""


class IQuestionAction(ISubResourceAction):
    """Interface for Question Action"""


class IItemAction(ISubResourceAction):
    """Interface for Item Action"""


class IBidAction(ISubResourceAction):
    """Interface for Bid Action"""


class ICancellationAction(ISubResourceAction):
    """Interface for Cancellation Action"""


class IActionFactory(Interface):
    """Interface for ActionFactory"""

# initializators interfaces


class IInitializator(Interface):
    """Interface for Initializators"""

# changers interfaces


class IResourceChanger(Interface):
    """interface for module auction changer"""


class ISubResourceChanger(Interface):
    """interface for module auction changer"""

# creators interfaces


class IAuctionCreationManager(Interface):
    """Interface for resource creator"""


class ISubAuctionCreationManager(Interface):
    """Interface for resource creator"""


class IAuctionCreator(Interface):
    """Interface for resource creator"""


class ISubAuctionCreator(Interface):
    """Interface for resource creator"""

# representers interfaces


class IResourceCreatedRepresenter(Interface):
    """Interface for resource creator"""


class ICreatedRepresenter(Interface):
    """Interface for resource creator"""


class ICreatedRepresentersFactory(Interface):
    """Interface for resource creator"""


# managers interfaces

# listings


class IResourceListingRepresenter(Interface):
    """Interface for Auction Listing Representer"""


class IListingRepresenter(Interface):
    """Interface for Listings Representer"""


class IListingRepresentersFactory(Interface):
    """Interface for Listings Representers Factory"""
