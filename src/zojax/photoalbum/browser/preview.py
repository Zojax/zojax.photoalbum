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
from zope.app.pagetemplate import ViewPageTemplateFile
from zojax.wizard.step import WizardStepForm
from zojax.layoutform import button, Fields
from zojax.statusmessage.interfaces import IStatusMessage

from zojax.photoalbum.interfaces import _


class IPreviewForm(interface.Interface):

    width = schema.Int(
        title = _(u'Width'),
        min = 0,
        required = True)

    height = schema.Int(
        title = _(u'Height'),
        min = 0,
        required = True)


class Previews(WizardStepForm):

    buttons = WizardStepForm.buttons.copy()
    handlers = WizardStepForm.handlers.copy()

    fields = Fields(IPreviewForm)
    label = _('Generate preview')
    ignoreContext = True

    def isComplete(self):
        return True

    @button.buttonAndHandler(_(u'Generate'), name='generate')
    def handlePreview(self, action):
        pass

    def update(self):
        super(Previews, self).update()

        if 'form.delete' in self.request:
            removed = False
            preview = self.context.preview
            names = self.request.get('preview', ())
            for name in names:
                if name in preview:
                    del preview[name]
                    removed = True

            if removed:
                IStatusMessage(self.request).add(_('Previews have been removed.'))

        if 'preview.buttons.generate' in self.request:
            data, errors = self.extractData()

            if errors:
                IStatusMessage(self.request).add(self.formErrorsMessage, 'error')
            else:
                context = self.context
                context.preview.generatePreview(data['width'], data['height'])
                IStatusMessage(self.request).add(_('Preview has been generated.'))
