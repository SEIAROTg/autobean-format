from typing import Callable, Iterable, Iterator, Optional, TypeVar
from autobean_refactor import models

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

    def peek(self) -> Optional[_V]:
        if not self._buffer:
            try:
                self._push(next(self._iterator))
            except StopIteration:
                return None
        return self._buffer[0]

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


def get_padding_align_left(model: models.RawModel, column: int) -> Optional[str]:
    assert model.token_store
    length = column - model.token_store.get_position(model.first_token).column
    if length <= 0:
        return None
    return ' ' * length


def get_padding_align_right(model: models.RawModel, column: int) -> Optional[str]:
    assert model.token_store
    next_token = model.token_store.get_next(model.last_token)
    assert next_token
    length = column - model.token_store.get_position(next_token).column
    if length <= 0:
        return None
    return ' ' * length
