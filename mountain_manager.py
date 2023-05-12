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
        del self.mountain_table[mountain.difficulty_level, mountain.name]

    def edit_mountain(self, old: Mountain, new: Mountain):
        self.remove_mountain(old)
        self.add_mountain(new)

    def mountains_with_difficulty(self, diff: int):
        return self.mountain_table.values(str(diff))

    def group_by_difficulty(self):
        mountains = self.mountain_table.values()
        sorted_mountains = mergesort(
            mountains, key=lambda m: m.difficulty_level)
        result = []
        i = 0
        while i < len(sorted_mountains):
            diff = sorted_mountains[i].difficulty_level
            diff_group = []
            while i < len(sorted_mountains) and sorted_mountains[i].difficulty_level == diff:
                diff_group.append(sorted_mountains[i])
                i += 1
            result.append(diff_group)
        return result


def make_set(my_list):
    """
    Since mountains are unhashable, add a method to get a set of all mountain ids.
    Ensures that we can compare two lists without caring about order.
    """
    return set(id(x) for x in my_list)


if __name__ == '__main__':
    m1 = Mountain("m1", 2, 2)
    m2 = Mountain("m2", 2, 9)
    m3 = Mountain("m3", 3, 6)
    m4 = Mountain("m4", 3, 1)
    m5 = Mountain("m5", 4, 6)
    m6 = Mountain("m6", 7, 3)
    m7 = Mountain("m7", 7, 7)
    m8 = Mountain("m8", 7, 8)
    m9 = Mountain("m9", 7, 6)
    m10 = Mountain("m10", 8, 4)

    mm = MountainManager()
    mm.add_mountain(m1)
    mm.add_mountain(m2)
    mm.add_mountain(m3)
    mm.add_mountain(m6)
    mm.add_mountain(m7)

    print(list(mm.mountain_table.array))

    print(make_set(mm.mountains_with_difficulty(3)), make_set([m3]))
    print(make_set(mm.mountains_with_difficulty(4)), make_set([]))
    print(make_set(mm.mountains_with_difficulty(7)), make_set([m6, m7]))

    mm.add_mountain(m4)
    mm.add_mountain(m5)
    mm.add_mountain(m8)
    mm.add_mountain(m9)

    res = mm.group_by_difficulty()
    print(len(res), 4)
    print(make_set(res[0]), make_set([m1, m2]))
    print(make_set(res[1]), make_set([m3, m4]))
    print(make_set(res[2]), make_set([m5]))
    print(make_set(res[3]), make_set([m6, m7, m8, m9]))

    mm.add_mountain(m10)
    mm.remove_mountain(m5)

    res = mm.group_by_difficulty()
    print(len(res), 4)

    print(make_set(res[3]), make_set([m10]))
    pass
