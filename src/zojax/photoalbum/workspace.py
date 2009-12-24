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
from zope import interface, component, event
from zope.lifecycleevent import ObjectCreatedEvent
from zope.lifecycleevent import ObjectModifiedEvent
from zope.security.proxy import removeSecurityProxy
from zojax.content.space.interfaces import IContentSpace
from zojax.content.space.workspace import WorkspaceFactory

from album import PhotoAlbum
from interfaces import IPhotosWorkspace, IPhotosWorkspaceFactory


class PhotosWorkspace(PhotoAlbum):
    interface.implements(IPhotosWorkspace)

    @property
    def space(self):
        return self.__parent__


class PhotosWorkspaceFactory(WorkspaceFactory):
    component.adapts(IContentSpace)
    interface.implements(IPhotosWorkspaceFactory)

    name = 'photos'
    title = u'Photos'
    description = u'Space photo albums workspace.'
    weight = 901
    factory = PhotosWorkspace
