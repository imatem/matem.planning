# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from matem.planning import _
from plone.supermodel import model
from zope import schema


class IPlan(model.Schema):
    """Dexterity Schema for Plans."""

    title = schema.TextLine(
        title=_(u'Title'),
        required=True,
    )

    description = schema.Text(
        title=_(u'Description'),
        required=False,
    )

    file = schema.Text(
        title=_(u'Description'),
        required=False,
    )
