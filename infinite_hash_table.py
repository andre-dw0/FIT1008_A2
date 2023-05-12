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
                if self.array[position][0] == key:
                    return self.array[position][1]
                else:
                    raise KeyError(key)

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
                del self.array[position][1][key]
                if len(self.array[position][1]) == 1:
                    for item in self.array[position][1].array:
                        if item is not None and item[0] != key:
                            new_key, new_value = item
                            break
                    self.array[position] = None
                    self[new_key] = new_value
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
        positions = []
        position = self.hash(key)
        current = self.array[position]

        while current is not None:
            if isinstance(current[1], InfiniteHashTable):
                positions.append(position)
                position = current[1].hash(key)
                current = current[1].array[position]
            elif current[0] == key:
                positions.append(position)
                return positions
            else:
                raise KeyError(key)
        raise KeyError(key)

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
