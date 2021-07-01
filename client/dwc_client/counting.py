import json
from dataclasses import dataclass

@dataclass(frozen=True, order=True)
class WordCount:
    words: int

    @classmethod
    def deserialize(cls, string: str) -> "WordCount":
       return  cls(**json.loads(string))