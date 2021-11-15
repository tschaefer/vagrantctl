# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='vagrantctl',
    version='0.0.1',
    packages=['vagrantctl', 'vagrantctl.core'],
    install_requires=['python-vagrant >= 0.5.10'],
    entry_points={'console_scripts': ['vagrantctl=vagrantctl.__main__:main']},
    author='Tobias Schäfer',
    author_email='vagrantctl@blackoxorg',
    url='https://github.com/tschaefer/vagrantctl',
    description="vagrantctl - Control the Vagrant virtual machines.",
    license='BSD',
    include_package_data=True,
    zip_safe=False
)
