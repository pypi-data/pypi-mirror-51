# -*- coding: utf-8 -*-

import logging

import yaml

from dt_shell.utils import format_exception
from .exceptions import *

logging.basicConfig()

dtslogger = logging.getLogger('dts')
dtslogger.setLevel(logging.DEBUG)

__version__ = '4.0.25'

dtslogger.info('duckietown-shell %s' % __version__)
import sys, locale

dtslogger.debug(f'encoding: stdout {sys.stdout.encoding} stderr {sys.stderr.encoding} '
                f'locale {locale.getpreferredencoding()}.')

import sys

if sys.version_info < (3, 6):
    msg = 'duckietown-shell works with Python 3.6 and later.\nDetected %s.' % str(sys.version)
    sys.exit(msg)


class OtherVersions(object):
    name2versions = {}


import termcolor

from .cli import DTShell, dts_print

from .dt_command_abs import DTCommandAbs
from .dt_command_placeholder import DTCommandPlaceholder


def cli_main():
    from .col_logging import setup_logging_color
    setup_logging_color()

    known_exceptions = (InvalidEnvironment, CommandsLoadingException)
    try:
        cli_main_()
    except UserError as e:

        msg = str(e)
        dts_print(msg, 'red')
        print_version_info()
        sys.exit(1)
    except known_exceptions as e:
        msg = str(e)
        dts_print(msg, 'red')
        print_version_info()
        sys.exit(1)
    except SystemExit:
        raise
    except KeyboardInterrupt:
        dts_print('User aborted operation.')
        pass
    except BaseException as e:
        msg = format_exception(e)
        dts_print(msg, 'red', attrs=['bold'])
        print_version_info()
        sys.exit(2)


def print_version_info():
    v = OtherVersions.name2versions
    v['python'] = sys.version
    v['duckietown-shell'] = __version__

    v['encodings'] = {'stdout': sys.stdout.encoding,
                      'stderr': sys.stderr.encoding,
                      'locale': locale.getpreferredencoding()}

    versions = yaml.dump(v, default_flow_style=False)
    # Please = termcolor.colored('Please', 'red', attrs=['bold'])
    msg = f'''\
If you think this is a bug, please report that you are using:

{versions}
'''
    dts_print(msg, 'red')


def cli_main_():
    from .env_checks import abort_if_running_with_sudo
    abort_if_running_with_sudo()
    # Problems with a step in the Duckiebot operation manual?
    #
    #     Report here: https://github.com/duckietown/docs-opmanual_duckiebot/issues

    # TODO: register handler for Ctrl-C
    url = href("https://github.com/duckietown/duckietown-shell-commands/issues")
    msg = """

Problems with a command?

Report here: {url}

Troubleshooting:

- If some commands update fail, delete ~/.dt-shell/commands

- To reset the shell to "factory settings", delete ~/.dt-shell

  (Note: you will have to re-configure.)

    """.format(url=url)
    dts_print(msg)

    from .exceptions import InvalidEnvironment, UserError

    shell = DTShell()
    arguments = sys.argv[1:]

    if arguments:
        from dt_shell.utils import replace_spaces
        arguments = map(replace_spaces, arguments)
        cmdline = " ".join(arguments)
        shell.onecmd(cmdline)
    else:
        shell.cmdloop()


def href(x):
    return termcolor.colored(x, 'blue', attrs=['underline'])
