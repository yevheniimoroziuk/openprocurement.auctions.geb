from zope.interface import (
    Interface
)

from openprocurement.auctions.core.interfaces import (
    IAuction as BaseIAuction,
)


class IAuction(BaseIAuction):
    """Marker interface for LandLease auctions"""


class IAuctionInitializator(Interface):
    """Marker interface for LandLease auctions"""


class IAuctionChanger(Interface):
    """Marker interface for LandLease auctions"""


class IAuctionChecker(Interface):
    """Marker interface for LandLease auctions"""


class IAuctionDocumenter(Interface):
    """Marker interface for LandLease auctions"""


class IBid(Interface):
    """Marker interface for LandLease auctions"""


class IBidManager(Interface):
    """Marker interface for LandLease auctions"""


class IBidChanger(Interface):
    """Marker interface for LandLease auctions"""


class IBidDeleter(Interface):
    """Marker interface for LandLease auctions"""


class IBidInitializator(Interface):
    """Marker interface for LandLease auctions"""
