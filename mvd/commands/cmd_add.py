import rich_click as click

from mvd.main import pass_environment
from mvd.dictionary.multivaluedict import ValueExistsException


@click.command(name="add", short_help="Adds a member for a given key.")
@click.argument("key", required=True)
@click.argument("value", required=True )

@pass_environment
def cli(ctx, key, value):
    """
    Adds a key/value to the multiValueDict.
    If the key does not exist, it will be created automatically.
    If the value already exists, a ValueExistsException will be thrown.
    """
    if not key or not value:
        print("Error: Missing one or more required parameter(s).")
        return "Error: Missing one or more required parameter(s)."
    try:
        ctx.dictionary.add_item(key, value)
    except ValueExistsException:
        print("Error: The value already exists.")
        return "Error: The value already exists."
    except Exception as error:
        print("Error: An unhandled exception occurred.")
        return f"Error: An unhandled exception occurred. {error}"
    else:
        print("Added")
        return "Added"





