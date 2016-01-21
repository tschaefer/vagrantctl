# -*- coding: utf-8 -*-

import sys
import os
import argparse
from core import Control


def stype(bytestring):
    unicode_string = bytestring.decode(sys.getfilesystemencoding())
    return unicode_string


def parse_options():
    base_directory = os.getcwd()

    parser = argparse.ArgumentParser(description='vagrantctl')
    parser.add_argument('-b', '--base-directory',
                        type=unicode,
                        default=base_directory,
                        help='vm base directory')
    subparsers = parser.add_subparsers()

    parser_list = subparsers.add_parser('list')
    parser_list.set_defaults(list=True)

    parser_up = subparsers.add_parser('up')
    parser_up.set_defaults(up=True)
    parser_up.add_argument('vm',
                           type=stype,
                           help='vm name')
    parser_up.add_argument('-v', '--verbose',
                           action='store_true',
                           help='verbose output')

    parser_halt = subparsers.add_parser('halt')
    parser_halt.set_defaults(halt=True)
    parser_halt.add_argument('vm',
                             type=stype,
                             help='vm name')
    parser_halt.add_argument('-v', '--verbose',
                             action='store_true',
                             help='verbose output')

    parser_status = subparsers.add_parser('status')
    parser_status.set_defaults(status=True)
    parser_status.add_argument('vm',
                               type=stype,
                               help='vm name')

    return parser.parse_args()


def _build_root(args):
    root = args.base_directory
    if hasattr(args, 'vm'):
        root = os.path.join(root, args.vm)
    return root


def _build_obj(args, root):
    if hasattr(args, 'verbose') and args.verbose:
        return Control(root=root, quiet_stdout=False, quiet_stderr=False)
    return Control(root=root)


def _vm_exists(root):
    return os.path.exists(os.path.join(root, 'Vagrantfile'))


def run(args):
    root = _build_root(args)
    vagrantctl = _build_obj(args, root)
    if hasattr(args, 'vm') and not _vm_exists(root):
        print "no such vm '%s'" % os.path.basename(root)
        sys.exit(1)

    if hasattr(args, 'list'):
        for vm in vagrantctl.list():
            print vm
    elif hasattr(args, 'up'):
        vagrantctl.up()
    elif hasattr(args, 'halt'):
        vagrantctl.halt()
    elif hasattr(args, 'status'):
        for status in vagrantctl.status():
            print status[1]

    sys.exit(0)


def main():
    args = parse_options()
    run(args)


if __name__ == '__main__':
    main()
