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
from zope import interface, component
from zope.size import byteDisplay
from zope.size.interfaces import ISized
from zope.proxy import removeAllProxies
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zojax.content.type.item import PersistentItem
from zojax.filefield.field import FileFieldProperty

from preview import PreviewFolder
from interfaces import IPhoto


class Photo(PersistentItem):
    interface.implements(IPhoto)

    data = FileFieldProperty(IPhoto['data'])

    def __init__(self, *args, **kw):
        super(Photo, self).__init__(*args, **kw)

        self.preview = PreviewFolder()
        self.preview.__parent__ = self


@component.adapter(IPhoto, IObjectModifiedEvent)
def photoModifiedHandler(photo, event):
    removeAllProxies(photo).preview.clear()


class Sized(object):
    component.adapts(IPhoto)
    interface.implements(ISized)

    def __init__(self, context):
        self.context = context

    def sizeForSorting(self):
        return "byte", self.context.data.size

    def sizeForDisplay(self):
        return byteDisplay(self.context.data.size)
