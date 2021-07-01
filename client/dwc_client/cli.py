import os.path
import yaml
import click
import glob
import uuid
from typing import Tuple
from pathlib import Path

from . import kafka, chunking
from .counting import WordCount

default_config_path = Path(__file__).parent/"config.yml"

@click.option(
    "-w", "--words",
    help="Print the word counts.",
    is_flag=True,
)
@click.argument(
    "file",
    nargs=-1, # Unlimited number of file arguments
    required=True, # Make sure we get at-least 1
    type=click.Path(),
)
@click.command()
def dwc(words: bool, file: Tuple[str, ...]):
    """
    A distributed version of the unix wc utility.

    Print newline, word, and byte counts for each FILE, and a
    total if multiple files are specified.

    If no file is given, standard input will be used.
    """
    config = yaml.safe_load(default_config_path.read_text())

    produce_from = kafka.produce(
        topic="chunks",
        bootstraps=config["kafka-bootstraps"],
    )

    files = (p for path in file 
             for p in glob.glob(path)
             if not os.path.isdir(p))

    command_id = uuid.uuid1().hex

    for record in produce_from(
        chunking.chunk_by_file(command_id, files)
    ):
        record.get()

    for result in kafka.consume(
        command_id,
        bootstraps=config["kafka-bootstraps"],
        deserializer=WordCount.deserialize,
    ):
        print(result)

