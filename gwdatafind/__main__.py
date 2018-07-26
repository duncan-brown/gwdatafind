# -*- coding: utf-8 -*-
# Copyright Duncan Macleod 2017
#
# This file is part of GWDataFind.
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

"""Query the DataFind service for information.
"""

from __future__ import print_function

import argparse
import re
import sys
from operator import attrgetter

from ligo import segments

from . import (__version__, ui)
from .utils import (get_default_host, to_wcache)

__author__ = 'Duncan Macleod <duncan.macleod@ligo.org>'
__credits__ = 'Scott Koranda, The LIGO Scientific Collaboration'


def command_line():
    """Build an `~argparse.ArgumentParser` for the `gwdatafind` CLI
    """
    try:
        defhost = get_default_host()
    except ValueError:
        defhost = None

    parser = argparse.ArgumentParser(description=__doc__)

    try:  # try and use leading upper case, but don't fail if API changes
        parser._optionals.title = "Optional arguments"
    except AttributeError:
        pass

    parser.add_argument('-V', '--version', action='version',
                        version=__version__,
                        help='show version number and exit')

    qargs = parser.add_argument_group(
        "Query types", "Select one of the following, if none are selected a "
                       "query for frame URLS will be performed"
    )
    qtype = qargs.add_mutually_exclusive_group(required=False)
    parser._mutually_exclusive_groups.append(qtype)  # bug in argparse
    qtype.add_argument('-p', '--ping', action='store_true', default=False,
                       help='ping the DataFind server')
    qtype.add_argument('-w', '--show-observatories', action='store_true',
                       default=False, help='list available observatories')
    qtype.add_argument('-y', '--show-types', action='store_true',
                       default=False, help='list available file types')
    qtype.add_argument('-a', '--show-times', action='store_true',
                       default=False, help='list available segments')
    qtype.add_argument('-f', '--filename', action='store', metavar='FILE',
                       help='resolve URL(s) for a particular file name')
    qtype.add_argument('-T', '--latest', action='store_true', default=False,
                       help='resolve URL(s) for the most recent file of the '
                            'specified type')

    dargs = parser.add_argument_group(
        "Data options", "Parameters for your query. Which options are "
                        "required depends on the query type"
    )
    dargs.add_argument('-o', '--observatory', metavar='OBS',
                       help='observatory(ies) that generated frame file; use '
                            '--show-observatories to see what is available.')
    dargs.add_argument('-t', '--type', help='type of frame file, use --show-'
                                            'types to see what is available.')
    dargs.add_argument('-s', '--gps-start-time', type=int, dest='gpsstart',
                       metavar='GPS', help='start of GPS time search')
    dargs.add_argument('-e', '--gps-end-time', type=int, dest='gpsend',
                       metavar='GPS', help='end of GPS time search')

    sargs = parser.add_argument_group(
        'Connection options', 'Authentication and connection options.')
    sargs.add_argument('-r', '--server', action='store', type=str,
                       metavar='HOST:PORT', default=defhost,
                       required=defhost is None,
                       help='hostname and optional port of server to query '
                            '(default: %(default)s)')
    sargs.add_argument('-P', '--no-proxy', action='store_true',
                       help='attempt to authenticate without a grid proxy '
                            '(default: %(default)s)')

    oargs = parser.add_argument_group(
        'Output options', 'Parameters for parsing and writing output.')
    oform = oargs.add_mutually_exclusive_group()
    parser._mutually_exclusive_groups.append(oform)  # bug in argparse
    oform.add_argument('-l', '--lal-cache', action='store_true',
                       help='format output for use as a LAL cache file')
    oform.add_argument('-W', '--frame-cache', action='store_true',
                       help='format output for use as a frame cache file')
    oform.add_argument('-n', '--names-only', action='store_true',
                       help='display only the basename of each file')
    oargs.add_argument('-m', '--match', help='return only results that match '
                                             'a regular expression')
    oargs.add_argument('-u', '--url-type', default='file',
                       help='return only URLs with a particular scheme or '
                            'head such as \'file\' or \'gsiftp\'')
    oargs.add_argument('-g', '--gaps', action='store_true',
                       help='check the returned list of URLs or paths to see '
                            'if the files cover the requested interval; a '
                            'return value of zero (0) indicates the interval '
                            'is covered, a value of one (1) indicates at '
                            'least one gap exists and the interval is not , '
                            'covered and a value of (2) indicates that the '
                            'entire interval is not covered; missing gaps are '
                            'printed to stderr (default: %(default)s)')
    oargs.add_argument('-O', '--output-file', metavar='PATH',
                       help='path to output file, defaults to stdout')

    return parser


def check_options(parser, args):
    """Sanity check parsed command line options

    If any problems are found `argparse.ArgumentParser.error` is called,
    which in turn calls :func:`sys.exit`.

    Parameters
    ----------
    parser : `argparse.ArgumentParser`
        the parser used to read the arguments

    args : `argparse.Namespace`
        the output of the command-line parsing
    """
    if args.show_times and (not args.observatory or not args.type):
        parser.error("--observatory and --type must be given when using "
                     "--show-times.")
    if args.show_urls and not all((args.observatory, args.type,
                                   args.gpsstart, args.gpsend)):
        parser.error("--observatory, --type, --gps-start-time, and "
                     "--gps-end-time time all must be given when querying for "
                     "file URLs")
    if args.gaps and not args.show_urls:
        parser.error('-g/--gaps only allowed when querying for file URLs')


