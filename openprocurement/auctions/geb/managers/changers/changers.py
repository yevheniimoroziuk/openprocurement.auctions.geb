from openprocurement.auctions.core.utils import (
    apply_patch,
    upload_file,
    get_now
)
from openprocurement.auctions.geb.managers.changers.base import (
    BaseResourceChanger
)
from openprocurement.auctions.geb.managers.changers.actions.auction import (
    AuctionPhaseCommitAction,
    AuctionPatchDraftAction,
    AuctionPatchActiveRectificationAction,
    AuctionPatchAction,
    ModuleAuctionBringsAction,
    ModuleAuctionUpdateUrlsAction,
    ChronographPatchAction,
    EndActiveEnquiryAction,
    EndActiveRectificationAction,
    EndActiveTenderingAction,
    SetAuctionPeriodStartDateAction
)
from openprocurement.auctions.geb.managers.changers.actions.auction import (
    BidActivationAction,
    BidActivePatchAction,
    BidDraftPatchAction,
    BidMakeActiveStatusAction,
    BidPatchAction,
    BidPendingPatchAction
)

from openprocurement.auctions.geb.managers.changers.actions.cancellation import (
    CancellationActivationAction
)
from openprocurement.auctions.geb.managers.changers.actions.documents import (
    AuctionDocumentPutAction,
    AuctionDocumentPatchAction
)
from openprocurement.auctions.geb.managers.changers.actions.bid import (
    BidDocumentPatchAction
)
from openprocurement.auctions.geb.managers.changers.actions.questions import (
    QuestionPatchAction
)
from openprocurement.auctions.geb.managers.changers.actions.items import (
    ItemPatchAction
)

# auction changers


class AuctionChanger(BaseResourceChanger):
    """
        Auction changer
        trigger when patch auction
    """
    actions = (
        AuctionPhaseCommitAction,
        AuctionPatchDraftAction,
        AuctionPatchActiveRectificationAction,
        AuctionPatchAction
    )


class ModuleAuctionChanger(BaseResourceChanger):
    """
        Module auction changer
        trigger when module auction change auction
    """
    actions = (
        ModuleAuctionBringsAction,
        ModuleAuctionUpdateUrlsAction
    )

    def _change(self):
        """
            When results come, it is end of auctionPerion
        """
        self.context.auctionPeriod['endDate'] = get_now()

        modified = apply_patch(self.request, save=False, src=self.context.serialize())
        if modified:
            self.context.modified = modified
        return modified


class ChronographChanger(BaseResourceChanger):
    """
        Chronograph changer
        trigger when chronograph change auction
    """
    actions = (
        ChronographPatchAction,
        EndActiveEnquiryAction,
        EndActiveRectificationAction,
        EndActiveTenderingAction,
        SetAuctionPeriodStartDateAction
    )


class BidChanger(BaseResourceChanger):
    """
        Bid patch changer
        trigger when patch bid
    """
    actions = (
        BidActivationAction,
        BidActivePatchAction,
        BidDraftPatchAction,
        BidMakeActiveStatusAction,
        BidPatchAction,
        BidPendingPatchAction
    )


class CancellationChanger(BaseResourceChanger):
    """
        Cancellation patch changer
        trigger when patch cancellation
    """
    actions = (
        CancellationActivationAction,
    )


class AuctionDocumentChanger(BaseResourceChanger):
    """
        Auction Document patch changer
        trigger when patch auction document
    """
    actions = (
         AuctionDocumentPatchAction,
    )


class AuctionDocumentPutChanger(BaseResourceChanger):
    """
        Auction Document put changer
        trigger when put auction document
    """

    actions = (
         AuctionDocumentPutAction,
    )

    def _change(self):
        document = upload_file(self._request)
        self._auction.documents.append(document)
        self._auction.modified = True
        return document


class BidDocumentChanger(BaseResourceChanger):
    """
        Bid Document patch changer
        trigger when patch bid document
    """

    actions = (
         BidDocumentPatchAction,
    )


class QuestionChanger(BaseResourceChanger):
    """
        Question patch changer
        trigger when patch  question
    """
    actions = (
         QuestionPatchAction,
    )


class ItemChanger(BaseResourceChanger):
    """
        Item patch changer
        trigger when patch item
    """
    actions = (
        ItemPatchAction,
    )
