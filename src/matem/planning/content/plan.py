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

from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime
from zope.i18n import translate


def PlanTypesVocabulary(context):
    items = [
        (_(u'By Text'), 'plantext'),
        (_(u'By File'), 'planfile'),
    ]

    items = [SimpleTerm(i[1], i[1], i[0]) for i in items]
    return SimpleVocabulary(items)
directlyProvides(PlanTypesVocabulary, IVocabularyFactory)


@provider(IContextAwareDefaultFactory)
def defaultPlanText(context):
    ''' generateWorkPlan from repordsend.py '''
    id = context.Login()
    pcatalog = getToolByName(context, 'portal_catalog')
    userl = pcatalog(portal_type='FSDPerson', id=id)
    if userl:
        if 'Investigadores' not in userl[0].getClassificationNames:
            return ''

    now = DateTime()
    projects = pcatalog(
        portal_type='CVProject',
        participantInProject=[id],
        fecha_termino={"query": [now, ], "range": "min"},
    )

    plan = []
    for p in projects:
        obj = p.getObject()
        colaboradores = obj.getInternalCollaborators()
        if obj.getInternalResponsible() and (id == obj.getInternalResponsible().id):
            role = 'responsable'
        elif id in [idss.id for idss in colaboradores]:
            role = 'colaborador'
        else:
            role = 'corresponsable'
        ptype = translate(obj.getProjectType(), 'UNAM.imateCVct', target_language='es')
        title = obj.Title()
        topics = pcatalog(portal_type='FSDSpecialty', id=[topic.id for topic in obj.getResearchTopics()])
        topics = [unicode(t.Title, 'utf-8') for t in topics]
        sponsor = translate(obj.getSponsor(), 'UNAM.imateCVct', target_language='es')
        pnumber = obj.getProjectNumber()
        c1 = u"Trabajar como %s en un proyecto de %s" % (role, ptype)
        if pnumber:
            c11 = u"con número %s, llamado %s " %(pnumber, unicode(title, 'utf-8'))
        else:
            c11 = u"llamado %s" %(unicode(title, 'utf-8'))
        c2 = u"dentro de la(s) línea(s) de investigación: %s." % ' '.join(topics)
        # c3 = u""  # TODO: faltan colaboradores
        c4 = u"Este proyecto es patrocinado por: %s.\n" % sponsor
        c5 = u"Objetivo del proyecto: %s" % unicode(obj.getAim(), 'utf-8')
        plan.append(u' '.join((c1, c11, c2, c4, c5)))
    return '\n\n'.join(plan)



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
        defaultFactory=defaultPlanText,
    )

    textfile = NamedBlobFile(
        title=_(u'File'),
        required=False,
    )

    file = NamedBlobFile(
        title=_(u'File'),
        required=False,
    )
