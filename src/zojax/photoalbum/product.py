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
from pytz import utc
from datetime import datetime

from zope import interface
from zojax.product.utils import registerUtility, unregisterUtility

from interfaces import IPhotoAlbumProduct


class PhotoalbumProduct(object):
    interface.implements(IPhotoAlbumProduct)

    def update(self):
        super(ContentTypesProduct, self).update()

        registerUtility('contenttypes.event.isEvent',
                        indexIsEvent, ((ICatalogIndex, 'eventIsEvent'),),
                        'indexes')
        registerUtility('contenttypes.event.startDate',
                        indexStartDate, ((ICatalogIndex, 'eventStartDate'),),
                        'indexes')
        registerUtility('contenttypes.event.endDate',
                        indexEndDate, ((ICatalogIndex, 'eventEndDate'),),
                        'indexes')

    def uninstall(self):
        unregisterUtility('contenttypes.event.isEvent',
                          ((ICatalogIndex, 'eventIsEvent'),),
                        'indexes')
        unregisterUtility('contenttypes.event.startDate',
                          ((ICatalogIndex, 'eventStartDate'),),
                        'indexes')
        unregisterUtility('contenttypes.event.endDate',
                          ((ICatalogIndex, 'eventEndDate'),),
                        'indexes')
        super(ContentTypesProduct, self).uninstall()
