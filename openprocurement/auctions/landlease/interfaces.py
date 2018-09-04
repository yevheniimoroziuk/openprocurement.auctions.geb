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
