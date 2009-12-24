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
from BTrees.Length import Length
from BTrees.OOBTree import OOTreeSet

from zope import interface, component
from zope.schema.fieldproperty import FieldProperty
from zope.security.proxy import removeSecurityProxy
from zope.app.container.interfaces import IObjectAddedEvent
from zope.app.container.interfaces import IObjectRemovedEvent

from zojax.content.type.container import ContentContainer

from interfaces import IPhoto, IPhotoAlbum


class PhotoAlbum(ContentContainer):
    interface.implements(IPhotoAlbum)

    pageCount = FieldProperty(IPhotoAlbum['pageCount'])

    def __init__(self, **kw):
        super(PhotoAlbum, self).__init__(**kw)

        self.albums = OOTreeSet()
        self.photos = OOTreeSet()
        self.__dict__['totalPhotos'] = Length(0)

    def __setitem__(self, name, item):
        super(PhotoAlbum, self).__setitem__(name, item)

        if IPhoto.providedBy(item):
            self.photos.insert(name)
        elif IPhotoAlbum.providedBy(item):
            self.albums.insert(name)

    def __delitem__(self, name):
        if name in self.photos:
            self.photos.remove(name)
        elif name in self.albums:
            self.albums.remove(name)

        super(PhotoAlbum, self).__delitem__(name)

    @property
    def total(self):
        return len(self.photos)

    @property
    def totalAlbums(self):
        return len(self.albums)

    @property
    def totalPhotos(self):
        return self.__dict__['totalPhotos']()

    def listPhotos(self):
        photos = self.photos

        for name in self:
            if name in photos:
                yield name

    def listPhotoAlbums(self):
        albums = self.albums

        for name in self:
            if name in albums:
                yield name


@component.adapter(IPhoto, IObjectAddedEvent)
def photoAdded(photo, event):
    parent = photo.__parent__
    while parent is not None:
        if IPhotoAlbum.providedBy(parent):
            removeSecurityProxy(parent).__dict__['totalPhotos'].change(+1)
        else:
            break
        parent = getattr(parent, '__parent__', None)


@component.adapter(IPhoto, IObjectRemovedEvent)
def photoRemoved(photo, event):
    parent = event.oldParent
    while parent is not None:
        if IPhotoAlbum.providedBy(parent):
            removeSecurityProxy(parent).__dict__['totalPhotos'].change(-1)
        else:
            break
        parent = getattr(parent, '__parent__', None)
