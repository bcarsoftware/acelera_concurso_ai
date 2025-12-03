from re import compile

from dataclasses import dataclass


@dataclass
class Regex:
    STRING_2_MIN = compile(r".{2,}")
    STRING_4_MIN = compile(r".{4,}")
