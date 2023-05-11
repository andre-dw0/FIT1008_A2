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
        # For use later such as efficiently calculating number of elements in hash table.
        self.count = 0
        self.table_count = 0
        self.size_index = 0
        self.sizes = sizes if sizes is not None else self.TABLE_SIZES
        self.internal_sizes = internal_sizes if internal_sizes is not None else self.TABLE_SIZES
        self.array = ArrayR(self.sizes[self.size_index])

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

        flag = False
        for _ in range(self.table_size):
            if self.array[position1] is None:
                if is_insert:
                    self.array[position1] = (
                        key1, LinearProbeTable(self.internal_sizes))
                    self.array[position1][1].hash = lambda k: self.hash2(
                        k, self.array[position1][1])
                    self.table_count += 1
                    flag = True
                    break
                else:
                    raise KeyError(key1)
            elif self.array[position1][0] == key1:
                flag = True
                break
            else:
                position1 = (position1 + 1) % self.table_size
        if flag == False:
            raise FullError("Table is full!")

        inner_table = self.array[position1][1]
        return (position1, inner_table._linear_probe(key2, is_insert))

    def iter_keys(self, key: K1 | None = None) -> Iterator[K1 | K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.
        """
        if key is not None:
            for item in self.array:
                if item is not None and item[0] == key:
                    for pair in item[0].array:
                        yield pair[0]
        else:
            for item in self.array:
                if item is not None:
                    yield item[0]

    def keys(self, key: K1 | None = None) -> list[K1]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.
        """
        if key is None:
            return [item[0] for item in self.array if item is not None]
        else:
            for i in range(len(self.array)):
                if self.array[i] is not None and self.array[i][0] == key:
                    return self.array[i][1].keys()

    def iter_values(self, key: K1 | None = None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.
        """
        if key is not None:
            for item in self.array:
                if item is not None:
                    if item[0] == key:
                        for pair in item[1].array:
                            if pair is not None:
                                yield pair[1]
        else:
            for item in self.array:
                if item is not None:
                    for pair in item[1].array:
                        if pair is not None:
                            yield pair[1]

    def values(self, key: K1 | None = None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.
        """
        if key is None:
            values = []
            for i in range(self.table_size):
                if self.array[i] is not None:
                    for value in self.array[i][1].values():
                        values.append(value)
            return values
        else:
            for i in range(self.table_size):
                if self.array[i] is not None:
                    if self.array[i][0] == key:
                        return self.array[i][1].values()

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
        positions = self._linear_probe(key[0], key[1], False)
        return self.array[positions[0]][1].array[positions[1]][1]

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """
        positions = self._linear_probe(key[0], key[1], True)
        inner_table = self.array[positions[0]][1]
        if inner_table.array[positions[1]] is None:
            self.count += 1

        inner_table[key[1]] = data
        inner_table.hash = lambda k: self.hash2(k, inner_table)
        if self.table_count > self.table_size / 2:
            self._rehash()

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        positions = self._linear_probe(key[0], key[1], False)
        # Remove the element
        del self.array[positions[0]][1][key[1]]
        self.count -= 1

        if self.array[positions[0]][1].is_empty():
            self.array[positions[0]] = None
            self.table_count -= 1
            # Start moving over the cluster
            position = (positions[0] + 1) % self.table_size
            while self.array[position] is not None:
                key2, value = self.array[position]
                self.array[position] = None
                newpos = self._linear_probe(key2, 'sd', True)
                self.array[newpos[0]] = (key2, value)
                position = (position + 1) % self.table_size

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)
        """
        old_array = self.array
        self.size_index += 1
        self.array = ArrayR(self.sizes[self.size_index])
        self.count = 0
        for item in old_array:
            if item is not None:
                key, value = item
                self.array[self.hash1(key)] = (key, value)

    @property
    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)
        """
        return len(self.array)

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
    dt["May", "Jim"] = 1
    dt["Kim", "Tim"] = 2

    key_iterator = dt.iter_keys()
    value_iterator = dt.iter_values()

    key = next(key_iterator)
    print(key)
    # self.assertIn(key, ["May", "Kim"])
    value = next(value_iterator)
    print(value)
    # self.assertIn(value, [1, 2])

    del dt["May", "Jim"]
    del dt["Kim", "Tim"]

    key2 = next(key_iterator)
    print(key2)

    # Retrieving the next value should either raise StopIteration or crash entirely.
    # Note: Deleting from an element being iterated over is bad practice
    # We just want to make sure you aren't returning a list and are doing this
    # with an iterator.
    # self.assertRaises(BaseException, lambda: next(key_iterator))
    # self.assertRaises(BaseException, lambda: next(value_iterator))
    pass
