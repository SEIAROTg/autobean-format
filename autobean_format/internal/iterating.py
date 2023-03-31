from typing import Callable, Iterable, Iterator, Optional, TypeVar

_V = TypeVar('_V')


class BufferedIterator(Iterator[_V]):
    def __init__(self, iterable: Iterable[_V]) -> None:
        self._iterator = iter(iterable)
        self._buffer = list[_V]()

    def __iter__(self) -> Iterator[_V]:
        return self

    def __next__(self) -> _V:
        if self._buffer:
            return self._buffer.pop(0)
        return next(self._iterator)

    def _push(self, item: _V) -> None:
        self._buffer.append(item)

    def take_until(self, predicate: Callable[[_V], bool]) -> Iterator[_V]:
        for item in self:
            if predicate(item):
                self._push(item)
                return
            yield item

    def take_until_inclusive(self, predicate: Callable[[_V], bool]) -> Iterator[_V]:
        for item in self:
            yield item
            if predicate(item):
                return
