"""
Handle Command Line Options
"""

import sys
import argparse
import yaml

import logging
log = logging.getLogger()

from toolaid_builder.config_file import ConfigurationFile


def debug_shell(app, parser):
    from IPython.terminal.ipapp import TerminalIPythonApp
    ip = TerminalIPythonApp.instance()
    ip.initialize(argv=[])
    ip.shell.user_global_ns['app'] = app
    ip.shell.user_global_ns['log'] = log
    ip.shell.user_global_ns['parser'] = parser
    def ipy_import(module_name, identifier):
        import importlib
        module = importlib.import_module(module_name)
        ip.shell.user_global_ns[identifier] = getattr(module, identifier) 
    ip.start()


description = """
ToolAid: Compile/install a local tools directory.
"""
    
    
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
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--show', action='store_true', default=False)
    group.add_argument('--build', action='store_true', default=False)
    group.add_argument('--build-pip', action='store_true', default=False)
    group.add_argument('--build-npm', action='store_true', default=False)
    group.add_argument('--build-gem', action='store_true', default=False)
    parser.add_argument('filenames', nargs=argparse.REMAINDER)
    return parser


def launch(repo_root):
    parser = make_parser()
    args = parser.parse_args(sys.argv[1:])
    if args.log is not None:
        level = getattr(logging, args.log)
        log.setLevel(level=level)
    from toolaid_builder.app import Application
    app = Application(repo_root)

    if args.debug:
        print(args)
        debug_shell(app, parser)
        return
    if args.option_help:
        parser.print_help()
        return

    action = None
    if args.show:
        action = app.show
    elif args.build:
        action = app.build
    elif args.build_pip:
        action = app.build_pip
    elif args.build_npm:
        action = app.build_npm
    elif args.build_gem:
        action = app.build_gem
    else:
        assert False, 'unreachable'
            
    for filename in args.filenames:
        config = ConfigurationFile(filename)
        action(config)
    
