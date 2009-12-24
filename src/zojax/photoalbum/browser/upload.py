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
import transaction

from zope import event
from zope.lifecycleevent import ObjectCreatedEvent

from zojax.wizard.step import WizardStep
from zojax.photoalbum.photo import Photo
from zojax.photoalbum.interfaces import _, IPhoto
from zojax.resourcepackage.library import include
from zojax.statusmessage.interfaces import IStatusMessage

from utils import unpack


class UploadForm(WizardStep):
    """ batch uplaods """

    title = _('Upload')

    def update(self):
        include('jquery-plugins')

        request = self.request

        if 'form.upload' in request:
            dataField = IPhoto['data']
            context = self.context

            files = []

            data = request.form.get('uploadFile', None)
            if data is not None:
                if type(data) is list:
                    files.extend(data)
                else:
                    files.append(data)

            updated = False
            for file in files:
                if not file:
                    continue

                for file in unpack(file):
                    name = file.filename

                    if name in context and \
                            not IPhoto.providedBy(context[name]):
                        photo = context[name]
                        field = dataField.bind(photo)
                        field.set(photo, file)
                        transaction.commit()
                        continue
                    elif name in context:
                        del context[name]

                    photo = Photo(name)
                    event.notify(ObjectCreatedEvent(photo))
                    context[name] = photo
                    field = dataField.bind(photo)
                    field.set(photo, file)
                    transaction.commit()
                    updated = True

            if updated:
                IStatusMessage(request).add(_(u'Files have been uploaded.'))
