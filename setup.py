#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) Duncan Macleod (2017)
#
# This file is part of GWDataFind
#
# GWDataFind is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# GWDataFind is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GWDataFind.  If not, see <http://www.gnu.org/licenses/>.

"""The client library for the LIGO Data Replicator (LDR) service.
"""

import os.path
import re
import sys

from setuptools import (setup, find_packages)

cmdclass = dict()


def find_version(path):
    """Parse the __version__ metadata in the given file.
    """
    with open(path, 'r') as fp:
        version_file = fp.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

# -- dependencies -------------------------------

setup_requires = []
if {'test'}.intersection(sys.argv):
    setup_requires.append('pytest_runner')
if {'build_sphinx'}.intersection(sys.argv):
    setup_requires.extend((
        'sphinx',
        'sphinx_rtd_theme',
        'sphinx_tabs',
        'numpydoc',
        'sphinx_automodapi',
    ))
    from sphinx.setup_command import BuildDoc
    cmdclass['build_sphinx'] = BuildDoc

install_requires = [
    'six',
    'ligo-segments',
    'pyOpenSSL',
]
tests_require = [
    'pytest >= 2.8.0',
]
if sys.version < '3.0':
    tests_require.append('mock')

# get long description from README
with open('README.md', 'rb') as f:
    longdesc = f.read().decode().strip()

# run setup
setup(
    name='gwdatafind',
    version=find_version(os.path.join('gwdatafind', '__init__.py')),
    packages=find_packages(),
    description=__doc__.rstrip(),
    long_description=longdesc,
    long_description_content_type='text/markdown',
    author='Duncan Macleod',
    author_email='duncan.macleod@ligo.org',
    url='https://gwdatafind.readthedocs.io/',
    license='GPLv3',
    cmdclass=cmdclass,
    setup_requires=setup_requires,
    install_requires=install_requires,
    tests_require=tests_require,
    #entry_points={'console_scripts': [             X Can't include this block
    #    'gw_data_find=gwdatafind.__main__:main',   X until gw_data_find isn't
    #]},                                            X also provided by glue
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Scientific/Engineering :: Physics',
    ],
)
