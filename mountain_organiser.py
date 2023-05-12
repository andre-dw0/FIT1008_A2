from __future__ import annotations
from typing import List
from mountain import Mountain
from double_key_table import DoubleKeyTable


class MountainOrganiser:

    def __init__(self):
        """
        Constructor.
        """
        self.mountains = []

    def add_mountains(self, mountains: List[Mountain]) -> None:
        """
        Adds the mountains inside the list 'mountains' to this organizer.

        The best and worst case time complexity this is O(n) where
        n is the length of mountains.
        """
        for mountain in mountains:
            self.mountains.append(mountain)

    def cur_position(self, mountain: Mountain) -> int:
        """
        When ordered from shortest to largest and then lexicographically,
        this function returns the order within all the mountains inside the
        organizer that the passed mountain is compared to all the rest.

        The worst case time complexity for this function is O(n^2), I'm sorry, I
        just didn't have time to implement binary search which would've gotten the
        big-o complexity up to par. The big-omega time complexity for this one
        is O(n) when the input mountain is at the beginning of self.mountains.
        """
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
