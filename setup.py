# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='vagrantctl',
    version='0.0.1',
    packages=['vagrantctl'],
    install_requires=[],
    entry_points={'console_scripts': ['vagrantctl=vagrant:main']},
    author='Tobias Schäfer',
    author_email='vagrantctl@blackoxorg',
    url='https://github.com/tschaefer/vagrantctl',
    description="vagrantctl - Control the Vagrant containers.",
    license='BSD',
    include_package_data=True,
    zip_safe=False
)