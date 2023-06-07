import rich_click as click
from mvd.main import pass_environment



@click.command(name="allmembers", short_help="Returns all the members in the dictionary.")
@pass_environment
def cli(ctx):
    """
    Returns all the members in the dictionary.
    Returns nothing if there are none.
    Order is not guaranteed.
    """
    items = [v for values in
                ctx.dictionary.get_dictionary().values()
                for v in values]
    result = ""
    for x,value in enumerate(items):
        print(f"{x+1}. {value}")
        result += f"\n{x+1}. {value}"
    return result


