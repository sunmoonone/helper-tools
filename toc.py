#!/usr/bin/env python
# encoding: utf-8
'''
tools.toc -- add table of contents to a markdown document

tools.toc is a tool that adds table of contents to a markdown document

@author:     sunmoonone

@copyright:  2016 organization_name. All rights reserved.

@license:    license

@contact:    zhangdan@huanqiu.com
@deffield    updated: Updated
'''

import sys
import os

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import re
import time

__all__ = []
__version__ = 0.1
__date__ = '2016-03-19'
__updated__ = '2016-03-19'

DEBUG = 0
TESTRUN = 0
PROFILE = 0


reg_header=re.compile('^(#+)\s+.*', re.I)

def add_toc(path, verbose=0):
    print 'adding toc'
    now=int(time.time())
    counter=0
    toc=[]
    lines=[]
    f = open(path, 'r+')
    try:
        for line in f:
            m = reg_header.match(line)
            if m:
                header = line.strip('# \n')
                anchor = 'anchor%s_%s' % (now,counter)
                counter += 1
                spaces=''.join(['    '] * (m.group(1).count('#') - 1))

                lines.append('<a name="%s"></a>\n' % anchor)
                item = '%s- [%s](#%s)\n' % (spaces, header, anchor)
                if verbose>0:
                    print item.rstrip('\n')

                toc.append(item)

            lines.append(line)
        if toc:
            toc.append('\n')
            f.seek(0)
            f.writelines(toc)
            f.writelines(lines)
    except Exception as e:
        print e
    finally:
        f.close()

def del_toc(path, verbose=0):
    print 'deleting existing toc'
        
    reg_item=re.compile('^\s*\- \[.*?\]\(#anchor\d+.*', re.I)
    reg_anchor=re.compile('^\<a name\="anchor\d+.*', re.I)
    lines=[]
    f = open(path, 'r+')
    try:
        skip=0
        for line in f:
            if reg_item.match(line) or reg_anchor.match(line):
                if verbose>0:
                    print 'rm',line.rstrip('\n')
                skip=1
                continue
            if skip and line.strip('\n')=='':
                skip=0
                continue
            skip=0

            lines.append(line)
        if lines:
            f.seek(0)
            f.truncate(0)
            f.writelines(lines)
    except Exception as e:
        print e
    finally:
        f.close()

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by sunmoonone on %s.
  Copyright 2016 organization_name. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        parser.add_argument('-r', '--remove', action='store_true', help="remove toc from document [default: false]")
        parser.add_argument('file', help='file path', metavar='FILE')
#         parser.add_argument(dest="paths", help="paths to folder(s) with source file(s) [default: %(default)s]", metavar="path", nargs='+')

        # Process arguments
        args = parser.parse_args()

        path = args.file
        verbose = args.verbose

        
        if args.remove:
            del_toc(path, verbose)
        else:
            del_toc(path, 0)
            add_toc(path, verbose)

        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception, e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-h")
        sys.argv.append("-v")
    if TESTRUN:
        import doctest
        doctest.testmod()
    sys.exit(main())