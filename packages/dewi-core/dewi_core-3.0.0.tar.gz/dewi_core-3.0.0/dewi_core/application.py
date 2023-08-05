# Copyright 2015-2019 Laszlo Attila Toth
# Distributed under the terms of the GNU Lesser General Public License v3

import argparse
import collections
import os
import shlex
import sys
import traceback
import typing

from dewi_core.command import Command
from dewi_core.commandregistry import CommandRegistry
from dewi_core.loader.context import Context
from dewi_core.loader.loader import PluginLoader
from dewi_core.loader.plugin import Plugin
from dewi_core.logger import create_logger, LoggerType, LogLevel, log_debug
from dewi_core.utils.levenstein import get_similar_names_to


class EmptyPlugin(Plugin):
    def get_description(self) -> str:
        return 'Default plugin which does nothing'

    def load(self, c: Context):
        pass


def _list_commands(prog_name: str, command_registry: CommandRegistry, *, all_commands: bool = False):
    commands = dict()
    max_length = 0
    max_name_length = 0
    infix = '  - alias of '
    infix_len = len(infix)

    for name in command_registry.get_command_names():
        desc = command_registry.get_command_class_descriptor(name)
        command = desc.get_class()
        command_name = desc.get_name()

        if name == command_name:
            cmdname = name
            current_length = len(name)
        else:

            if not all_commands:
                continue
            cmdname = (name, command_name)
            current_length = len(name) + len(command_name) + infix_len

        if len(name) > max_name_length:
            max_name_length = len(name)

        if current_length > max_length:
            max_length = current_length

        commands[name] = (cmdname, command.description)

    format_str = "  {0:<" + str(max_length) + "}   -- {1}"
    alias_format_str = "{0:<" + str(max_name_length) + "}" + infix + "{1}"

    print(f'Available {prog_name.capitalize()} Commands.')
    for name in sorted(commands):
        cmdname, description = commands[name]
        if isinstance(cmdname, tuple):
            cmdname = alias_format_str.format(*cmdname)
        print(format_str.format(cmdname, description))


class _ListAllCommand(Command):
    name = 'list-all'
    description = 'Lists all available command with aliases'

    def run(self, args: argparse.Namespace):
        context: Context = args.context_
        _list_commands(args.program_name_, context.command_registry, all_commands=True)


class _ListCommand(Command):
    name = 'list'
    description = 'Lists all available command with their names only'

    def run(self, args: argparse.Namespace):
        context: Context = args.context_
        _list_commands(args.program_name_, context.command_registry)


