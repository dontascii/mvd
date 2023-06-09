import rich_click as click

from mvd.main import pass_environment
from mvd.dictionary.multivaluedict import ValueExistsException
@click.command(name="dict", short_help="returns a serialized " +
                                       "version of the dictionary ")

@pass_environment
def cli(ctx):
    """
    Returns a string representation of the dictionary
    (__repr__)
    """
    print(repr(ctx.dictionary.get_dictionary()))
    return repr(ctx.dictionary.get_dictionary())





