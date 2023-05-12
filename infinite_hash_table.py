from __future__ import annotations
from typing import Generic, TypeVar

from data_structures.referential_array import ArrayR

K = TypeVar("K")
V = TypeVar("V")


class InfiniteHashTable(Generic[K, V]):
    """
    Infinite Hash Table.

    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise `hash` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """
    TABLE_SIZE = 27

    def __init__(self):
        self.level = 0
        self.array = ArrayR(self.TABLE_SIZE)

    def hash(self, key: K) -> int:
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE-1)
        return self.TABLE_SIZE-1

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """
        position = self.hash(key)
        if self.array[position] is None:
            raise KeyError(key)
        else:
            if isinstance(self.array[position], InfiniteHashTable):
                return self.array[position][key]
            else:
                return self.array[position]

    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """
        position = self.hash(key)
        if self.array[position] is not None:
            # Need to account for none first
            if isinstance(self.array[position][1], InfiniteHashTable):
                self.array[position][1][key] = value
            else:
                new_table = InfiniteHashTable()
                new_table.level = self.level + 1
                old_key, old_value = self.array[position]
                self.array[position] = (
                    key[:new_table.level], new_table)
                self.array[position][1][key] = value
                self.array[position][1][old_key] = old_value
        else:
            self.array[position] = key, value

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        position = self.hash(key)
        if self.array[position] is not None:
            if not isinstance(self.array[position][1], InfiniteHashTable):
                self.array[position] = None
            else:
                if len(self.array[position][1]) == 2:
                    for item in self.array[position][1].array:
                        if item is not None and item[0] != key:
                            new_key, new_value = item
                            break
                    del self.array[position][1][key]
                    del self.array[position][1][new_key]
                    self[new_key] = new_value
                else:
                    del self.array[position][1][key]
        else:
            raise KeyError(key)

    def __len__(self):
        count = 0
        for item in self.array:
            if item is not None:
                if isinstance(item[1], InfiniteHashTable):
                    count += len(item[1])
                else:
                    count += 1
        return count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        result = ""
        for item in self.array:
            if item is None:
                continue
            elif isinstance(item[1], InfiniteHashTable):
                sub_table_str = str(item[1])
                sub_table_str = "\n".join(
                    ["  " + line for line in sub_table_str.split("\n")])
                result += f"{item[0]}*\n{sub_table_str}\n"
            else:
                result += f"{item[0]}: {item[1]}\n"
        return result.strip()

    def get_location(self, key):
        """
        Get the sequence of positions required to access this key.

        :raises KeyError: when the key doesn't exist.
        """
        position = self.hash(key)
        if self.array[position] is None:
            raise KeyError(key)
        if isinstance(self.array[position][1], InfiniteHashTable):
            return [position] + self.array[position][1].get_location(key)
        return [position]

    def __contains__(self, key: K) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See linear probe.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True


if __name__ == "__main__":
    ih = InfiniteHashTable()
    ih["lin"] = 1
    ih["leg"] = 2
    ih["mine"] = 3
    ih["linked"] = 4
    ih["limp"] = 5
    ih["mining"] = 6
    ih["jake"] = 7
    ih["linger"] = 8

    # del ih["limp"]
    # print(ih.get_location("linked"))
    # Should do nothing
    # self.assertEqual(ih.get_location("linked"), [4, 1, 6, 3])

    print(ih)
    del ih["mine"]
    # print(ih)
    print(ih.get_location("mining"))
    # self.assertEqual(ih.get_location("mining"), [5])
    # self.assertRaises(KeyError, lambda: ih.get_location("mine"))

    del ih["mining"]
    del ih["jake"]
    del ih["leg"]
    del ih["linger"]
    del ih["linked"]

    # self.assertEqual(ih["lin"], 1)
    # self.assertEqual(ih.get_location("lin"), [4])

    del ih["lin"]

    ih["lin"] = 10
    # self.assertEqual(ih.get_location("lin"), [4])
    # self.assertEqual(len(ih), 1)
    pass
