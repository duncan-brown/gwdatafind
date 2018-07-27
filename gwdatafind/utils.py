# -*- coding: utf-8 -*-
# Copyright (C) 2012-2015  Scott Koranda, 2015+ Duncan Macleod
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

"""Utilities for the GW datafind service
"""

import calendar
import os
import time
from operator import attrgetter

from OpenSSL import crypto

from lal import LIGOTimeGPS
from lal.utils import CacheEntry

DEFAULT_SERVER = os.getenv('LIGO_DATAFIND_SERVER')


def get_default_host():
    try:
        return os.environ['LIGO_DATAFIND_SERVER']
    except KeyError:
        raise ValueError("Failed to determine default gwdatafind host, please "
                         "pass manually or set the `LIGO_DATAFIND_SERVER` "
                         "environment variable")


def validate_proxy(path):
    """Validate the users X509 proxy certificate

    Tests that the proxy certificate is RFC 3820 compliant and that it
    is valid for at least the next 15 minutes.

    @returns: L{True} if the certificate validates
    @raises RuntimeError: if the certificate cannot be validated
    """
    # load the proxy from path
    with open(path, 'rt') as f:
        cert = crypto.load_certificate(crypto.FILETYPE_PEM, f.read())

    # try and read proxyCertInfo
    for i in range(cert.get_extension_count()):
        if cert.get_extension(i).get_short_name() == 'proxyCertInfo':
            break
    else:  # not rfc3820
        if cert.get_subject().CN.startswith('proxy'):
            raise RuntimeError('Could not find a valid proxy credential')

    # check time remaining
    expiry = cert.get_notAfter()
    if isinstance(expiry, bytes):
        expiry = expiry.decode('utf-8')
    expiryu = calendar.timegm(time.strptime(expiry, "%Y%m%d%H%M%SZ"))
    if expiryu < time.time():
        raise RuntimeError('Required proxy credential has expired')

    # return True to indicate validated proxy
    return True


def find_credential():
    """Locate the users X509 certificate and key files

    This method uses the C{X509_USER_CERT} and C{X509_USER_KEY} to locate
    valid proxy information. If those are not found, the standard location
    in /tmp/ is searched.

    @raises RuntimeError: if the proxy found via either method cannot
                          be validated
    @raises RuntimeError: if the cert and key files cannot be located
    """

    rfc_proxy_msg = ("Could not find a RFC 3820 compliant proxy credential."
                     "Please run 'grid-proxy-init -rfc' and try again.")

    # use X509_USER_PROXY from environment if set
    try:
        filePath = os.environ['X509_USER_PROXY']
    except KeyError:
        pass
    else:
        if validate_proxy(filePath):
            return filePath, filePath
        raise RuntimeError(rfc_proxy_msg)

    # use X509_USER_CERT and X509_USER_KEY if set
    try:
        return os.environ['X509_USER_CERT'], os.environ['X509_USER_KEY']
    except KeyError:
        pass

    # search for proxy file on disk
    uid = os.getuid()
    path = "/tmp/x509up_u%d" % uid
    if os.access(path, os.R_OK) and validate_proxy(path):
        return path, path

    raise RuntimeError(rfc_proxy_msg)


def as_cacheentry(url, coltype=LIGOTimeGPS):
    return CacheEntry.from_T050017(url, coltype=coltype)


def to_wcache(cache):
    """Convert a LAL-format `~glue.lal.Cache` into an omega format cache
    """
    wcache = []
    duration = 0
    for entry in sorted(
            cache, key=attrgetter('observatory', 'description', 'segment')):
        dir_ = os.path.dirname(entry.path)
        # if this file has the same attributes, goes into the same directory,
        # has the same duration, and overlaps with or is contiguous with
        # the last file, just add its segment to the last one:
        if duration and (
                entry.observatory == wentry.observatory and
                entry.description == wentry.description and
                dir_ == wentry.path and
                abs(entry.segment) == duration and
                (entry.segment.connects(wentry.segment) or
                 entry.segment.intersects(wentry.segment))
        ):
            wentry.segment |= entry.segment
        # otherwise create a new entry in the omega wcache
        else:
            wentry = CacheEntry(entry.observatory, entry.description,
                                entry.segment, dir_)
            wcache.append(wentry)
            duration = abs(entry.segment)
    return wcache
