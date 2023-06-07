import rich_click as click

from mvd.main import pass_environment



@click.command(name="clear",
               short_help="Removes all keys and all values from the dictionary.")
@pass_environment
def cli(ctx):
    """
    Removes all keys and values from the dictionary.
    """
    try:
        ctx.dictionary.clear()
    except Exception:
        print(f"Error: An unhandled exception occurred.")
        return "Error: An unhandled exception occurred."
    else:
        print("Cleared")
        return "Cleared"
