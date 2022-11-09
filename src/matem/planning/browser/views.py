# -*- coding: utf-8 -*-

from plone.dexterity.browser.view import DefaultView
from plone import api


class PlanView(DefaultView):
    """The default view for plans."""

    def hasfile(self):
        if self.context.plan_type == 'plantext':
            if self.context.textfile:
                return True
            return False
        else:
            if self.context.file:
                return True
            return False

    def getFile(self):
        if self.context.plan_type == 'plantext':
            return self.context.textfile

        return self.context.file

    def candownload(self):
        current_state = api.content.get_state(self.context)
        if current_state == 'sended':
            return True
        return False