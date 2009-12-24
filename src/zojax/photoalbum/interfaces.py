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
from zope import interface, schema
from zope.i18nmessageid import MessageFactory

from zojax.filefield.field import FileField
from zojax.content.type.interfaces import IItem
from zojax.content.feeds.interfaces import IRSS2Feed
from zojax.content.space.interfaces import IWorkspace, IWorkspaceFactory

_ = MessageFactory('zojax.photoalbum')

sizes = {'thumbnail': (_('Thumbnail'), 128, 128),
         'small': (_('Small'), 320, 320),
         'medium': (_('Medium'), 480, 480),
         'large': (_('Large'), 768, 768)}


class IPhoto(interface.Interface):
    """ photo """

    title = schema.TextLine(
        title = _(u'Title'),
        default = u'',
        missing_value = u'',
        required = False)

    description = schema.Text(
        title = _(u'Description'),
        default = u'',
        missing_value = u'',
        required = False)

    data = FileField(
        title = _(u'Photo'),
        mimeTypes = ('image/jpeg','image/gif','image/png'),
        required = False)

    preview = interface.Attribute('Previews')


class IPhotoType(interface.Interface):
    """ photo content type """


class ISimplePhotoType(interface.Interface):
    """ photo content type """


class IPhotoAlbum(IItem):
    """ photo album """

    pageCount = schema.Int(
        title = _(u'Page count'),
        description = _(u'Number of photos on page.'),
        default = 10,
        required = False)

    total = interface.Attribute('Total photos in album')
    totalAlbums = interface.Attribute('Total sub albums')
    totalPhotos = interface.Attribute('Total photos in all sub albums')

    def listPhotos():
        """ list contained photos """

    def listPhotoAlbums():
        """ list contained photo albums """


class IPhotoAlbumType(interface.Interface):
    """ photo album content type """


class IPreviewFolder(interface.Interface):
    """ folder for photo previews """

    def clear():
        """ clear previews """

    def generatePreview(width, height):
        """ generate preview """


class IPhotoAlbumProduct(interface.Interface):
    """ photoalbum product """

    lightbox = schema.Bool(
        title = _(u'Lightbox'),
        description = _(u'Use Lightbox javascript for quick photo album browsing.'),
        default = True,
        required = False)


class IPhotosWorkspace(IPhotoAlbum, IWorkspace):
    """ photos workspace """


class IPhotosWorkspaceFactory(IWorkspaceFactory):
    """ photos workspace factory """


class IPhotosRSSFeed(IRSS2Feed):
    """ photos rss feed """
