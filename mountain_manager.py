from double_key_table import DoubleKeyTable
from mountain import Mountain
from algorithms.mergesort import mergesort


class MountainManager:

    def __init__(self) -> None:
        self.mountain_table = DoubleKeyTable()

    def add_mountain(self, mountain: Mountain) -> None:
        self.mountain_table[str(mountain.difficulty_level),
                            mountain.name] = mountain

    def remove_mountain(self, mountain: Mountain) -> None:
        del self.mountain_table[str(mountain.difficulty_level), mountain.name]

    def edit_mountain(self, old: Mountain, new: Mountain) -> None:
        self.remove_mountain(old)
        self.add_mountain(new)

    def mountains_with_difficulty(self, diff: int) -> list[Mountain]:
        return self.mountain_table.values(str(diff))

    def group_by_difficulty(self) -> list[list[Mountain]]:
        mountains, keys = [], []
        sorted_values = mergesort(self.mountain_table.values())
        for value in sorted_values:
            if value.difficulty_level not in keys:
                keys.append(value.difficulty_level)
        for key in keys:
            diff_list = []
            for value in sorted_values:
                if value.difficulty_level == int(key):
                    diff_list.append(value)
            mountains.append(diff_list)
        return mountains
