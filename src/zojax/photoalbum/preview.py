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
import logging, sys
from zope import interface, event
from zope.lifecycleevent import ObjectCreatedEvent
from zope.app.container.btree import BTreeContainer

from zojax.filefield.data import File
from zojax.converter.api import convert
from zojax.converter.interfaces import ConverterException

from interfaces import IPreviewFolder


class PreviewFolder(BTreeContainer):
    interface.implements(IPreviewFolder)

    __name__ = u'preview'

    def clear(self):
        for name in self.keys():
            del self[name]

    def generatePreview(self, width, height, quality=88):
        name = '%sx%s'%(width, height)
        if name in self:
            return self[name]

        photoFile = self.__parent__.data
        if photoFile is None:
            return

        try:
            data = convert(photoFile.data, 'image/jpeg',
                           sourceMimetype=photoFile.mimeType,
                           width=width, height=height, quality=quality)
        except ConverterException, err:
            log = logging.getLogger('zojax.photoalbum')
            log.log(logging.WARNING, str(err))
            return

        preview = File()
        preview.data = data
        preview.filename = name
        preview.mimeType = 'image/jpeg'
        event.notify(ObjectCreatedEvent(preview))

        self[name] = preview
        return self[name]
