from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Mountain:

    name: str
    difficulty_level: int
    length: int

    """
    Important:
    I've added two magic methods inside the Mountain class which I can use to
    order them by difficulty level. It's limited in a way since it only allows me
    order them by difficulty level at this stage but it serves my purpose well.
    """

    def __le__(self, other: Mountain) -> bool:
        return self.difficulty_level <= other.difficulty_level
