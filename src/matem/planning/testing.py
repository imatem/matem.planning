# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import matem.planning


class MatemPlanningLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=matem.planning)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'matem.planning:default')


MATEM_PLANNING_FIXTURE = MatemPlanningLayer()


MATEM_PLANNING_INTEGRATION_TESTING = IntegrationTesting(
    bases=(MATEM_PLANNING_FIXTURE,),
    name='MatemPlanningLayer:IntegrationTesting'
)


MATEM_PLANNING_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(MATEM_PLANNING_FIXTURE,),
    name='MatemPlanningLayer:FunctionalTesting'
)


MATEM_PLANNING_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        MATEM_PLANNING_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='MatemPlanningLayer:AcceptanceTesting'
)
