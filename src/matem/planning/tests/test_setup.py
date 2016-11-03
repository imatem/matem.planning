# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from matem.planning.testing import MATEM_PLANNING_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that matem.planning is properly installed."""

    layer = MATEM_PLANNING_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if matem.planning is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'matem.planning'))

    def test_browserlayer(self):
        """Test that IMatemPlanningLayer is registered."""
        from matem.planning.interfaces import (
            IMatemPlanningLayer)
        from plone.browserlayer import utils
        self.assertIn(IMatemPlanningLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = MATEM_PLANNING_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['matem.planning'])

    def test_product_uninstalled(self):
        """Test if matem.planning is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'matem.planning'))

    def test_browserlayer_removed(self):
        """Test that IMatemPlanningLayer is removed."""
        from matem.planning.interfaces import \
            IMatemPlanningLayer
        from plone.browserlayer import utils
        self.assertNotIn(IMatemPlanningLayer, utils.registered_layers())
