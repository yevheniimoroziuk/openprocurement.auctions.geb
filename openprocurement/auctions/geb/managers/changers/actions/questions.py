from openprocurement.auctions.geb.validation import (
    validate_patch_questions,
)
from openprocurement.auctions.geb.managers.changers.base import (
    BaseAction
)


class QuestionPatchAction(BaseAction):
    """
        This action triggered then patch question
    """
    validators = [validate_patch_questions]

    @classmethod
    def demand(cls, request, context):
        if request.method == 'PATCH':
            return cls
        return False

    def act(self):
        pass
