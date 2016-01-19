# -*- coding: utf-8 -*-

import sys
import os
import argparse
from control import VagrantControl

def stype(bytestring):
    unicode_string = bytestring.decode(sys.getfilesystemencoding())
    return unicode_string


def parse_options():
    base_directory = os.path.join(os.environ['HOME'], '.vagrant.d',
                                  'container')

    parser = argparse.ArgumentParser(description='vagrantctl')
    parser.add_argument('-b', '--base-directory',
                        type=unicode,
                        default=base_directory,
                        help='container base directory')
    subparsers = parser.add_subparsers()

    parser_list = subparsers.add_parser('list')
    parser_list.set_defaults(list=True)

    parser_start = subparsers.add_parser('start')
    parser_start.set_defaults(start=True)
    parser_start.add_argument('container',
                               type=stype,
                               help='container name')
    parser_start.add_argument('-v', '--verbose',
                               action='store_true',
                               help='verbose output')

    parser_stop = subparsers.add_parser('stop')
    parser_stop.set_defaults(stop=True)
    parser_stop.add_argument('container',
                               type=stype,
                               help='container name')
    parser_stop.add_argument('-v', '--verbose',
                               action='store_true',
                               help='verbose output')

    parser_status = subparsers.add_parser('status')
    parser_status.set_defaults(status=True)
    parser_status.add_argument('container',
                               type=stype,
                               help='container name')
    parser_status.add_argument('-v', '--verbose',
                               action='store_true',
                               help='verbose output')

    return parser.parse_args()


def run(args):
    vagrantctl = VagrantControl(args.base_directory)
    if hasattr(args, 'list'):
        for container in vagrantctl.list():
            print container
    elif hasattr(args, 'start'):
        print "start"
    elif hasattr(args, 'stop'):
        print "stop"
    elif hasattr(args, 'status'):
        status = vagrantctl.status(args.container)
        print status[3]

def main():
    args = parse_options()
    run(args)


if __name__ == '__main__':
    main()
