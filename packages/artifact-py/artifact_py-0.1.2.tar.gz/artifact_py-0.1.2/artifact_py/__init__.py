# artifact_py: the design documentation tool made for everyone.
#
# Copyright (C) 2019 Rett Berg <github.com/vitiral>
#
# The source code is Licensed under either of
#
# * Apache License, Version 2.0, ([LICENSE-APACHE](LICENSE-APACHE) or
#   http://www.apache.org/licenses/LICENSE-2.0)
# * MIT license ([LICENSE-MIT](LICENSE-MIT) or
#   http://opensource.org/licenses/MIT)
#
# at your option.
#
# Unless you explicitly state otherwise, any contribution intentionally submitted
# for inclusion in the work by you, as defined in the Apache-2.0 license, shall
# be dual licensed as above, without any additional terms or conditions.
from __future__ import print_function, unicode_literals, division
"""
A reimiging of artifact.

See README.md and #SPC-design
"""
import sys
import argparse
import json
import yaml

from . import utils
from . import load
from . import dump


def main(argv):
    """Main function for cmdline."""
    parser = argparse.ArgumentParser(
        description='The design documentation tool for everyone.')

    parser.add_argument('--doc',
                        help="Change the root design doc.",
                        default="./README.md")

    subparsers = parser.add_subparsers(
        help='There are multiple types of commands you can perform.',
        dest='mode')

    # export
    parser_export = subparsers.add_parser(
        'export', help='export the designs to stdout or an output.')
    parser_export.add_argument('-o', '--output', help='path to output file')
    parser_export.add_argument(
        '-i',
        '--inplace',
        action='store_true',
        help='whether to export inplace. Only valid with --format md')
    parser_export.add_argument(
        '--format',
        help='format to output to on of [json, yaml, md]',
        default='md')

    # completion
    parser_show = subparsers.add_parser('show',
                                        help='show various information')
    parser_show.add_argument(
        'type', help='the type of information to show. One of [spc, tst]')

    # TODO: add lint

    args = parser.parse_args(argv)

    def fail(msg, print_help=False):
        print(msg)
        if print_help:
            parser.print_help()
        return 1

    if args.mode is None:
        return fail("must specify a mode", print_help=True)

    project = load.from_root_file(args.doc)
    artifacts = project.artifacts

    if args.mode == 'export':
        output = None
        try:
            if args.inplace:
                if args.format != 'md':
                    return fail("if --inplace requires --format=md")
                output = open(args.doc, 'w')
            elif args.output:
                output = open(args.output, 'w')
            else:
                output = sys.stdout

            if args.format == 'json':
                json.dump(project.serialize(), output)
            elif args.format == 'yaml':
                yaml.safe_dump(project.serialize(), output)
            elif args.format == 'md':
                utils.write_lines(dump.dump_project(project), output)
            else:
                return fail("Unrecognized --format: " + args.format,
                            print_help=True)

            utils.flush_output(output)
        finally:
            if output and output is not sys.stdout:
                output.close()

    elif args.mode == 'show':
        length = len(artifacts)
        if args.type == 'spc':
            for a in sorted(artifacts, key=lambda a: a.name):
                print('{}\t{}'.format(a.name.key, a.completion.spc))
        elif args.type == 'tst':
            for a in sorted(artifacts, key=lambda a: a.name):
                print('{}\t{}'.format(a.name.key, a.completion.tst))
        else:
            return fail("Unrecognized type: " + args.type, print_help=True)

    else:
        return fail("Unrecognized mode: " + args.mode, print_help=True)

    return 0
