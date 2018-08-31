from openprocurement.auctions.core.interfaces import (
    IAuction as BaseIAuction,
    IAuctionInitializator as BaseIAuctionInitializator
)


class IAuction(BaseIAuction):
    """Marker interface for LandLease auctions"""


class IAuctionInitializator(BaseIAuctionInitializator):
    """Marker interface for LandLease auctions"""
