from zope.interface import Interface
from openprocurement.auctions.core.interfaces import IAuction as BaseIAuction


class IAuction(BaseIAuction):
    """Interface for Geb Auction"""


class IBid(Interface):
    """Interface for Geb Bid"""


class IItem(Interface):
    """Interface for Geb Item"""


class IContract(Interface):
    """Interface for Geb Contract"""


class IDocument(Interface):
    """Interface for Geb Document"""


class IBidDocument(Interface):
    """Interface for Geb Bid Document"""


class IQuestion(Interface):
    """Interface for Geb Questions"""


class ICancellation(Interface):
    """Interface for Geb Cancellations"""


class ICancellationDocument(Interface):
    """Interface for Geb Cancellation Document"""
