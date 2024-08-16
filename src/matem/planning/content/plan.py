# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from collective.z3cform.datagridfield import DictRow
from collective.z3cform.datagridfield.datagridfield import DataGridFieldFactory
from DateTime import DateTime
from matem.planning import _
from matem.planning.validators import isValidFileType
from Products.CMFCore.utils import getToolByName
from plone.autoform import directives
from plone.directives import form
from plone.formwidget.masterselect import MasterSelectField
from plone.namedfile.field import NamedBlobFile
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from zope import schema
from zope.interface import directlyProvides
from zope.interface import Interface
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
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
    try:
        id = context.Login()
    except AttributeError:
        return u''
    pcatalog = getToolByName(context, 'portal_catalog')
    userl = pcatalog(portal_type='FSDPerson', id=id)
    if userl:
        if 'Investigadores' not in userl[0].getClassificationNames:
            return u''

    now = DateTime('2024/01/01')
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
        if sponsor.lower() == 'interno':
            sponsor = 'UNAM (Interno)'
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


class IConferenceInfo(Interface):
    conference_title = schema.TextLine(
        title=_(u'label_conference_title', default=u'Título'),
        required=False,
    )

    conference_month = schema.Choice(
        title=_(u'label_conference_month', default=u'Mes probable de realización'),
        vocabulary="matem.cv.vocabularies.MonthsVocabularyFactory",
        required=False,
    )

    conference_institution = schema.TextLine(
        title=_(u'label_conference_institution', default=u'Institución'),
        required=False,
    )

    conference_scope = schema.Choice(
        title=_(u'label_conference_', default=u'Ambito'),
        vocabulary="matem.cv.vocabularies.EventType",
        required=False,
    )


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
                'name': 'teaching',
                'action': 'hide',
                'hide_values': ('planfile',),
                'siblings': True,
            },
            {
                'name': 'students',
                'action': 'hide',
                'hide_values': ('planfile',),
                'siblings': True,
            },
            {
                'name': 'divulgacion',
                'action': 'hide',
                'hide_values': ('planfile',),
                'siblings': True,
            },
            {
                'name': 'notes',
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
            {
                'name': 'conferences',
                'action': 'hide',
                'hide_values': ('planfile',),
                'siblings': True,
            },


        ),
    )

    form.widget('text', cols=80, rows=15)
    text = schema.Text(
        title=_(u'Research'),
        description=_(
            u'label_help_text',
            u'You can use article latex format. Packages included are: latexsym and amsmath'
        ),
        required=False,
        defaultFactory=defaultPlanText,
    )

    form.widget('teaching', cols=80, rows=10)
    teaching = schema.Text(
        title=_(u'Teaching'),
        required=False,
    )

    form.widget('students', rows=10)
    students = schema.Text(
        title=_(u'Formación de recursos humanos'),
        required=False,
    )

    form.widget('divulgacion', rows=10)
    divulgacion = schema.Text(
        title=_(u'Divulgación, vinculación'),
        required=False,
    )

    form.widget('notes', rows=5)
    notes = schema.Text(
        title=_(u'otros/comentarios'),
        required=False,
    )

    textfile = NamedBlobFile(
        title=_(u'File'),
        required=False,
    )

    file = NamedBlobFile(
        title=_(u'File'),
        required=False,
        constraint=isValidFileType,
    )

    directives.omitted('thumbpdf')
    thumbpdf = NamedBlobImage(
        title=_(u'ImageThumb'),
        required=False,
    )

    form.widget(
        'conferences',
        DataGridFieldFactory,
        allow_reorder=True,
        # allow_insert=False,
        # allow_delete=False,
        # auto_append=False,
    )
    conferences = schema.List(
        title=_(u'label_conferences', u'Actividades Académicas a organizar'),
        value_type=DictRow(title=_(u'Conferencia'), schema=IConferenceInfo),
        required=False,
    )
