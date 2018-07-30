.. sectionauthor:: Duncan Macleod <duncan.macleod@ligo.org>
.. currentmodule:: gwdatafind

###################################
Migrating from :mod:`glue.datafind`
###################################

This document provides some basic instructions on how to update code written
to use :mod:`glue.datafind` to using :mod:`gwdatafind`.

===============
Renamed objects
===============

The table below summarise all renamings between :mod:`glue.datafind` and
:mod:`gwdatafind`.

==========================================  ======================================
:mod:`glue.datafind` name                   :mod:`gwdatafind` name
==========================================  ======================================
`GWDataFindHTTPConnection`                  `HTTPConnection`
`GWDataFindHTTPSConnection`                 `HTTPSConnection`
`GWDataFindHTTPConnection.find_frame`       `HTTPConnection.find_url`
`GWDataFindHTTPConnection.find_frame_urls`  `HTTPConnection.find_urls`
==========================================  ======================================

=================
Query output type
=================

:mod:`glue.datafind` returns list of URLs as a :class:`glue.lal.Cache` of
:class:`lal.CacheEntry` objects.
:mod:`gwdatafind` returns simple `lists <list>` of `str`.
You can translate the new form back to the old easily::

    from glue.lal import Cache
    cache = Cache.from_urls(urls)

=====================
Creating a connection
=====================

:mod:`glue.datafind` provided no convenience methods for opening a new
connection, so you probably wrote your own function that stripped the port
number from the server name, and handled HTTP/HTTPS manually.
With `gwdatafind`, you can just use the :meth:`gwdatafind.connect` method to
handle that::

    >>> from gwdatafind import connect
    >>> connection = connect()

or if you know the server URL::

    >>> connection = connect('datafind.server.url:443')

=======================
Simplified single calls
=======================

If you are only interested in a single query to a single server (the typical
use case), you can utilise one of the new top-level functions.
So, instead of::

    >>> from glue.datafind import GWDataFindHTTPConnection
    >>> connection = GWDataFindHTTPConnection()
    >>> cache = connection.find_frame_urls(...)

you can just use::

    >>> from gwdatafind import find_urls
    >>> urls = find_urls(...)

The arguments and syntax for :func:`~gwdatafind.find_urls` is the same as that of the
old :meth:`glue.datafind.GWDataFindHTTPConnection.find_frame_urls` method.

Similar top-level functions exist for
:func:`~gwdatafind.ping`,
:func:`~gwdatafind.find_observatories`,
:func:`~gwdatafind.find_types`,
:func:`~gwdatafind.find_times`,
:func:`~gwdatafind.find_url`,
:func:`~gwdatafind.find_latest`, and
:func:`~gwdatafind.find_urls`

==================
Command-line usage
==================

The `lscsoft-glue <https://pypi.org/project/lscsoft-glue/>`__ package provides the
``gw_data_find`` script, used to perform queries from the command-line.
`gwdatafind` provides an identical interface via Python module execution (`python -m`).

To migrate, replace ``gw_data_find`` with ``python -m gwdatafind``.
