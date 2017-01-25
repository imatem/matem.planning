# -*- coding: utf-8 -*-
from matem.planning.content.interfaces import IPlanFolder
from plone.dexterity.content import Container
from zope import interface


@interface.implementer(IPlanFolder)
class PlanFolder(Container):
    """Class for plans"""

    def summary(self):
        return []
