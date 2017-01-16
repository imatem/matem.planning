# -*- coding: utf-8 -*-

from plone.dexterity.browser.view import DefaultView


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
