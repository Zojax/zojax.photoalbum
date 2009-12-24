##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
import os.path
import unittest, doctest
from zope import interface
from zope.app.testing import setup
from zope.app.rotterdam import Rotterdam
from zope.app.intid import IntIds
from zope.app.intid.interfaces import IIntIds
from zope.app.testing.functional import getRootFolder
from zojax.layoutform.interfaces import ILayoutFormLayer
from zojax.filefield.testing import ZCMLLayer, FunctionalDocFileSuite
from zojax.catalog.catalog import Catalog, ICatalog
from zojax.personal.space.manager import PersonalSpaceManager, IPersonalSpaceManager


class IDefaultSkin(ILayoutFormLayer, Rotterdam):
    """ skin """


def setUp(test):
    root = getRootFolder()
    root['intids'] = IntIds()
    root['intids'].register(root)
    root.getSiteManager().registerUtility(root['intids'], IIntIds)

    catalog = Catalog()
    root['catalog'] = catalog
    root.getSiteManager().registerUtility(root['catalog'], ICatalog)

    manager = PersonalSpaceManager()
    root['people'] = manager
    root.getSiteManager().registerUtility(root['people'], IPersonalSpaceManager)


photoalbumLayer = ZCMLLayer(
    os.path.join(os.path.split(__file__)[0], 'ftesting.zcml'),
    __name__, 'photoalbumLayer', allow_teardown=True)


def test_suite():
    return unittest.TestSuite((
            FunctionalDocFileSuite(
                "testbrowser.txt",
                optionflags=doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE,
                layer = photoalbumLayer, setUp=setUp),))
