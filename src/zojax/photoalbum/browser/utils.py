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
import os.path, zipfile, tarfile
from cStringIO import StringIO
from zojax.filefield.data import FileData


def unpack(file):
    filename = os.path.split(file.filename)[1]

    file_data = []
    extracted = 0

    pre, ext = os.path.splitext(filename)
    file.seek(0)

    if ext in ('.tar', '.gz', '.tgz', '.bz2', '.tbz2'):
        if ext == '.tar':
            tar = tarfile.open(filename, mode='r|', fileobj=file)
        elif ext in ('.gz', '.tgz'):
            tar = tarfile.open(filename, mode='r|gz', fileobj=file)
        elif ext in ('.bz2', '.tbz2'):
            tar = tarfile.open(filename, mode='r|bz2', fileobj=file)

        for ti in tar:
            if ti.isreg():
                file_data.append(
                    (ti.name, StringIO(tar.extractfile(ti).read())))

    elif ext == '.zip':
        zip = zipfile.ZipFile(file, "r")
        for name in zip.namelist():
            file_data.append((name, zip.read(name)))
    else:
        file_data.append((filename, file))

    for name, data in file_data:
        fn = os.path.split(name)[1]

        if fn:
            file = FileData(data, fn)
            if file.mimeType in ('image/jpeg','image/gif','image/png'):
                yield file
