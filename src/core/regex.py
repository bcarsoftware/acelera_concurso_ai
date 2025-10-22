from dataclasses import dataclass


@dataclass
class Regex:
    STRING_2_MIN = ".{2,}"
    STRING_4_MIN = ".{4,}"
