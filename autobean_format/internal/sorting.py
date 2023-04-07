"""Sorts entities in a less disruptive way.

## Problems

Sorting beancount entities may sound as simple as `sorted(entities)` but doing it properly isn't trivial.

* Establishing total order may not be possible.
  * There may be undated entities (e.g. `include`)
  * Ideally we also sort by time if specified in meta. But they may not be consistently specified.
* Swapping entries inside and outside a pushtag / pushmeta block is not allowed.
* Ideally we would like to reorder as few entities as possible.
* Ideally we would like to keep the original block structure.

## Solution

In order to not disrupt existing formatting, we make the assumption that the majority of the file is already sorted
and only a few entities need to be reordered. This assumption may not be true for all files, but when it isn't, we
really don't know how to best preserve the existing formatting.

The sorting process is:

1. Partition the file into blocks based on surrounding blank lines and entities types (pushpop / undated / dated).
  1. For each dated block, sort entities with prudent sort.
1. Partition the blocks into compartments of blocks, split by pushpop blocks.
1. For each compartment:
  1. Sort blocks with prudent sort.

The prudent sort process is:

1. Identify the longest non-decreasing subsequence of entities and split out the rest.
1. Sort the rest with simple sort by dicating a total order.
1. Merge the sorted rest into the non-decreasing subsequence.
  * When merging blocks, this may involve split some blocks when necessary.

## Alternatives

Instead of sorting each compartment separately, we could allow swapping entities before `pushtag #foo` and after
`poptag #foo`, but we don't do it as it may be over-complexing due to possibly interleaving pushes.

Instead of sorting out-of-order entities with simple sort, we could recurse with the same method, but we don't do it
as it may be over-complexing and degraded performance.
"""

import abc
import decimal
import functools
import heapq
import itertools
from typing import TYPE_CHECKING, Any, Generic, Iterable, Iterator, Optional, Self, Sequence, TypeAlias, TypeVar, cast, get_args

from autobean_refactor import models
from . import chrono
if TYPE_CHECKING:
    from _typeshed import SupportsDunderLT, SupportsDunderGT

_T = TypeVar('_T')
_O = TypeVar('_O', bound='_Ordered')
_Entry: TypeAlias = models.Balance | models.Close | models.Commodity | models.Pad | models.Event | models.Query | models.Price | models.Note | models.Document | models.Custom | models.Transaction
_CompartmentSplitter: TypeAlias = models.Pushtag | models.Poptag | models.Pushmeta | models.Popmeta | models.BlockComment
_TopLevelEntitiy = models.Directive | models.BlockComment


class _Ordered(Generic[_T], abc.ABC):

    def __init__(self, value: _T) -> None:
        self.value = value

    # Note: a.more_successor_permissive_than(b) may not imply !(b.can_go_before(a))
    @abc.abstractmethod
    def more_successor_permissive_than(self, other: Self) -> bool:
        """Tests if successors permitted by this entity forms a proper superset of those permitted by the other entity."""

    # Note: may not be transitive
    @abc.abstractmethod
    def can_go_before(self, other: Self) -> bool:
        """Tests if this entity can go before the other entity."""

    @classmethod
    @abc.abstractmethod
    def min(cls, a: Self, b: Self) -> Self:
        """An associative function to summarize the lower bound for can_go_before.
        
        Formally:
        forall x: x.can_go_before(a) && x.can_go_before(b) <=> x.can_go_before(min(a, b))
        """

    @classmethod
    @abc.abstractmethod
    def max(cls, a: Self, b: Self) -> Self:
        """An associative function to summarize the upper bound for can_go_before.

        Formally:
        forall x: a.can_go_before(x) && b.can_go_before(x) <=> max(a, b).can_go_before(x)
        """

    @classmethod
    @abc.abstractmethod
    def merge(cls, sorted: list[Self], unsorted: list[Self]) -> Iterable[Self]:
        """Merges a sorted list with an unsorted list into a sorted list.

        The original order of `sorted` must be preserved.
        """

    @classmethod
    def sort(cls, values: list[Self]) -> list[Self]:
        if _is_ordered(values):
            return values
        sorted, unsorted = _split_sorted_unsorted(values)
        return list(cls.merge(sorted, unsorted))


def _is_ordered(entities: Sequence[_Ordered[_T]]) -> bool:
    if not entities:
        return True
    it = iter(entities)
    running_max = next(it)
    for entity in it:
        if not running_max.can_go_before(entity):
            return False
        running_max = running_max.max(running_max, entity)
    return True


