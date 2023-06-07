import rich_click as click
from mvd.main import pass_environment


@click.command(name="memberexists", short_help="Returns whether a member "
                                               "exists in key.")
@click.argument("key", required=True)
@click.argument("value", required=True)
@pass_environment
def cli(ctx, key, value) -> str:
    """
    Returns whether a member exists within a key. Returns false if the key
    does not exist.
    """
    result: bool = ctx.dictionary.key_value_exists(key, value)
    print(result)
    return str(result)