class Application:
    def __init__(self, loader: PluginLoader, program_name: str, *,
                 fallback_to_plugin_name: typing.Optional[str] = None,
                 disable_plugins_from_cmdline: typing.Optional[bool] = None,
                 command_class: typing.Optional[typing.Type[Command]] = None
                 ):
        self._loader = loader
        self._program_name = program_name
        self._fallback_plugin_name = fallback_to_plugin_name or 'dewi_core.application.EmptyPlugin'
        self._disable_plugins_from_cmdline = disable_plugins_from_cmdline
        self._command_class = command_class

    def _parse_app_args(self, args: collections.Sequence):
        parser = argparse.ArgumentParser(
            prog=self._program_name,
            usage='%(prog)s [options] [command [command-args]]')

        if not self._disable_plugins_from_cmdline:
            parser.add_argument(
                '-p', '--plugin', help='Load this plugin. This option can be specified more than once.',
                default=[], action='append')

        parser.add_argument('--wait', action='store_true', help='Wait for user input before terminating application')
        parser.add_argument(
            '--print-backtraces', action='store_true',
            help='Print backtraces of the exceptions')
        parser.add_argument('--debug', '-d', action='store_true', help='Enable print/log debug messages')

        logging = parser.add_argument_group('Logging')
        logging.add_argument('-v', '--log-level', dest='log_level', help='Set log level, default: warning',
                             choices=[i.name.lower() for i in LogLevel], default='info')
        logging.add_argument('--log-syslog', dest='log_syslog', action='store_true',
                             help='Log to syslog. Can be combined with other log targets')
        logging.add_argument('--log-console', '--log-stdout', dest='log_console', action='store_true',
                             help='Log to STDOUT, the console. Can be combined with other targets.'
                                  'If no target is specified, this is used as default.')
        logging.add_argument('--log-file', dest='log_file', action='append',
                             help='Log to a file. Can be specified multiple times and '
                                  'can be combined with other options.')
        logging.add_argument('--no-log', '-l', dest='log_none', action='store_true',
                             help='Disable logging. If this is set, other targets are invalid.')

        parser.add_argument('command', nargs='?', help='Command to be run', default='list')
        parser.add_argument(
            'commandargs', nargs=argparse.REMAINDER, help='Additonal options and arguments of the specified command',
            default=[], )
        return parser.parse_args(args)

    def run(self, args: collections.Sequence):
        if self._command_class:
            args_ = []
            env_var_name = f'{self._program_name.replace("-", "_").upper()}_ARGS'
            if env_var_name in os.environ:
                args_ = shlex.split(os.environ[env_var_name])
            args_ += [self._command_class.name] + args
            args = args_

            self._disable_plugins_from_cmdline = True

        app_ns = self._parse_app_args(args)
        if app_ns.debug:
            app_ns.print_backtraces = True
            app_ns.log_level = 'debug'

        if self._process_logging_options(app_ns):
            sys.exit(1)

        if self._disable_plugins_from_cmdline:
            plugins = [self._fallback_plugin_name]
        else:
            plugins = app_ns.plugin or [self._fallback_plugin_name]

        try:
            log_debug('Loading plugins')
            context = self._loader.load(set(plugins))
            command_name = app_ns.command

            if self._command_class:
                context.commands.register_class(self._command_class)
                prog = self._program_name
            else:
                context.commands.register_class(_ListAllCommand)
                context.commands.register_class(_ListCommand)
                prog = '{} {}'.format(self._program_name, command_name)

            if command_name in context.command_registry:

                command_class = context.command_registry.get_command_class_descriptor(command_name).get_class()
                command = command_class()
                parser = argparse.ArgumentParser(
                    description=command.description,
                    prog=prog)

                command.register_arguments(parser)
                ns = parser.parse_args(app_ns.commandargs)
                ns.running_command_ = command_name
                ns.debug_ = app_ns.debug
                ns.print_backtraces_ = app_ns.print_backtraces
                ns.parser_ = parser
                ns.context_ = context
                ns.program_name_ = self._program_name

                log_debug('Starting command', name=command_name)
                sys.exit(command.run(ns))

            else:
                print(f"ERROR: The command '{command_name}' is not known.\n")
                similar_names = get_similar_names_to(command_name, sorted(context.command_registry.get_command_names()))

                if similar_names:
                    print('Similar names - firstly based on command name length:')
                    for name in similar_names:
                        print('  {:30s}   -- {}'.format(
                            name,
                            context.command_registry.get_command_class_descriptor(name).get_class().description))
                else:
                    print('NO similar command name.')

                    print('Available commands with aliases:')
                    for name in sorted(context.command_registry.get_command_names()):
                        print('  {:30s}   -- {}'.format(
                            name,
                            context.command_registry.get_command_class_descriptor(name).get_class().description))
                sys.exit(1)

        except SystemExit:
            self._wait_for_termination_if_needed(app_ns)
            raise
        except BaseException as exc:
            if app_ns.print_backtraces:
                einfo = sys.exc_info()
                tb = traceback.extract_tb(einfo[2])
                tb_str = 'An exception occured:\n  Type: %s\n  Message: %s\n\n' % \
                         (einfo[0].__name__, einfo[1])
                for t in tb:
                    tb_str += '  File %s:%s in %s\n    %s\n' % (t.filename, t.lineno, t.name, t.line)
                print(tb_str)
            print(exc, file=sys.stderr)
            self._wait_for_termination_if_needed(app_ns)
            sys.exit(1)

    def _process_logging_options(self, args: argparse.Namespace):
        if args.log_none:
            if args.log_syslog or args.log_file or args.log_console:
                print('ERROR: --log-none cannot be used any other log target,')
                print('ERROR: none of: --log-file, --log-console, --log-syslog')
                return 1
            create_logger(self._program_name, LoggerType.NONE, args.log_level, filenames=[])
        else:
            logger_types = []
            if args.log_console:
                logger_types.append(LoggerType.CONSOLE)
            if args.log_file:
                logger_types.append(LoggerType.FILE)
            if args.log_syslog:
                logger_types.append(LoggerType.SYSLOG)

            if not logger_types:
                # Using default logger
                logger_types = LoggerType.CONSOLE

            create_logger(self._program_name, logger_types, args.log_level, filenames=args.log_file)

    def _wait_for_termination_if_needed(self, app_ns):
        if app_ns.wait:
            print("\nPress ENTER to continue")
            input("")


class SinglePluginApplication(Application):
    def __init__(self, program_name: str, plugin_name: str):
        super().__init__(PluginLoader(), program_name, fallback_to_plugin_name=plugin_name,
                         disable_plugins_from_cmdline=True)


class SingleCommandApplication(Application):
    def __init__(self, program_name: str, command_class: typing.Type[Command]):
        super().__init__(PluginLoader(), program_name, command_class=command_class)
