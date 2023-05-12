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

        The best case complexity is actually O(1) if the key is already in the table and
        we follow a flow through the linear probe function that will return a value right
        after checking this. An example is if we're trying to insert a value but it's already
        in the table. The worst case complexity is O(n) where n is table_size, this occurs when perhaps
        the table is relatively full and we have to search for an empty address during an insertion
        operation. Since a search for a free address could take close to n number of searches,
        the worst case complexity is O(n) where n is the table_size.  
        """
        position1 = self.hash1(key1)
        for i in range(self.table_size):
            if self.array[position1] is None:
                if is_insert:
                    self.array[position1] = (
                        key1, LinearProbeTable(self.internal_sizes))
                    self.array[position1][1].hash = lambda k: self.hash2(
                        k, self.array[position1][1])
                    self.table_count += 1
                    return (position1, self.array[position1][1]._linear_probe(key2, is_insert))
                else:
                    raise KeyError(key1)
            elif self.array[position1][0] == key1:
                return (position1, self.array[position1][1]._linear_probe(key2, is_insert))
            position1 = (position1 + 1) % self.table_size
        raise FullError("Table is full!")

    def iter_keys(self, key: K1 | None = None) -> Iterator[K1 | K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.

        The best case complexity is when the hash table is empty O(1),
        otherwise, it will be O(n) where n is the length of the table.
        """
        if key is not None:
            inner_table = self.get_inner_table(key)
            yield from inner_table.keys()
        else:
            for item in self.array:
                if item is not None:
                    yield item[0]

    def keys(self, key: K1 | None = None) -> list[K1]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.

        The best case complexity is when the hash table is empty O(1),
        otherwise, it will be O(n) where n is the length of the table.
        """
        if key is None:
            return [item[0] for item in self.array if item is not None]

        for item in self.array:
            if item is not None and item[0] == key:
                return item[1].keys()

    def iter_values(self, key: K1 | None = None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.

        The best case complexity is when the hash table is empty O(1),
        otherwise, it will be O(n) where n is the length of the table.
        """
        if key is not None:
            for item in self.array:
                if item and item[0] == key:
                    yield from (pair[1] for pair in item[1].array if pair)
        else:
            for item in self.array:
                if item:
                    yield from (pair[1] for pair in item[1].array if pair)

    def values(self, key: K1 | None = None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.

        The best case complexity is when the hash table is empty O(1),
        otherwise, it will be O(n) where n is the length of the table.
        """
        if key is None:
            return [value for item in self.array if item is not None for value in item[1].values()]
        else:
            for item in self.array:
                if item is not None and item[0] == key:
                    return item[1].values()
            return []

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

        The worst complexity can be O(n) (see linear probe) with respect to the
        size of the table (if probe chain is close to table size for example). Best
        case is O(1) if item is attained straight away at location it's key maps to.
        """
        positions = self._linear_probe(key[0], key[1], False)
        return self.array[positions[0]][1].array[positions[1]][1]

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.

        Just like getitem magic method. The best case complexity for
        set item is O(n), since we might have to search through the entire
        array because of a long probe chain close to the size of the array.
        Otherwise, O(1) is the best case time complexity when key maps without collision.
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

        Best case complexity is O(1) if we can delete an item and not
        have to worry about rehashing anythign. Otherwise, the
        worst case time complexity is O(n), since in the worst case, we
        might have to rehash everything in the table.
        """
        positions = self._linear_probe(key[0], key[1], False)
        # Remove the element
        del self.array[positions[0]][1][key[1]]
        self.count -= 1

        if self.array[positions[0]][1].is_empty():
            self.table_count -= 1
            self.array[positions[0]] = None
            position = (positions[0] + 1) % self.table_size
            while self.array[position]:
                key2, value = self.array[position]
                self.array[position] = None
                # I know its a rough solution but couldn't figure out a compact way to do it otherwise
                newpos = self._linear_probe(key2, key[1], True)
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

        Best and worst case time complexity is O(n) where n is the size of the array.
        """
        items = []
        for i in range(len(self.array)):
            if self.array[i] is None:
                items.append(" -- EMPTY -- \n")
            else:
                items.append(f"{i} ~ {self.array[i][0]}: {self.array[i][1]}")

        return "START\n" + "".join(items) + "END"