def _split_sorted_unsorted(
    entities: Sequence[_O],
) -> tuple[list[_O], list[_O]]:

    # (length, running_max, prev)
    l = [(1, entity, -1) for entity in entities]
    sorted, unsorted = [], []
    max_len, last = 0, -1
    for i in range(len(entities)):
        for j in range(i):
            length, running_max, _ = l[j]
            if not running_max.can_go_before(entities[i]) or length + 1 < l[i][0]:
                continue
            running_max = running_max.max(running_max, entities[i])
            if length + 1 > l[i][0] or running_max.more_successor_permissive_than(l[i][1]):
                l[i] = (length + 1, running_max, j)
        if l[i][0] > max_len:
            max_len = l[i][0]
            last = i
    unsorted.append(entities[last+1:])
    while last >= 0:
        sorted.append(entities[last])
        prev = l[last][2]
        unsorted.append(entities[prev + 1:last])
        last = prev
    sorted.reverse()
    return sorted, list(itertools.chain.from_iterable(reversed(unsorted)))


def _get_entry_time(entry: _Entry) -> int | None:
    time = entry.meta.get('time')
    if isinstance(time, str):
        return chrono.try_normalize_timestring(entry.date, time)
    elif isinstance(time, decimal.Decimal):
        return chrono.try_normalize_timestamp(time)
    else:
        return None


def _build_reversed_running_min(entities: Sequence[_O]) -> list[_O]:
    reversed_running_min = list(entities)
    for i in reversed(range(len(reversed_running_min) - 1)):
        reversed_running_min[i] = reversed_running_min[i].min(
            reversed_running_min[i], reversed_running_min[i + 1])
    return reversed_running_min


def _merge_entries(sorted: Sequence['_OrderedEntry'], unsorted: Sequence['_OrderedEntry']) -> Iterator[Sequence['_OrderedEntry']]:
    cursor_sorted, cursor_unsorted = 0, 0
    reversed_running_min_unsorted = _build_reversed_running_min(unsorted)
    while cursor_sorted < len(sorted) and cursor_unsorted < len(unsorted):
        prev_cursor_sorted = cursor_sorted
        while cursor_sorted < len(sorted) and sorted[cursor_sorted].can_go_before(reversed_running_min_unsorted[cursor_unsorted]):
            cursor_sorted += 1
        if cursor_sorted > prev_cursor_sorted:
            yield sorted[prev_cursor_sorted:cursor_sorted]
        if cursor_sorted == len(sorted):
            break
        prev_cursor_unsorted = cursor_unsorted
        while cursor_unsorted < len(unsorted) and not sorted[cursor_sorted].can_go_before(reversed_running_min_unsorted[cursor_unsorted]):
            cursor_unsorted += 1
        yield unsorted[prev_cursor_unsorted:cursor_unsorted]
    if cursor_sorted < len(sorted):
        yield sorted[cursor_sorted:]
    if cursor_unsorted < len(unsorted):
        yield unsorted[cursor_unsorted:]


class _OrderedEntry(_Ordered[_Entry]):

    def __init__(self, entry: _Entry) -> None:
        super().__init__(entry)
        self.date = entry.date
        self.time = _get_entry_time(entry)

    def more_successor_permissive_than(self, other: Self) -> bool:
        return self.date < other.date or (self.date == other.date and (
            self.time is None and other.time is not None or
            self.time is not None and other.time is not None and self.time < other.time))

    def can_go_before(self, other: Self) -> bool:
        return self.date < other.date or (self.date == other.date and (
            self.time is None or other.time is None or self.time <= other.time))

    @classmethod
    def min(cls, a: Self, b: Self) -> Self:
        if a.date < b.date or (a.date == b.date and (
                b.time is None or (a.time is not None and a.time < b.time))):
            return a
        return b

    @classmethod
    def max(cls, a: Self, b: Self) -> Self:
        if a.date < b.date or (a.date == b.date and (
                a.time is None or (b.time is not None and a.time < b.time))):
            return b
        return a

    def simple_sort_key(self) -> Any:
        return (self.date, self.time or 0)

    @classmethod
    def merge(cls, sorted: list['_OrderedEntry'], unsorted: list['_OrderedEntry']) -> Iterator['_OrderedEntry']:
        unsorted.sort(key=lambda x: x.simple_sort_key())
        return itertools.chain.from_iterable(_merge_entries(sorted, unsorted))


