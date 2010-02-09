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
from zope import interface
from zope.component import getUtility
from zope.traversing.browser import absoluteURL

from zojax.batching.batch import Batch
from zojax.resourcepackage.library import include
from zojax.resourcepackage.library import includeInplaceSource
from zojax.photoalbum.interfaces import _, sizes, IPhoto
from zojax.photoalbum.interfaces import IPhotoAlbum, IPhotoAlbumProduct

from interfaces import IPhotoView


class PhotoAlbumView(object):
    interface.implements(IPhotoView)

    def update(self):
        include('zojax.photoalbum')

        product = getUtility(IPhotoAlbumProduct)

        self.lightbox = product.lightbox
        if self.lightbox:
            try:
                self.context.listPhotos().next()
                includeInplaceSource(lightboxinit, required=('jquery-lightbox',))
            except:
                pass

        title, self.width, self.height = sizes['thumbnail']
        self.url = absoluteURL(self.context, self.request)

    def listPhotos(self):
        context = self.context
        request = self.request

        seq = list(context.listPhotoAlbums()) + list(context.listPhotos())

        return Batch(seq, size=self.context.pageCount, request=request)

    def photoInfo(self, photoId):
        photo = self.context[photoId]

        if IPhotoAlbum.providedBy(photo):
            return {'name': photoId,
                    'title': photo.title or photoId,
                    'tag': '',
                    'album': photo}
        else:
            preview = photo.preview.generatePreview(480, 480)
            photo.preview.generatePreview(self.width, self.height)

            title = photo.title or photoId

            url = '%s/%s'%(self.url, photoId)

            if self.lightbox:
                lightbox = '%s<br /><a href="%s/fullscreen.html" title="%s">%s</a> <a href="%s/" title="%s">%s</a>'%(
                    title, url, _('Fullscreen view'), _('Fullscreen'),
                    url, _('Standard view'), _(u'View'))
                photoUrl = '%s/preview/480x480/'%url
            else:
                lightbox = ''
                photoUrl = url

            return {'name': photoId,
                    'title': title,
                    'tag': '<img src="%s/preview/%sx%s/" title="%s" />'%(
                        url, self.width, self.height, photo.title),
                    'album': None,
                    'url': photoUrl,
                    'lightbox': lightbox,
                    'preview': preview}

    def randomPhoto(self, album):
        photo = album[album.listPhotos().next()]
        photo.preview.generatePreview(self.width, self.height)

        url = absoluteURL(album, self.request)
        return '<img src="%s/%s/preview/%sx%s/" title="%s"/>'%(
            url, photo.__name__, self.width, self.height, album.description)


lightboxinit = """
<script type="text/javascript">
</script>
"""
