import rich_click as click

from mvd.main import pass_environment
from mvd.dictionary.multivaluedict import KeyMissingException, \
    ValueMissingException


@click.command(name="remove", short_help="Removes a member from a key.")
@click.argument("key", required=True)
@click.argument("value", required=True)
@pass_environment
def cli(ctx, key: str, value: str):
    """
    Removes a member from a key. If the last member is removed from the key,
    the key is removed from the dictionary. If the key or member does not
    exist, displays an error.
    """
    try:
        ctx.dictionary.remove_value_from_key(key, value)
    except ValueMissingException as E:
        print(f"Error: Value not found in key.")
        return f"Error: Value not found in key."
    except KeyMissingException as E:
        print(f"Error: Key was not found.")
        return f"Error: Key was not found."
    except Exception:
        print(f"Error: An unhandled exception occurred.")
        return f"Error: An unhandled exception occurred."
    else:
        print("Removed")
        return "Removed"
