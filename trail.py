from __future__ import annotations
from dataclasses import dataclass

from data_structures.linked_stack import LinkedStack
from mountain import Mountain

from typing import TYPE_CHECKING, Union

# Avoid circular imports for typing.
if TYPE_CHECKING:
    from personality import WalkerPersonality


@dataclass
class TrailSplit:
    """
    A split in the trail.
       ___path_top____
      /               \
    -<                 >-path_follow-
      \__path_bottom__/
    """

    path_top: Trail
    path_bottom: Trail
    path_follow: Trail

    def remove_branch(self) -> TrailStore:
        """Removes the branch, should just leave the remaining following trail.

        The best and worst case complexity for this function is O(1)
        """
        return self.path_follow.store


@dataclass
class TrailSeries:
    """
    A mountain, followed by the rest of the trail

    --mountain--following--

    """
    mountain: Mountain
    following: Trail

    def remove_mountain(self) -> TrailStore:
        """Removes the mountain at the beginning of this series.

        The best and worst case time complexity of this function is O(1)
        """
        return self.following.store

    def add_mountain_before(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain in series before the current one.

        The best and worst case time complexity of this function is O(1)
        """
        return TrailSeries(mountain, Trail(self))

    def add_empty_branch_before(self) -> TrailStore:
        """Adds an empty branch, where the current trailstore is now the following path.

        The best and worst case time complexity of this function is O(1)
        """
        return TrailSplit(Trail(None), Trail(None), Trail(self))

    def add_mountain_after(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain after the current mountain, but before the following trail.

        The best and worst case time complexity of this function is O(1)
        """
        return TrailSeries(self.mountain, Trail(TrailSeries(mountain, self.following)))

    def add_empty_branch_after(self) -> TrailStore:
        """Adds an empty branch after the current mountain, but before the following trail.

        The best and worst case time complexity of this function is O(1)
        """
        return TrailSeries(self.mountain, Trail(TrailSplit(Trail(None), Trail(None), self.following)))


TrailStore = Union[TrailSplit, TrailSeries, None]


@dataclass
class Trail:

    store: TrailStore = None

    def add_mountain_before(self, mountain: Mountain) -> Trail:
        """Adds a mountain before everything currently in the trail.

        Best and Worst Complexity are O(1)
        """
        if self.store is None:
            return Trail(TrailSeries(mountain, Trail(None)))
        return Trail(self.store.add_mountain_before(mountain))

    def add_empty_branch_before(self) -> Trail:
        """Adds an empty branch before everything currently in the trail.

        Best and Worst Complexity are O(1)
        """
        if self.store is None:
            return Trail(TrailSplit(Trail(None), Trail(None), Trail(None)))
        return Trail(self.store.add_empty_branch_before())

    def follow_path(self, personality: WalkerPersonality) -> None:
        """Follow a path and add mountains according to a personality.

        The time complexity of follow_path really depends on the length of the
        trail, if it's empty, that's the best case and the function retunrs
        immediately, if not, it will traverse the entire trail. The worst case
        complexity in this situation is O(n)
        """
        current = self
        linked_stack = LinkedStack()

        while True:
            if current.store is None:
                if linked_stack.is_empty():
                    return
                else:
                    current = linked_stack.pop()
            else:
                if isinstance(current.store, TrailSeries):
                    personality.add_mountain(current.store.mountain)
                    current = current.store.following
                else:
                    linked_stack.push(current.store.path_follow)
                    branch = personality.select_branch(
                        current.store.path_top, current.store.path_bottom)
                    current = current.store.path_top if branch == True else current.store.path_bottom

    def collect_all_mountains(self) -> list[Mountain]:
        """
        Returns a list of all mountains on the trail.

        The complexity of this function is O(n).
        """
        raise NotImplementedError()

    # Input to this should not exceed k > 50, at most 5 branches.
    def length_k_paths(self, k) -> list[list[Mountain]]:
        """
        Returns a list of all paths of containing exactly k mountains.
        Paths are represented as lists of mountains.

        Paths are unique if they take a different branch, even if this results in the same set of mountains.
        """
        raise NotImplementedError()