_Block = Sequence[_OrderedEntry] | Sequence[_TopLevelEntitiy]


class _OrderedBlock(_Ordered[_Block]):

    def __init__(self, block: _Block) -> None:
        super().__init__(block)
        self.entries = cast(Sequence[_OrderedEntry], block) if isinstance(block[0], _OrderedEntry) else None

    @classmethod
    def from_raw_block(cls, block: Sequence[_TopLevelEntitiy]) -> Self:
        if isinstance(block[0], get_args(_Entry)):
            return cls(_OrderedEntry.sort([
                _OrderedEntry(entry) for entry in cast(list[_Entry], block)]))
        else:
            return cls(block)

    @functools.cached_property
    def _max(self) -> Optional['_OrderedEntry']:
        if not self.entries:
            return None
        return functools.reduce(_OrderedEntry.max, self.entries)

    @functools.cached_property
    def _min(self) -> Optional['_OrderedEntry']:
        if not self.entries:
            return None
        return functools.reduce(_OrderedEntry.min, self.entries)

    @classmethod
    def min(cls, a: Self, b: Self) -> Self:
        if (not b._min or (a._min and _OrderedEntry.min(a._min, b._min) is a._min)):
            return a
        return b

    @classmethod
    def max(cls, a: Self, b: Self) -> Self:
        if (not a._max or (b._max and _OrderedEntry.max(a._max, b._max) is b._max)):
            return b
        return a

    def more_successor_permissive_than(self, other: Self) -> bool:
        return bool(
            not self._max and other._max or  # undated is more permissive than dated
            self._max and other._max and self._max.more_successor_permissive_than(other._max)
        )

    def can_go_before(self, other: Self) -> bool:
        return bool(not self._max or not other._min or self._max.can_go_before(other._min))

    def simple_sort_key(self) -> Any:
        assert self._min and self._max  # undated blocks must be part of sorted
        return (self._min.simple_sort_key(), self._max.simple_sort_key())

    @classmethod
    def merge(cls, sorted: list['_OrderedBlock'], unsorted: list['_OrderedBlock']) -> Iterator['_OrderedBlock']:
        keyed_unsorted = [(block.simple_sort_key(), block) for block in unsorted]
        heapq.heapify(keyed_unsorted)
        cursor_sorted = 0
        while cursor_sorted < len(sorted) and keyed_unsorted:
            if sorted[cursor_sorted].can_go_before(keyed_unsorted[0][1]):
                yield sorted[cursor_sorted]
                cursor_sorted += 1
            elif keyed_unsorted[0][1].can_go_before(sorted[cursor_sorted]):
                yield heapq.heappop(keyed_unsorted)[1]
            else:
                sorted_head_entries = sorted[cursor_sorted].entries
                cursor_sorted += 1
                unsorted_head_entries = heapq.heappop(keyed_unsorted)[1].entries
                assert sorted_head_entries is not None
                assert unsorted_head_entries is not None
                split_blocks = _merge_entries(sorted_head_entries, unsorted_head_entries)
                for block in split_blocks:
                    ordered_block = _OrderedBlock(block)
                    heapq.heappush(keyed_unsorted, (ordered_block.simple_sort_key(), ordered_block))
        if cursor_sorted < len(sorted):
            yield from sorted[cursor_sorted:]
        while keyed_unsorted:
            yield heapq.heappop(keyed_unsorted)[1]


def _sort_compartment(blocks: list[_OrderedBlock]) -> list[Sequence[_TopLevelEntitiy]]:
    blocks = _OrderedBlock.sort(blocks)

    sorted_blocks = list[Sequence[_TopLevelEntitiy]]()
    for ordered_block in blocks:
        if ordered_block.entries is not None:
            sorted_blocks.append([entry.value for entry in ordered_block.entries])
        else:
            sorted_blocks.append(cast(Sequence[_TopLevelEntitiy], ordered_block.value))
    return sorted_blocks


def sort_blocks(blocks: Iterable[Sequence[_TopLevelEntitiy]]) -> list[Sequence[_TopLevelEntitiy]]:
    results = []
    compartment = list[_OrderedBlock]()
    for block in blocks:
        if isinstance(block[0], get_args(_CompartmentSplitter)):
            results.extend(_sort_compartment(compartment))
            compartment.clear()
            results.append(block)
        else:
            compartment.append(_OrderedBlock.from_raw_block(block))
    if compartment:
        results.extend(_sort_compartment(compartment))
    return results
