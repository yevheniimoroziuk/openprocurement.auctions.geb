# -*- coding: utf-8 -*-
from openprocurement.auctions.core.utils import (
    json_view,
    context_unpack,
    opresource
)
from openprocurement.auctions.core.validation import (
    validate_question_data,
    validate_patch_question_data,
)

from openprocurement.auctions.core.interfaces import (
    IManager
)

from openprocurement.auctions.core.views.mixins import (
    AuctionQuestionResource
)


@opresource(name='geb:Auction Questions',
            collection_path='/auctions/{auction_id}/questions',
            path='/auctions/{auction_id}/questions/{question_id}',
            auctionsprocurementMethodType="geb",
            description="Auction questions")
class AuctionQuestionResource(AuctionQuestionResource):

    @json_view(content_type="application/json", validators=(validate_question_data,), permission='create_question')
    def collection_post(self):
        """
        Post a question
        """
        save = None

        manager = self.request.registry.queryMultiAdapter((self.request, self.context), IManager)

        applicant = self.request.validated['question']
        question = manager.create(applicant)
        if question:
            save = manager.save()

        if save:
            msg = 'Created auction question {}'.format(question['id'])
            extra = context_unpack(self.request, {'MESSAGE_ID': 'auction_question_create'}, {'question_id': question['id']})
            self.LOGGER.info(msg, extra=extra)

            self.request.response.status = 201

            route = self.request.matched_route.name.replace("collection_", "")
            location = self.request.current_route_url(_route_name=route, question_id=question['id'], _query={})
            self.request.response.headers['Location'] = location
            return {'data': question.serialize("view")}

    @json_view(content_type="application/json", permission='edit_auction', validators=(validate_patch_question_data,))
    def patch(self):
        """
        Post an Answer
        """
        question = self.request.context

        manager = self.request.registry.queryMultiAdapter((self.request, self.context), IManager)

        manager.change()
        save = manager.save()

        if save:
            extra = context_unpack(self.request, {'MESSAGE_ID': 'auction_question_patch'})
            msg = 'Updated auction question {}'.format(self.request.context.id)
            self.LOGGER.info(msg, extra=extra)
            return {'data': question.serialize(question.__parent__.status)}
