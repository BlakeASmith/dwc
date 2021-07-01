import yaml
import click
from typing import List
from pathlib import Path

from . import kafka

default_config_path = Path(__file__).parent/"config.yml"

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
def dwc(words: bool, file: List[str], recursive: bool):
    """
    A distributed version of the unix wc utility.

    Print newline, word, and byte counts for each FILE, and a
    total if multiple files are specified.

    If no file is given, standard input will be used.
    """
    config = yaml.safe_load(default_config_path.read_text())

    produce = kafka.produce(
        topic="chunks",
        bootstraps=config["kafka-bootstraps"],
    )

    for future in produce(
        ("foobar", {}) for _ in range(100)
    ):
        print(future.get())
