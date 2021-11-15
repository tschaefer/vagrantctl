# -*- coding: utf-8 -*-

import os
import subprocess
from vagrant import Vagrant


class Control(Vagrant):

    def list(self):
        vms = list()
        for root, dirs, files in os.walk(self.root):
            for file in files:
                if file == 'Vagrantfile':
                    vms.append(os.path.basename(root))
        return vms

    def snapshot_take(self, name):
        self._call_vagrant_command(['snapshot', 'take', name])

    def snapshot_delete(self, name):
        self._call_vagrant_command(['snapshot', 'delete', name])

    def snapshot_go(self, name):
        self._call_vagrant_command(['snapshot', 'go', name])

    def config(self):
        return os.path.join(self.root, 'Vagrantfile')
