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
from zope.security import checkPermission
from zope.security.proxy import removeSecurityProxy
from zope.traversing.browser import absoluteURL

from zojax.photoalbum.interfaces import _
from zojax.photoalbum.interfaces import IPhoto, IPhotoAlbum, IPhotosWorkspace
from zojax.content.actions.interfaces import \
    IAddContentCategory, IManageContentCategory
from zojax.content.actions.interfaces import IContextAction, IContentAction
from zojax.content.actions.contentactions import AddContent
from zojax.content.space.interfaces import IContentSpace
from zojax.personal.content.interfaces import IContentWorkspace

import interfaces


class AddPhotoAction(AddContent):
    interface.implements(interfaces.IAddPhotoAction, IAddContentCategory)
    component.adapts(IPhotosWorkspace, interface.Interface)

    weight = 100
    title = _(u'Upload a photo')

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def url(self):
        ws = IContentWorkspace(self.request.principal, None)
        return '%s/content.photo/create.html'%(absoluteURL(ws, self.request))

    def isAvailable(self):
        ws = IContentWorkspace(self.request.principal, None)
        if ws is None:
            return False

        context = self.context
        if not IPhotosWorkspace.providedBy(context.get('photos')):
            return False

        if checkPermission('zojax.AddPhoto', context) or \
                checkPermission('zojax.SubmitPhoto', context):
            return True

        return False
    
    
class UploadPhotosAction(AddContent):
    interface.implements(interfaces.IUploadPhotosAction, IAddContentCategory)
    component.adapts(IPhotoAlbum, interface.Interface)

    weight = 101
    title = _(u'Batch upload of photos')

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def url(self):
        return '%s/context.html/upload'%(absoluteURL(self.context, self.request))

    def isAvailable(self):
        context = self.context
        if checkPermission('zojax.AddPhoto', context) or \
                checkPermission('zojax.SubmitPhoto', context):
            return True

        return False


class BaseViewPhotoAlbumAction(object):
    component.adapts(IPhoto, interface.Interface)
    interface.implements(IContentAction, interfaces.IViewPhotoAlbumAction)

    weight = 300
    title = _(u'Back to album')
    description = u''

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def url(self):
        return '%s/'%absoluteURL(self.context.__parent__, self.request)

    def isAvailable(self):
        return True


class ViewPhotoAlbumAction(BaseViewPhotoAlbumAction):
    interface.implements(IManageContentCategory)


class ContextViewPhotoAlbumAction(BaseViewPhotoAlbumAction):
    interface.implements(IContextAction)

    weight = 0


class PhotoAlbumRSSFeedAction(object):
    component.adapts(IPhotoAlbum, interface.Interface)
    interface.implements(interfaces.IPhotoAlbumRSSFeedAction)

    weight = 99999
    title = _(u'RSS Feed')
    description = u''

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def url(self):
        return '%s/@@feeds/photos'%absoluteURL(self.context, self.request)

    def isAvailable(self):
        return True
