from double_key_table import DoubleKeyTable
from mountain import Mountain
from algorithms.mergesort import mergesort


class MountainManager:

    def __init__(self) -> None:
        """
        Constructor.
        """
        self.mountain_table = DoubleKeyTable()

    def add_mountain(self, mountain: Mountain) -> None:
        """
        Adds a new mountain to the mountain manager.

        Best case complexity and worst case complexity are
        O(1) and O(m + n) respectively due to insertion into a hash table which
        uses linear probing. Worst case has a probe chain close to
        the size of the inner_table (n) or outer_table (m)
        """
        self.mountain_table[str(mountain.difficulty_level),
                            mountain.name] = mountain

    def remove_mountain(self, mountain: Mountain) -> None:
        """
        Removes a mountain from the mountain manager.

        Same as before. The best case complexity is O(1), the worst case
        complexity is O(m+n) where m is the size of the outer table and n
        is the size of the inner table.

        I believe since we are assuming that the best/worst case
        complexity of operations within the double hash table are O(1), that
        would mean this would also have a best/worst case complexity of O(1).
        """
        del self.mountain_table[str(mountain.difficulty_level), mountain.name]

    def edit_mountain(self, old: Mountain, new: Mountain) -> None:
        """
        Removes a specified mountain and adds another at the same time.

        Best case complexity is O(1), worst case complexity is O(m+n) as
        discussed in the above two functions.

        I believe since we are assuming that the best/worst case
        complexity of operations within the double hash table are O(1), that
        would mean this would also have a best/worst case complexity of O(1).
        """
        self.remove_mountain(old)
        self.add_mountain(new)

    def mountains_with_difficulty(self, diff: int) -> list[Mountain]:
        """
        Returns a list of mountains with the difficulty level of parameter 'diff'.

        We assume operations in the double keyed hash table are O(1),
        and therefore this operation has a best/worst case complexity
        of O(1). 
        """
        return self.mountain_table.values(str(diff))

    def group_by_difficulty(self) -> list[list[Mountain]]:
        """
        Returns a list of lists which each contain mountains of a different
        difficulty level. The outer list is sorted in ascending order based on
        the difficulty level of the mountains in each list.

        The Big-O time complexity of the list is O(n log(n)) due to the
        implementation of the merge sort algorithm. The best case time complexity
        for this list happens to also be O(n log(n)).
        """
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
