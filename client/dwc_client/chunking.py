
from typing import Iterable

import os
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass(frozen=True, order=True)
class Chunk:
    command_id: str
    file: os.PathLike
    payload: str
    encoding: str = "utf-8"


def chunk_by_file(command_id: str, files: Iterable[os.PathLike]) -> Chunk:
    for path in (Path(pathlike) for pathlike in files):
        path_text = path.read_text()

        yield Chunk(
            command_id=command_id,
            payload=path_text,
            file=str(path),
        )