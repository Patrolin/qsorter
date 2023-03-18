from random import shuffle
from typing import Callable, NamedTuple, TypeVar, cast
from common import *

T = TypeVar("T")
S = TypeVar("S", int, str)
SortMappingTuple = tuple[int, ...]

class Node(NamedTuple):
    direction: int
    sort_mapping: SortMappingTuple

    #def __repr__(self):
    #    return f"Node<{self.direction}>"

    # isSorted
    def isSorted(self):
        return self.sumOffsets() == 0

    def sumOffsets(self) -> int:
        return sum(abs(i - v) for i, v in enumerate(self.sort_mapping))

    # drag and drop
    def dad(self, current_i: int, desired_i: int) -> SortMappingTuple:
        acc = list(self.sort_mapping)
        v = acc.pop(current_i)
        acc.insert(desired_i, v)
        return tuple(acc)

    # diff
    def getCurrentIndex(self, desired_i: int) -> int:
        return self.sort_mapping.index(desired_i)

    def _insert(self, direction: int):
        order = range(len(self.sort_mapping)) if direction == 0 else range(len(self.sort_mapping) - 1, -1, -1)
        for desired_i in order:
            current_i = self.getCurrentIndex(desired_i)
            if current_i != desired_i:
                return (current_i, desired_i)

    def insert(self, direction: int):
        found = self._insert(direction)
        if found:
            current_i, desired_i = found
            return Node(direction, self.dad(current_i, desired_i))

    def sortNeighbor(self):
        first = self.insert(0)
        last = self.insert(1)
        if first and last:
            return first if first.sumOffsets() <= last.sumOffsets() else last
        if first: return first
        if last: return last

Diff = list[tuple[int, int, int]]

def makeYtSortDiff(items: list[T], key: Callable[[T], S]) -> Diff:
    start = makeSortMapping(items, key)
    path = [Node(-1, start)]
    while not path[-1].isSorted():
        neighbor = path[-1].sortNeighbor()
        if neighbor == None: break
        path.append(neighbor)
    diff: Diff = []
    for j in range(0, len(path) - 1):
        step = path[j]
        next_step = path[j + 1]
        current_i, desired_i = cast(tuple, step._insert(next_step.direction))
        i = path[0].getCurrentIndex(desired_i)
        diff.append((i, current_i, desired_i))
    return diff

def isVideoPrivate(item) -> bool:
    return getOrNone(item, "status.privacyStatus") in ["privacyStatusUnspecified", "private"]

def makeSortMapping(items: list[T], key: Callable[[T], S]) -> SortMappingTuple:
    items_with_index = [(v, i) for i, v in enumerate(items)]
    sorted_items_with_index = sorted(items_with_index, key=lambda vi: key(vi[0]))
    sort_mapping = [0] * len(items)
    for desired_i, vi in enumerate(sorted_items_with_index):
        sort_mapping[vi[1]] = desired_i
    return tuple(sort_mapping)

if __name__ == "__main__":
    n1 = 125
    n2 = 250
    items1 = [i for i in range(n1)]
    items2 = [i for i in range(n1, n2)]
    shuffle(items2)
    items = [*items2, *items1]
    diff = makeYtSortDiff(items, lambda v: v)
    print("diff", len(diff))
    print(diff)
