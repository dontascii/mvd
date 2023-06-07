import rich_click as click
from mvd.main import pass_environment


@click.command(name="members", short_help="Returns the collection of strings "
                                          "for the given key.")
@click.argument("key", required=True)
@pass_environment
def cli(ctx, key):
    """
    Returns the collection of strings for the given key.
    Return order is not guaranteed.
    Returns an error if the key does not exists.
    """
    result = ""
    if key is None or not ctx.dictionary.key_exists(key):
        print("Error: Key not found")
        return "Error: Key not found."
    else:
        members = [val for val in ctx.dictionary.get_values_for_key(key)]
        for member in members:
            print(member)
            result += f"\n{member}"
    return result
