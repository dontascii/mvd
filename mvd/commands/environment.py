"""
environment.py
author: dontascii
email: dontascii@duck.com
copyright 2023 - Joel Clegg
"""
import os
import sys
from typing import Set, List, Union
import rich_click as click
from rich_click.cli import RichGroup

import mvd.dictionary.multivaluedict as multivaluedict


class Environment:
    """
    An instance of this class is used as the object of a Click pass decorator
    (@pass_environment).  All click commands in the './commands' folder should
    have the function :func:`cli`, and it should be decorated with
    '@pass_environment'.
    The functionality provided by :meth:`click.make_pass_decorator` allows a
    single instance to be passed through and shared with each sub-command,
    making it a perfect place for our :class:`MultiValueDict` class
    to be instantiated.
    """

    def __init__(self):
        self.verbose: bool = False
        self.dict_file: Union[str, None] = None
        self.do_save: bool = True
        self.dictionary: multivaluedict.MultiValueDict[
            str, Set[str]] = multivaluedict.MultiValueDict()

    def log(self, msg: str, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)

    def vlog(self, msg, *args):
        """Logs a message to stderr only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)


class LazyClickGroup(RichGroup):
    """
    custom click.Group that provides dynamic loading
    of sub-commands
    """
    cmd_folder = os.path.abspath(os.path.dirname(__file__))

    def list_commands(self, ctx) -> List[str]:
        rv = []
        for filename in os.listdir(self.cmd_folder):
            if filename.endswith(".py") and filename.startswith("cmd_"):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            mod = __import__(f"mvd.commands.cmd_{name}", None, None, ["cli"])
        except ImportError:
            return
        if hasattr(mod, 'cli'):
            return mod.cli
