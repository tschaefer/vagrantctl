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
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='verbose output')

    subparsers = parser.add_subparsers()

    parser_list = subparsers.add_parser('list')
    parser_list.set_defaults(list=True)

    parser_up = subparsers.add_parser('up')
    parser_up.set_defaults(up=True)
    parser_up.add_argument('vm',
                           type=stype,
                           help='vm name')

    parser_halt = subparsers.add_parser('halt')
    parser_halt.set_defaults(halt=True)
    parser_halt.add_argument('vm',
                             type=stype,
                             help='vm name')

    parser_suspend = subparsers.add_parser('suspend')
    parser_suspend.set_defaults(suspend=True)
    parser_suspend.add_argument('vm',
                                type=stype,
                                help='vm name')

    parser_resume = subparsers.add_parser('resume')
    parser_resume.set_defaults(resume=True)
    parser_resume.add_argument('vm',
                               type=stype,
                               help='vm name')

    parser_reload = subparsers.add_parser('reload')
    parser_reload.set_defaults(reload=True)
    parser_reload.add_argument('vm',
                               type=stype,
                               help='vm name')

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

    parser_config = subparsers.add_parser('config')
    parser_config.set_defaults(config=True)
    parser_config.add_argument('-s', '--show',
                               action='store_true',
                               dest='config_show',
                               help='output Vagrantfile')
    parser_config.add_argument('vm',
                               type=stype,
                               help='vm name')

    if 'vagrant-vbox-snapshot' in \
            [plugin.name for plugin in Control().plugin_list()]:
        parser_snapshot = subparsers.add_parser('snapshot')
        parser_snapshot.set_defaults(snapshot=True)
        parser_snapshot.add_argument('-l', '--list',
                                     action='store_true',
                                     dest='snapshot_list',
                                     help='list snapshots')
        parser_snapshot.add_argument('-t', '--take',
                                     nargs=1,
                                     metavar='SNAPSHOT_NAME',
                                     dest='snapshot_take',
                                     help='take named snapshot')
        parser_snapshot.add_argument('-d', '--delete',
                                     nargs=1,
                                     metavar='SNAPSHOT_NAME',
                                     dest='snapshot_delete',
                                     help='delete named snapshot')
        parser_snapshot.add_argument('-g', '--go',
                                     nargs=1,
                                     metavar='SNAPSHOT_NAME',
                                     dest='snapshot_go',
                                     help='go to named snapshot')
        parser_snapshot.add_argument('vm',
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
    elif hasattr(args, 'suspend'):
        vagrantctl.suspend()
    elif hasattr(args, 'resume'):
        vagrantctl.resume()
    elif hasattr(args, 'reload'):
        vagrantctl.reload()
    elif hasattr(args, 'status'):
        for status in vagrantctl.status():
            print status[1]
    elif hasattr(args, 'ssh_config'):
        try:
            print vagrantctl.ssh_config()
        except:
            print_error_exit("vm '%s' not up" % args.vm)
    elif hasattr(args, 'snapshot'):
        if args.snapshot_take:
            vagrantctl.snapshot_take(args.snapshot_take.pop())
        elif args.snapshot_delete:
            vagrantctl.snapshot_delete(args.snapshot_delete.pop())
        elif args.snapshot_go:
            vagrantctl.snapshot_go(args.snapshot_go.pop())
        else:
            snapshots = vagrantctl.snapshot_list()
            for snapshot in snapshots[1:]:
                print snapshot
    elif hasattr(args, 'config'):
        if args.config_show:
            with open(vagrantctl.config()) as config:
                print config.read()
        else:
            print vagrantctl.config()

    sys.exit(0)


def main():
    args = parse_options(parse_config())
    run(args)


if __name__ == '__main__':
    main()
