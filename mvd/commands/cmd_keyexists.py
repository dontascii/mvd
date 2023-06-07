import rich_click as click
from mvd.main import pass_environment


@click.command(name="keyexists",
               short_help="Returns whether a key exists or not..")
@click.argument("key", required=True)
@pass_environment
def cli(ctx, key) -> str:
    """
    Returns True if the key exists, false otherwise
    """
    result = ctx.dictionary.key_exists(key)
    print(result)
    return str(result)
