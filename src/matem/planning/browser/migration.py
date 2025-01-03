# -*- coding: utf-8 -*-

from datetime import date
from plone import api
from z3c.form import button
from z3c.form import form
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
from matem.planning.content.plan import defaultPlanText
import logging


logger = logging.getLogger('Plone')


class MigrationForm(form.Form):

    @button.buttonAndHandler(u'Migrate Plans')
    def handle_migrate_plans(self, action):
        logger.info('moving plans ...')
        plans_path = '/acerca-de/estructura-interna/secretaria-academica/informes/planes'
        plans = api.content.get(path=plans_path)
        transforms = api.portal.get_tool('portal_transforms')
        for folder in plans.getFolderContents():
            year = folder.id
            for plan in folder.getObject().getFolderContents():
                userid = plan.id
                if userid in ['natig', 'dolivero', 'aortiz', 'gruiz', 'pablo', 'rolando', 'maperez']:
                    # if userid not in ['rolando', ]:
                    continue
                planfolder = self.getplanfolder(userid)
                logger.info('Plan Folder {0}'.format(planfolder))
                obj = api.content.create(
                    type='plan',
                    title='Plan de trabajo {0}'.format(year),
                    container=planfolder,
                    id=year)
                text = plan.getObject().getText().decode('utf-8', 'ignore')
                try:
                    stream = transforms.convertTo('text/plain', plan.getObject().getText(), mimetype='text/html')
                except UnicodeDecodeError:
                    stream = transforms.convertTo('text/plain', text, mimetype='text/html')
                obj.text = stream.getData().strip().decode('utf-8', 'ignore')
                obj.reindexObject()
                notify(ObjectModifiedEvent(obj))
                api.content.transition(obj=obj, transition='submit_send')
                logger.info('{0}-{1}'.format(plan.id, folder.id))

    def getplanfolder(self, id):
        """ get plan folder. create one if necesary."""
        cvfolder = api.content.get(path='/fsd/{0}/cv'.format(id))
        if 'planes' not in cvfolder:
            obj = api.content.create(
                type='PlanFolder',
                title='Plane de Trabajo',
                container=cvfolder,
                id='planes')
            api.content.transition(obj=obj, transition='submit_noteditable')
        else:
            obj = cvfolder['planes']
        return obj


    @button.buttonAndHandler(u'create Plans for net year')
    def handle_new_plans(self, action):
        """Create plans for net year"""
        logger.info('creatiing plans ...')
        year = str(date.today().year + 1)
        reserchers = api.content.find(
            context=api.portal.get()['fsd'],
            depth=1,
            portal_type='FSDPerson',
            person_classification='investigadores',
            review_state='active',
        )
        for brain in reserchers:
            planfolder = self.getplanfolder(brain.id)

            if len(planfolder) > 1:
                logger.warning('Plan Folder {0} has many plans'.format(planfolder))

        for brain in reserchers:
            planfolder = self.getplanfolder(brain.id)

            if year in planfolder:
                continue
            logger.info('Plan Folder {0}'.format(planfolder))
            obj = api.content.create(
                type='plan',
                title='Plan de trabajo {0}'.format(year),
                container=planfolder,
                text=defaultPlanText(planfolder),
                id=year)
            obj.setCreators(brain.id)
            obj.reindexObject()
