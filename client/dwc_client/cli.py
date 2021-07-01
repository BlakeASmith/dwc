import os.path
import yaml
import time
import click
import glob
import uuid
import multiprocessing as mp
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
    wc_args = []

    if words:
        wc_args.append("-w")

    config = yaml.safe_load(default_config_path.read_text())

    produce_from = kafka.produce(
        topic="chunks",
        bootstraps=config["kafka-bootstraps"],
    )

    files = (p for path in file 
             for p in glob.glob(path)
             if not os.path.isdir(p))

    command_id = uuid.uuid1().hex

    def watch_results():
        for result in kafka.consume(
            "results",
            bootstraps=config["kafka-bootstraps"],
            deserializer=lambda x: x,
        ):
            print(result)

    watch_results_process = mp.Process(target=watch_results)
    watch_results_process.start()

    time.sleep(0.5)

    for record in produce_from(
        chunking.chunk_by_file(command_id, wc_args, files)
    ):
        record.get()

    watch_results_process.join()
