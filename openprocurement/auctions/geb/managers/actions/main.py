from zope.interface import implementer

from openprocurement.auctions.geb.interfaces import (
    IActionFactory
)


@implementer(IActionFactory)
class ActionFactory(object):
    """
        Base ActionFactory
    """
    actions = []

    def get_actions(self, request, context):
        """
            Factory method that returns a list of need Action instances
        """
        actions = []
        for action in self.actions:
            action_class = action.demand(request, context)
            if action_class:
                actions.append(action_class)
        return actions
