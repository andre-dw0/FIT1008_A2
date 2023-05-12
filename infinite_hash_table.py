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
            if self.array[position].isinstance(InfiniteHashTable):
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
                self.array[position] = (key[new_table.level-1], new_table)
                self.array[position][1][key] = (key, value)
                self.array[position][1][old_key] = (old_key, old_value)
        else:
            self.array[position] = (key, value)

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        position = self.hash(key)
        if self.array[position] is not None:
            if isinstance(self.array[position][1], InfiniteHashTable):
                del self.array[position][1][key]
            else:
                del self.array[position]
                if len(self.array) == 0:
                    del self
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
        return str(self.table)

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
