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
from zojax.content.actions.interfaces import IAddContentAction
from zojax.content.actions.interfaces import IContextAction, IContentAction


class IPhotoView(interface.Interface):
    """ """


class IPhotoBatch(interface.Interface):
    """ photo """


class IAddPhotoAction(IAddContentAction):
    """ add photo action """
    
    
class IUploadPhotosAction(IAddContentAction):
    """ upload photos action """


class IViewPhotoAlbumAction(interface.Interface):
    """ """


class IPhotoAlbumRSSFeedAction(IContextAction):
    """ """
