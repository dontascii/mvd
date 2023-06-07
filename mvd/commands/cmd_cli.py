from mvd.main import pass_environment, LazyClickGroup
from mvd.cli.terminal import InteractiveCli

import rich_click as click


@click.command(name="cli", short_help="Starts the interactive cli")
@click.pass_context
@pass_environment
def cli(ctx, context):
    """Starts mvd's interactive command-line interface"""
    # For the interactive CLI, do_save is initially set to False.
    # If a command is issued in the interactive CLI that changes the dictionary,
    # do_save will be set to True and the user will be prompted to save on exit.
    context.obj.do_save = False
    term: InteractiveCli = InteractiveCli(context)
    term.start()


