# -*- coding: utf-8 -*-
# Copyright (C) 2018  Duncan Macleod
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

"""Test utilities
"""

import pytest

from six.moves import http_client

try:
    from unittest import mock
except ImportError:  # python2.x
    import mock

HTTP_CLIENT = http_client.__name__
HTTP_CONNECTION = '{0}.HTTPConnection'.format(HTTP_CLIENT)


@pytest.fixture
def response():
    """Patch an HTTPConnection to do nothing in particular

    Yields the patch for `http.client.HTTPConnection.getresponse`
    """
    with mock.patch('{0}.request'.format(HTTP_CONNECTION)), \
         mock.patch('{0}.getresponse'.format(HTTP_CONNECTION)) as resp:
        yield resp
