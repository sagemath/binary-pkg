
import sys
import os
import argparse
import logging

from binary_pkg.config import Configuration
from binary_pkg.git_interface import git_clone


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
    parser.add_argument('--checkout', default=False, action='store_true',
                        help='Checkout source')  
    parser.add_argument('--build', default=False, action='store_true',
                        help='Build')  
    parser.add_argument('--package', default=False, action='store_true',
                        help='Package')  
    return parser


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
        config.build_script.run(cwd=config.source_path)

        
if __name__ == '__main__':
    launch()
