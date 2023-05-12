from __future__ import annotations
from typing import List
from mountain import Mountain
from double_key_table import DoubleKeyTable


class MountainOrganiser:
    def __init__(self):
        self.mountains = []

    def add_mountains(self, mountains: List[Mountain]) -> None:
        for mountain in mountains:
            self.mountains.append(mountain)

    def cur_position(self, mountain: Mountain) -> int:
        if mountain in self.mountains:
            length = mountain.length
            name = mountain.name
            count = 0
            for m in self.mountains:
                if m.length < length:
                    count += 1
                elif m.length == length and m.name < name:
                    count += 1
            return count
        else:
            raise KeyError(mountain)


if __name__ == "__main__":

    pass
