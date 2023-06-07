import rich_click as click

from mvd.main import pass_environment


@click.command(name="keys", short_help="Returns all the keys in the dictionary.")
@pass_environment
def cli(ctx):
    """Returns all the keys in the dictionary. Order is not guaranteed."""
    result: str = ""
    for key in ctx.dictionary.get_dictionary().keys():
        print(key)
        result += f"\n{key}"
    return result


