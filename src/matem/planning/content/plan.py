# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from matem.planning import _
from plone.directives import form
from plone.namedfile.field import NamedBlobFile
from plone.supermodel import model
from zope import schema


class IPlan(model.Schema):
    """Dexterity Schema for Plans."""

    title = schema.TextLine(
        title=_(u'Title'),
        required=True,
    )

    form.widget('text', cols=80, rows=20)
    text = schema.Text(
        title=_(u'Text'),
        required=False,
    )

    file = NamedBlobFile(
        title=_(u'File'),
        required=False,
    )
