from double_key_table import DoubleKeyTable
from mountain import Mountain
from algorithms.mergesort import merge, mergesort


class MountainManager:

    def __init__(self) -> None:
        self.mountain_table = DoubleKeyTable()

    def add_mountain(self, mountain: Mountain) -> None:
        self.mountain_table[str(mountain.difficulty_level),
                            mountain.name] = mountain

    def remove_mountain(self, mountain: Mountain) -> None:
        del self.mountain_table[mountain.difficulty_level, mountain.name]

    def edit_mountain(self, old: Mountain, new: Mountain):
        self.remove_mountain(old)
        self.add_mountain(new)

    def mountains_with_difficulty(self, diff: int):
        return self.mountain_table.keys(str(diff))

    def group_by_difficulty(self):
        mountain_lists = []
        for difficulty_level in self.keys():
            mountain_list = self.mountain_table.keys(
                difficulty_level)
            mountain_list = mergesort(mountain_list, key=lambda m: m.name)
            mountain_lists.append(mountain_list)
        mountain_lists = mergesort(
            mountain_lists, key=lambda lst: lst[0].difficulty)
        return mountain_lists