def ping(args, out):
    """Worker for the --ping option.

    Parameters
    ----------
    args : `argparse.Namespace`
        the parsed command-line options.

    out : `file`
        the open file object to write to.

    Returns
    -------
    exitcode : `int` or `None`
        the return value of the action or `None` to indicate success.
    """
    ui.ping(host=args.server)
    print("LDRDataFindServer at {0.server} is alive".format(args), file=out)


def show_observatories(args, out):
    """Worker for the --show-observatories option

    Parameters
    ----------
    args : `argparse.Namespace`
        the parsed command-line options.

    out : `file`
        the open file object to write to.

    Returns
    -------
    exitcode : `int` or `None`
        the return value of the action or `None` to indicate success.
    """
    sitelist = ui.find_observatories(host=args.server, match=args.match)
    print("\n".join(sitelist), file=out)


def show_types(args, out):
    """Worker for the --show-types option

    Parameters
    ----------
    args : `argparse.Namespace`
        the parsed command-line options.

    out : `file`
        the open file object to write to.

    Returns
    -------
    exitcode : `int` or `None`
        the return value of the action or `None` to indicate success.
    """
    typelist = ui.find_types(site=args.observatory, match=args.match,
                             host=args.server)
    print("\n".join(typelist), file=out)


def show_times(args, out):
    """Worker for the --show-times option

    Parameters
    ----------
    args : `argparse.Namespace`
        the parsed command-line options.

    out : `file`
        the open file object to write to.

    Returns
    -------
    exitcode : `int` or `None`
        the return value of the action or `None` to indicate success.
    """
    seglist = ui.find_times(site=args.observatory, frametype=args.type,
                            gpsstart=args.gpsstart, gpsend=args.gpsend,
                            host=args.server)
    print('# seg\tstart     \tstop      \tduration', file=out)
    for i, seg in enumerate(seglist):
        print(
            '{n}\t{segment[0]:10}\t{segment[1]:10}\t{duration}'.format(
                n=i, segment=seg, duration=abs(seg),
            ), file=out,
        )


def latest(args, out):
    """Worker for the --latest option

    Parameters
    ----------
    args : `argparse.Namespace`
        the parsed command-line options.

    out : `file`
        the open file object to write to.

    Returns
    -------
    exitcode : `int` or `None`
        the return value of the action or `None` to indicate success.
    """
    cache = ui.find_latest(args.observatory, args.type, urltype=args.url_type,
                           on_missing='warn', host=args.server)
    return postprocess_cache(cache, args, out)


def filename(args, out):
    """Worker for the --filename option

    Parameters
    ----------
    args : `argparse.Namespace`
        the parsed command-line options.

    out : `file`
        the open file object to write to.

    Returns
    -------
    exitcode : `int` or `None`
        the return value of the action or `None` to indicate success.
    """
    cache = ui.find_url(args.filename, urltype=args.url_type,
                        on_missing='warn', host=args.server)
    return postprocess_cache(cache, args, out)


def show_urls(args, out):
    """Worker for the default (show-urls) option

    Parameters
    ----------
    args : `argparse.Namespace`
        the parsed command-line options.

    out : `file`
        the open file object to write to.

    Returns
    -------
    exitcode : `int` or `None`
        the return value of the action or `None` to indicate success.
    """
    cache = ui.find_urls(args.observatory, args.type,
                         args.gpsstart, args.gpsend,
                         match=args.match, urltype=args.url_type,
                         host=args.server, on_gaps='ignore')
    return postprocess_cache(cache, args, out)


def postprocess_cache(cache, args, out):
    """Post-process a cache produced from a DataFind query

    This function checks for gaps in the file coverage, prints the cache
    in the requested format, then prints gaps to stderr if requested.
    """
    # if searching for SFTs replace '.gwf' file suffix with '.sft'
    if args.type is not None and 'SFT' in args.type:
        for idx in range(len(cache)):
            cache[idx].path = re.sub('.gwf', '.sft', cache[idx].path)

    # determine output format for a given URL
    if args.lal_cache:
        fmt = str
    elif args.names_only:
        fmt = attrgetter('path')
    elif args.frame_cache:
        cache = to_wcache(cache)

        def fmt(entry):
            return ('{e.observatory} {e.description} {e.segment[0]} '
                    '{e.segment[1]} {duration} {e.path}'.format(
                        e=entry, duration=abs(entry.segment)))
    else:
        fmt = attrgetter('url')

    for entry in cache:
        print(fmt(entry), file=out)

    # check for gaps
    if args.gaps:
        span = segments.segment(args.gpsstart, args.gpsend)
        seglist = segments.segmentlist(e.segment for e in cache).coalesce()
        missing = (segments.segmentlist([span]) - seglist).coalesce()
        if missing:
            print("Missing segments:\n", file=sys.stderr)
            for seg in missing:
                print("%f %f" % tuple(seg), file=sys.stderr)
            if span in missing:
                return 2
            return 1


def main(args=None):
    """Run the thing
    """
    # parse command line
    parser = command_line()
    opts = parser.parse_args(args=args)
    opts.show_urls = not any((opts.ping, opts.show_observatories,
                              opts.show_types, opts.show_times,
                              opts.filename, opts.latest))
    check_options(parser, opts)

    # open output
    if opts.output_file:
        out = open(opts.output_file, 'w')
    else:
        out = sys.stdout

    # run query
    if opts.ping:
        return ping(opts, out)
    if opts.show_observatories:
        return show_observatories(opts, out)
    if opts.show_types:
        return show_types(opts, out)
    if opts.show_times:
        return show_times(opts, out)
    if opts.latest:
        return latest(opts, out)
    if opts.filename:
        return filename(opts, out)
    return show_urls(opts, out)


if __name__ == '__main__':
    sys.exit(main())
