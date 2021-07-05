import glob
import os
from pathlib import Path
from typing import Tuple
from click.core import F
from tabulate import tabulate

import click
import dask.bag
from dask.distributed import Client


@click.option(
    "-w", "--words",
    help="Print the word counts.",
    is_flag=True,
)
@click.option(
    "-c", "--bytes",
    help="Print the byte counts.",
    is_flag=True,
)
@click.option(
    "-l", "--lines",
    help="Print the line counts.",
    is_flag=True,
)
@click.option(
    "-a", "--address",
    help="Address of a dask scheduler. A multiprocess scheduler is used by default.",
    default=None,
)
@click.argument(
    "file",
    nargs=-1, # Unlimited number of file arguments
    required=True, # Make sure we get at-least 1
    type=click.Path(),
)
@click.command()
def dwc(words: bool, bytes: bool, lines: bool, address: str, file: Tuple[str, ...]):
    """
    A distributed version of the unix wc utility.

    Print newline, word, and byte counts for each FILE, and a
    total if multiple files are specified.

    If no file is given, standard input will be used.
    """
    if not words and not bytes and not lines:
        words = bytes = lines = True

    files = list(Path(p) for path in file 
             for p in glob.glob(path)
             if not os.path.isdir(p))

    if address is not None:
        client = Client(address)

    bags = dask.bag.from_sequence(files).map(dask.bag.read_text)

    def process_bag(bag):
        line_count = (
            bag
            .count()
            .compute()
        )

        word_count = (
            bag
            .map(lambda it: it.split())
            .map(len)
            .sum()
            .compute()
        )

        byte_count = (
            bag
            .map(len)
            .sum()
            .compute()
        )

        return line_count, word_count, byte_count

    bags = bags.map(process_bag)

    tlc, twc, tbc = 0, 0, 0
    rows = []

    for file, (lc, wc, bc) in zip(files, bags.compute()):
        row = []
        if lines:
            row.append(lc)
        if words:
            row.append(wc)
        if bytes:
            row.append(bc)

        row.append(file)

        rows.append(row)

        tlc += lc
        twc += wc
        tbc += bc

    if len(files) > 1:
        row = []
        if lines:
            row.append(tlc)
        if words:
            row.append(twc)
        if bytes:
            row.append(tbc)

        row.append("total")
        rows.append(row)

    print(tabulate(rows, tablefmt="plain"))


