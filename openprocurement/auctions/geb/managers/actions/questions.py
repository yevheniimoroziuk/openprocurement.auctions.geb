from zope.interface import implementer

from openprocurement.auctions.geb.managers.actions.main import (
    ActionFactory
)
from openprocurement.auctions.geb.interfaces import (
    IQuestionAction,
)
from openprocurement.auctions.geb.validation import (
    validate_patch_questions
)

# question actions


@implementer(IQuestionAction)
class QuestionPatchAction(object):
    """
        This action triggered then patch question
    """
    validators = [validate_patch_questions]

    def __init__(self, request, auction, context):
        self._request = request
        self._context = context
        self._auction = auction

    @classmethod
    def demand(cls, request, context):
        if request.method == 'PATCH':
            return cls
        return False

    def act(self):
        pass

# questions actions factories


class QuestionPatchActionsFactory(ActionFactory):
    actions = (
         QuestionPatchAction,
    )
