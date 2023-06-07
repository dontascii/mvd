import rich_click as click
from mvd.main import pass_environment


@click.command(name="items",
               short_help="Returns all keys in the dictionary and all of " +
                          "their members.")
@pass_environment
def cli(ctx):
    """
    Returns all keys in the dictionary and all of their members.
    Returns nothing if there are none. Order is not guaranteed.
    """
    result = ""
    for key, values in ctx.dictionary.get_dictionary().items():
        for v in values:
            print(f"{key}: {v}")
            result += f"\n{key}: {v}"
    return result
