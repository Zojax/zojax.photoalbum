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
from zope.component import getMultiAdapter
from zope.app.pagetemplate import ViewPageTemplateFile
from z3c.batching.batch import Batch

from interfaces import IPhotoBatch


class PhotoBatch(Batch):
    interface.implements(IPhotoBatch)

    def __init__(self, sequence, start=0, size=1, batches=None):
        super(PhotoBatch, self).__init__(sequence, start, size, batches)


class PhotoBatchView(object):

    template = ViewPageTemplateFile('batch.pt')

    def render(self):
        context = self.context

        if not bool(context.previous or context.next):
            return u''

        self.batch_url = self.request.URL[-2]

        return super(PhotoBatchView, self).render()


class PhotoBatchFullView(PhotoBatchView):

    template = ViewPageTemplateFile('batchfull.pt')
