from __future__ import annotations

from typing import Generic, TypeVar, Iterator
from data_structures.hash_table import LinearProbeTable, FullError
from data_structures.referential_array import ArrayR

K1 = TypeVar('K1')
K2 = TypeVar('K2')
V = TypeVar('V')


class DoubleKeyTable(Generic[K1, K2, V]):
    """
    Double Hash Table.

    Type Arguments:
        - K1:   1st Key Type. In most cases should be string.
                Otherwise `hash1` should be overwritten.
        - K2:   2nd Key Type. In most cases should be string.
                Otherwise `hash2` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151,
                   12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes: list | None = None, internal_sizes: list | None = None) -> None:
        if sizes is not None:
            self.sizes = sizes
            self.table = LinearProbeTable(sizes)
        else:
            self.table = LinearProbeTable(self.TABLE_SIZES)
        if internal_sizes is not None:
            self.internal_sizes = internal_sizes
        else:
            self.internal_sizes = self.TABLE_SIZES
        self.count = 0

    def hash1(self, key: K1) -> int:
        """
        Hash the 1st key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """
        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: K2, sub_table: LinearProbeTable[K2, V]) -> int:
        """
        Hash the 2nd key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """
        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % sub_table.table_size
            a = a * self.HASH_BASE % (sub_table.table_size - 1)
        return value

    def _linear_probe(self, key1: K1, key2: K2, is_insert: bool) -> tuple[int, int]:
        """
        Find the correct position for this key in the hash table using linear probing.

        :raises KeyError: When the key pair is not in the table, but is_insert is False.
        :raises FullError: When a table is full and cannot be inserted.
        """
        position1 = self.hash1(key1)
        pos1, pos2 = False, False

        for _ in range(self.table.table_size):
            if self.table.array[position1] is None:
                # Empty spot. Am I upserting or retrieving?
                if is_insert:
                    self.table.array[position1] = (
                        key1, LinearProbeTable(self.internal_sizes))
                    self.table.array[position1][1].hash = lambda k: self.hash2(
                        k, self.table.array[position1][1])
                    pos1 = True
                    break
                else:
                    raise KeyError("Key 1:", key1)
            elif self.table.array[position1][0] == key1:
                pos1 = True
                break
            else:
                # Taken by something else. Time to linear probe.
                position1 = (position1 + 1) % self.table_size

        if pos1 == False:
            if is_insert:
                raise FullError("Table is full!")
            else:
                raise KeyError("Key 1", key1)

        inner_table = self.table.array[position1][1]
        position2 = self.hash2(key2, inner_table)

        for _ in range(inner_table.table_size):
            if inner_table.array[position2] is None:
                if is_insert:
                    pos2 = True
                    break
                else:
                    raise KeyError("Key 2:", key2)
            elif inner_table.array[position2][0] == key2:
                pos2 = True
                break
            else:
                position2 = (position2 + 1) % inner_table.table_size

        if pos2 == False:
            if is_insert:
                raise FullError("Table is full!")
            else:
                raise KeyError("Key 1:", key2)

        return (position1, position2)

    def iter_keys(self, key: K1 | None = None) -> Iterator[K1 | K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.
        """
        raise NotImplementedError()

    def keys(self, key: K1 | None = None) -> list[K1]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.
        """
        if key is None:
            return self.table.keys()
        else:
            return self.table[key].keys()

    def iter_values(self, key: K1 | None = None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.
        """
        raise NotImplementedError()

    def values(self, key: K1 | None = None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.
        """
        if key is None:
            values = set()
            for key in self.keys():
                for item in self.table[key].values():
                    values.add(item)
            return list(values)
        else:
            return self.table[key].values()

    def __contains__(self, key: tuple[K1, K2]) -> bool:
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

    def __getitem__(self, key: tuple[K1, K2]) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """
        position = self._linear_probe(key[0], key[1], False)
        return self.table.array[position[0]][1].array[position[1]][1]

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """
        position = self._linear_probe(key[0], key[1], True)
        inner_table = self.table.array[position[0]][1]

        if inner_table.array[position[1]] is None:
            self.count += 1
        inner_table.array[position[1]] = (key[1], data)
        if len(inner_table) > inner_table.table_size / 2:
            inner_table._rehash()

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        raise NotImplementedError()

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)
        """
        raise NotImplementedError()

    @property
    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)
        """
        return len(self.table.array)

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        """
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        raise NotImplementedError()


if __name__ == "__main__":
    dt = DoubleKeyTable()

    dt["Tim", "Jen"] = 1
    dt["Amy", "Ben"] = 2
    dt["May", "Ben"] = 3
    dt["Ivy", "Jen"] = 4
    dt["May", "Tom"] = 5
    dt["Tim", "Bob"] = 6
    dt["May", "Jim"] = 7
    dt["Het", "Liz"] = 8

    print(dt["May", "Ben"])
    print(dt["May", "Tom"])
    print(dt["May", "Jim"])
    print(dt["May", "Tom"])

    print(dt.keys("May"))

    print(dt.values())

    print(dt.values("Tim"))
