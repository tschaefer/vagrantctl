# -*- coding: utf-8 -*-

import os
from vagrant import Vagrant


class Control(Vagrant):

    def list(self):
        containers = list()
        for root, dirs, files in os.walk(self.root):
            for file in files:
                if file == 'Vagrantfile':
                    containers.append(os.path.basename(root))
        return containers
