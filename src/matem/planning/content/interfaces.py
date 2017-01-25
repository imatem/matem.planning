# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""
from matem.planning import _
from plone.supermodel import model
from zope import schema


class IPlanFolder(model.Schema):
    """Dexterity-schema for Folders of plan."""

    title = schema.TextLine(
        title=_(u'Title'),
        required=True,
    )

    description = schema.Text(
        title=_(u'Description'),
        required=False,
    )
