# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from matem.planning import _
from plone.directives import form
from plone.namedfile.field import NamedBlobFile
from plone.supermodel import model
from zope import schema

from plone.formwidget.masterselect import MasterSelectField
# from Products.Archetypes.utils import DisplayList
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.interface import directlyProvides


def PlanTypesVocabulary(context):
    items = [
        (_(u'By Text'), 'plantext'),
        (_(u'By File'), 'planfile'),
    ]

    items = [SimpleTerm(i[1], i[1], i[0]) for i in items]
    return SimpleVocabulary(items)
directlyProvides(PlanTypesVocabulary, IVocabularyFactory)


class IPlan(model.Schema):
    """Dexterity Schema for Plans."""

    title = schema.TextLine(
        title=_(u'Title'),
        required=True,
    )

    plan_type = MasterSelectField(
        title=_(u'label_plan_type', default=u'Plan type'),
        vocabulary='matem.sis.PlanTypesVocabulary',
        default='plantext',
        required=True,
        slave_fields=(
            {
                'name': 'text',
                'action': 'hide',
                'hide_values': ('planfile',),
                'siblings': True,
            },
            {
                'name': 'file',
                'action': 'hide',
                'hide_values': ('plantext',),
                'siblings': True,
            },
            {
                'name': 'textfile',
                'action': 'hide',
                'hide_values': ('plantext', 'planfile'),
                'siblings': True,
            },


        ),
    )

    form.widget('text', cols=80, rows=20)
    text = schema.Text(
        title=_(u'Text'),
        required=False,
    )

    textfile = NamedBlobFile(
        title=_(u'File'),
        required=False,
    )

    file = NamedBlobFile(
        title=_(u'File'),
        required=False,
    )
