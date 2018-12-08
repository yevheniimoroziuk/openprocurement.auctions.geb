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
    action_factory = None

    def __init__(self, request, context):
        self.request = request
        self.context = context

    def _validate(self, validators):
        for validator in validators:
            if not validator(self.request, context=self.context):
                return False
        return True

    def _change(self):
        modified = apply_patch(self.request, save=False, src=self.context.serialize())
        if modified:
            self.context.modified = modified
        return modified

    def change(self):
        factory = self.action_factory()
        actions = factory.get_actions(self.request, self.context)
        if actions:
            if all([self._validate(action.validators) for action in actions]):
                change = self._change()
                if change:
                    [action(self.request, self.context).act() for action in actions]
                return change


@implementer(IChangionManager)
class BaseChangionManager(object):

    def get_changer(self):
        pass

    def manage(self):
        changer = self.changer(self.request, self.context)
        changer.change()


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
