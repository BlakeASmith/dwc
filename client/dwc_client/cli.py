from typing import List
import click


@click.option(
    "-w", "--words",
    help="Print the word counts.",
    is_flag=True,
)
@click.option(
    "-r", "--recursive",
    help="Read all files within directories, recursively."
)
@click.argument(
    "file",
    nargs=-1, # Unlimited number of file arguments
    required=True, # Make sure we get at-least 1
    type=click.Path(),
)
@click.command()
def dwc(words: bool, file: List[str]):
    """
    A distributed version of the unix wc utility.

    Print newline, word, and byte counts for each FILE, and a
    total if multiple files are specified.

    If no file is given, standard input will be used.
    """
    print(words)
    print(file)
