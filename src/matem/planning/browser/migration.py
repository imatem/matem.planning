# -*- coding: utf-8 -*-

from plone import api
from z3c.form import button
from z3c.form import form
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

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
                # if userid not in ['natig', 'dolivero', 'aortiz', 'gruiz', 'pablo', 'rolando',]:
                if userid not in ['rolando', ] or year == '2012':
                    continue
                planfolder = self.getplanfolder(userid)
                logger.info('Plan Folder {0}'.format(planfolder))
                obj = api.content.create(
                    type='plan',
                    title='Plan de trabajo {0}'.format(year),
                    container=planfolder,
                    id=year)
                text = plan.getObject().getText().decode('utf-8')
                stream = transforms.convertTo('text/plain', text, mimetype='text/html')
                obj.text = stream.getData().strip()
                obj.reindexObject()
                notify(ObjectModifiedEvent(obj))
                logger.info('{0}-{1}'.format(plan.id, folder.id))

    def getplanfolder(self, id):
        """ get plan folder. create one if necesary."""
        cvfolder = api.content.get(path='/fsd/{0}/cv'.format(id))
        if 'planes' not in cvfolder:
            obj = api.content.create(
                type='PlanFolder',
                title='Planes de Trabajo',
                container=cvfolder,
                id='planes')
        else:
            obj = cvfolder['planes']
        return obj
