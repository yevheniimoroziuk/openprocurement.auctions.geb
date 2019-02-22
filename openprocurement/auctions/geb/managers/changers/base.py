from zope.interface import implementer

from openprocurement.auctions.core.utils import (
    apply_patch
)
from openprocurement.auctions.geb.interfaces import (
    IResourceChanger,
    IChangionManager,
    IAction
)


@implementer(IResourceChanger)
class BaseResourceChanger(object):
    actions = []

    def __init__(self, request, context):
        self.request = request
        self.context = context

    def _validate(self, validators):
        for validator in validators:
            if not validator(self.request, context=self.context):
                return False
        return True

    def get_actions(self):
        actions = []

        for action_type in self.actions:
            action = action_type.demand(self.request, self.context)
            if action:
                action_obj = action(self.request, self.context)
                actions.append(action_obj)
        return actions

    def _change(self):
        modified = apply_patch(self.request, save=False, src=self.context.serialize())
        return modified

    def change(self):
        actions = self.get_actions()
        if actions:
            if all([self._validate(action.validators) for action in actions]):
                change = self._change()
                if change:
                    _ = [action.act() for action in actions]
                return change


@implementer(IChangionManager)
class BaseChangionManager(object):
    changer = None

    def __init__(self, request, context):
        self.request = request
        self.context = context

    def manage(self):
        changer = self.changer(self.request, self.context)
        return changer.change()


@implementer(IAction)
class BaseAction(object):

    def __init__(self, request, context):
        self.request = request
        self.context = context

    @classmethod
    def demand(cls, request, context):
        pass

    def act(self):
        pass
