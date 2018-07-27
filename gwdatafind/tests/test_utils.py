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

"""Tests for :mod:`gwdatafind.utils`
"""

import os

from OpenSSL import crypto

import pytest

try:
    from unittest import mock
except ImportError:  # python < 3
    import mock

from .. import utils


@mock.patch.dict('os.environ')
def test_get_default_host():
    os.environ.pop('LIGO_DATAFIND_SERVER', None)
    with pytest.raises(ValueError):
        utils.get_default_host()
    os.environ['LIGO_DATAFIND_SERVER'] = 'test'
    assert utils.get_default_host() == 'test'


@mock.patch('gwdatafind.utils.crypto.load_certificate')
def test_validate_proxy(loader, tmpname):
    # mocks
    cert = mock.MagicMock()
    subject = mock.MagicMock()
    ext = mock.MagicMock()
    loader.return_value = cert
    cert.get_subject.return_value = subject
    cert.get_extension.return_value = ext

    # check we get to the end
    ext.get_short_name.return_value = 'proxyCertInfo'
    subject.CN = ''
    cert.get_notAfter.return_value = '22000101000000Z'
    assert utils.validate_proxy(tmpname)
    assert loader.called_once_with(crypto.FILETYPE_PEM, 'test\n')

    # check non-RFC3820 non-proxy still returns
    ext.get_short_name.return_value = 'test'
    assert utils.validate_proxy(tmpname)

    # check expired ticket
    cert.get_notAfter.return_value = '20000101000000Z'
    with pytest.raises(RuntimeError) as exc:
        utils.validate_proxy(tmpname)
    assert str(exc.value) == 'Required proxy credential has expired'

    # assert non-RFC3820 non-proxy raises correct error
    subject.CN = 'proxy'
    with pytest.raises(RuntimeError) as exc:
        utils.validate_proxy(tmpname)
    assert str(exc.value) == 'Could not find a valid proxy credential'


@mock.patch.dict('os.environ')
@mock.patch('gwdatafind.utils.validate_proxy')
@mock.patch('os.access')
def test_find_credential(access, validate, tmpname):
    # clear the deck
    for suffix in ('PROXY', 'CERT', 'KEY'):
        os.environ.pop('X509_USER_{0}'.format(suffix), None)

    access.return_value = True

    # check fixed path for proxy
    validate.return_value = False
    with pytest.raises(RuntimeError) as exc:
        utils.find_credential()
    assert str(exc.value).startswith('Could not find a RFC 3820')

    validate.return_value = True
    assert utils.find_credential() == (
        '/tmp/x509up_u{0}'.format(os.getuid()),) * 2

    # use CERT and KEY
    os.environ.update({
        'X509_USER_CERT': 'test_cert',
        'X509_USER_KEY': 'test_key',
    })
    assert utils.find_credential() == ('test_cert', 'test_key')

    # use X509_USER_PROXY
    os.environ['X509_USER_PROXY'] = tmpname
    validate.return_value = True
    assert utils.find_credential() == (tmpname, tmpname)
    validate.return_value = False
    with pytest.raises(RuntimeError):
        utils.find_credential()
