# -*- coding: utf-8 -*-

import sys
import os
import argparse
from control import VagrantControl


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


def run(args):
    if hasattr(args, 'vm'):
        root = os.path.join(args.base_directory, args.vm)
    else:
        root = args.base_directory

    if hasattr(args, 'verbose') and args.verbose:
        vagrantctl = VagrantControl(root=root, quiet_stdout=False,
                                    quiet_stderr=False)
    else:
        vagrantctl = VagrantControl(root=root)

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


def main():
    args = parse_options()
    run(args)


if __name__ == '__main__':
    main()
