import rich_click as click

from mvd.main import pass_environment
from mvd.dictionary.multivaluedict import KeyMissingException, \
    ValueMissingException


@click.command(name="removeall",
               short_help="Removes all members from a key and deletes the key.")
@click.argument("key", required=True)
@pass_environment
def cli(ctx, key: str):
    """
    Removes all members for a key and removes the key from the dictionary.
    Returns an error if the key does not exist.
    """
    try:
        ctx.dictionary.remove_key(key)
    except KeyMissingException as E:
        print(f"Error: Key was not found.")
        return "Error: Key was not found."
    except Exception:
        print(f"Error: An unhandled exception occurred.")
        return f"Error: An unhandled exception occurred."
    else:
        print("Removed")
        return "Removed"
