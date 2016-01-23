# -*- coding: utf-8 -*-

import sys
import os
import argparse
from ConfigParser import SafeConfigParser
from core import Control


def stype(bytestring):
    unicode_string = bytestring.decode(sys.getfilesystemencoding())
    return unicode_string


def parse_config():
    config_file = os.path.join(os.environ['HOME'], '.vagrantctl')
    try:
        parser = SafeConfigParser()
        parser.read(config_file)
        base_directory = parser.get('vagrantctl', 'base-directory')
    except:
        base_directory = os.getcwd()

    return os.path.abspath(base_directory)


def parse_options(base_directory):
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

    parser_ssh_config = subparsers.add_parser('ssh-config')
    parser_ssh_config.set_defaults(ssh_config=True)
    parser_ssh_config.add_argument('vm',
                                   type=stype,
                                   help='vm name')

    return parser.parse_args()


def build_vm_root(args):
    root = args.base_directory
    if hasattr(args, 'vm'):
        root = os.path.join(root, args.vm)
    return root


def build_control_obj(args, root):
    if hasattr(args, 'verbose') and args.verbose:
        return Control(root=root, quiet_stdout=False, quiet_stderr=False)
    return Control(root=root)


def vm_exists(root):
    return os.path.exists(os.path.join(root, 'Vagrantfile'))


def print_error_exit(msg):
    err = "%s: %s\n" % (os.path.basename(sys.argv[0]), msg)
    sys.stderr.write(err)
    sys.exit(1)


def run(args):
    root = build_vm_root(args)
    vagrantctl = build_control_obj(args, root)
    if hasattr(args, 'vm') and not vm_exists(root):
        print_error_exit("no such vm '%s'" % args.vm)

    if hasattr(args, 'list'):
        for vm in vagrantctl.list():
            print vm
    elif hasattr(args, 'up'):
        vagrantctl.up()
    elif hasattr(args, 'halt'):
        vagrantctl.halt()
    if hasattr(args, 'status'):
        for status in vagrantctl.status():
            print status[1]
    elif hasattr(args, 'ssh_config'):
        try:
            print vagrantctl.ssh_config()
        except:
            print_error_exit("vm '%s' not up" % args.vm)

    sys.exit(0)


def main():
    args = parse_options(parse_config())
    run(args)


if __name__ == '__main__':
    main()
