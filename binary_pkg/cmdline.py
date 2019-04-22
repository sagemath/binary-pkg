# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import sys
import argparse

import logging
logging.basicConfig()
log = logging.getLogger()

from binary_pkg.config import Configuration
from binary_pkg.git_interface import git_clone
from binary_pkg.package import Packager


description = """
Build binary packages
""".strip()


def make_parser():
    parser = argparse.ArgumentParser(description=description, add_help=False)
    parser.add_argument('-h', dest='option_help', action='store_true',
                        default=False, 
                        help='show this help message and exit')
    parser.add_argument('--debug', dest='debug', action='store_true',
                        default=False, 
                        help='debug')
    parser.add_argument('--log', dest='log', default=None,
                        help='one of [DEBUG, INFO, ERROR, WARNING, CRITICAL]')
    parser.add_argument('--config', required=True, help='Configuration yaml file')
    parser.add_argument('--package', default='',
                        help='name of the package section (in the Configuration yaml file)'
                             ' to create. Only used in stage and dist steps.')
    parser.add_argument('--checkout', default=False, action='store_true',
                        help='Checkout source')  
    parser.add_argument('--build', default=False, action='store_true',
                        help='Build')  
    parser.add_argument('--stage', default=False, action='store_true',
                        help='Copy to staging and analyze')  
    parser.add_argument('--dist', default=False, action='store_true',
                        help='Build file archive')  
    parser.add_argument('--info', default=False, action='store_true',
                        help='Show information')  
    return parser


def pick_package(config, package_name):
    if not package_name:
        return config.package[0]
    for package in config.package:
        if package.name == package_name:
            log.debug('Package {0} matches {1}'.format(package.name, package_name))
            return package
        log.debug('Package {0} does not match {1}'.format(package.name, package_name))
    raise ValueError('Unknown package name: {0}'.format(package_name))


def launch():
    parser = make_parser()
    args = parser.parse_args(sys.argv[1:])
    print(args)
    if args.log is not None:
        level = getattr(logging, args.log)
        log.setLevel(level=level)
    config = Configuration(args.config)
    if args.checkout:
        git_clone(config)
    if args.build:
        config.build_script.run()
    package = pick_package(config, args.package)
    if args.stage:
        Packager(config, package).copy().strip().save_relocate_script()
    if args.dist:
        package.dist_script.run()

        
if __name__ == '__main__':
    launch()
