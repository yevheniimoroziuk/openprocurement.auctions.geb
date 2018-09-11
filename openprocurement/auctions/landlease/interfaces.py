from zope.interface import (
    Interface
)

from openprocurement.auctions.core.interfaces import (
    IAuction as BaseIAuction,
    IAuctionInitializator as BaseIAuctionInitializator,
    IAuctionChanger as BaseIAuctionChanger

)


class IAuction(BaseIAuction):
    """Marker interface for LandLease auctions"""


class IAuctionInitializator(BaseIAuctionInitializator):
    """Marker interface for LandLease auctions"""


class IAuctionChanger(BaseIAuctionChanger):
    """Marker interface for LandLease auctions"""


class IAuctionChecker(Interface):
    """Marker interface for LandLease auctions"""


class IBid(Interface):
    """Marker interface for LandLease auctions"""


class IBidManager(Interface):
    """Marker interface for LandLease auctions"""


class IBidChanger(Interface):
    """Marker interface for LandLease auctions"""


class IBidInitializator(Interface):
    """Marker interface for LandLease auctions"""
