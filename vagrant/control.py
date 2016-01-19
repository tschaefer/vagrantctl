# -*- coding: utf-8 -*-

import os
import subprocess


class VagrantControl(object):

    def __init__(self, base_directory=None):
        self.base_directory = os.path.abspath(base_directory)

    def list(self):
        containers = list()
        for root, dirs, files in os.walk(self.base_directory):
            for file in files:
                if file == 'Vagrantfile':
                    containers.append(os.path.basename(root))
        return containers

    def start(self):
        return

    def stop(self):
        return

    def status(self, container):
        cwd = os.path.join(self.base_directory, container)
        process = subprocess.Popen(['vagrant', 'status', '--machine-readable'],
                                   cwd=cwd,
                                   stdout=subprocess.PIPE)
        output = process.communicate()
        return output[0].split('\n')[2].split(',')
