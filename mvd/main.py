"""
entry point for multi-value dictionary (mvd) interactive
command-line tool
"""
import os
import yaml
from typing import List
import rich_click as click

from mvd.commands.environment import Environment, LazyClickGroup

click.rich_click.MAX_WIDTH = 80
click.rich_click.SHOW_ARGUMENTS = True
CONTEXT_SETTINGS = {"help_option_names": [
    "-h", "--help"], "show_default": True, "auto_envvar_prefix": "MVD"}

READ_ONLY_COMMANDS: List = ["items", "allmembers", "keyexist", "keys",
                            "memberexists", "members"]

pass_environment = click.make_pass_decorator(Environment, ensure=True)


@click.command(cls=LazyClickGroup, context_settings=CONTEXT_SETTINGS)
@click.option("-d",
              "--dict-file",
              type=click.Path(),
              allow_from_autoenv=True,
              help="dictionary will be loaded from, and saved to, " +
                   "this file. If this option is not used, the dictionary " +
                   "instance only lives in memory for the duration of the " +
                   "command. You can set a default value using the env variable " +
                   "`MVD_DICT_FILE` in your terminal session."
              )
@click.option("-v", "--verbose", is_flag=True, help="Enables verbose mode.")
@click.pass_context
@pass_environment
def cli(ctx, context: click.Context, verbose, dict_file):
    """ mvd - multi-value dictionary interactive cli.
     \f
     Args:
        ctx (mvd.commands.Environment): Environment 
        context (click.Context): The click.Context
        verbose (bool): --verbose flag
        dict_file (str): --dict-file argument 
    """
    ctx.verbose = verbose
    if dict_file is None:
        if context.invoked_subcommand not in [
            'cli'] and '--help' not in context.args:
            ctx.log("Warning: no dict_file set. The dictionary will be " +
                    "destroyed after this command completes. \n" +
                    "Use '-d <file>' option to persist dictionary to a file.\n")
    if dict_file is not None:
        ctx.dict_file = dict_file
        if os.path.exists(dict_file):
            try:
                with open(dict_file, mode="rb") as file:
                    ctx.dictionary._dict = yaml.safe_load(file.read())
                    ctx.vlog("dictionary successfully " +
                             f"loaded from file {dict_file}")
            except Exception:
                ...


@cli.result_callback()
@click.pass_context
@pass_environment
def process_result(ctx, context, result, verbose, dict_file):
    """
    This callback is invoked after every command.
    It will write the dictionary contents to yaml but only if
    the `-d` or `--dict-file` commandline argument was passed 
    and the dictionary has changed. 
    
    Args:
        ctx (mvd.commands.Environment): Environment 
        context (click.Context): the click.Context
        result (_type_): The Command result
        verbose (_type_): --verbose flag
        dict_file (_type_): --dict-file argument 
    """
    if dict_file is not None:
        do_save: bool = context.obj.do_save
        skip_ask: bool = False
        if context.invoked_subcommand in [READ_ONLY_COMMANDS]:
            do_save = False
        elif context.invoked_subcommand not in ['cli']:
            skip_ask = True
        if skip_ask or (
                do_save and click.confirm(f"Save changes to {dict_file}?")):
            with open(dict_file, mode="w", encoding="utf8") as file:
                yaml.dump(ctx.dictionary.get_dictionary(), file)
                ctx.vlog("dictionary successfully saved to " +
                         f"filesystem as {dict_file}")


if __name__ == '__main__':
    cli(None,None,False,"")
