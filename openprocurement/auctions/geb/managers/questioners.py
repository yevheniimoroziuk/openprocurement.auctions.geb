
from zope.interface import implementer

from openprocurement.auctions.core.interfaces import (
    IAuctionQuestioner
)

from openprocurement.auctions.geb.validation import (
    validate_question_adding_period
)


@implementer(IAuctionQuestioner)
class AuctionQuestioner(object):
    name = 'Auction Questioner'
    validators = [validate_question_adding_period]

    def __init__(self, request, context):
        self._request = request
        self._context = context

    def validate(self):
        for validator in self.validators:
            if not validator(self._request):
                return
        return True

    def add_question(self):
        if self.validate():
            question = self._request.validated['question']
            self._context.questions.append(question)
            return question
