# -*- coding: utf-8 -*-

from plone.dexterity.browser.view import DefaultView


class PlanView(DefaultView):
    """The default view for plans."""

    def hasfile(self):
        if self.context.file:
            return True
        return False
