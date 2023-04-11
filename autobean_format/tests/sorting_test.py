import datetime
import decimal
from typing import Optional, Sequence, TypeAlias, cast, get_args
from autobean_refactor import models
import pytest
from ..internal import sorting
from . import base

_Entry: TypeAlias = models.Balance | models.Close | models.Commodity | models.Pad | models.Event | models.Query | models.Price | models.Note | models.Document | models.Custom | models.Transaction
_TopLevelEntity: TypeAlias = models.Directive | models.BlockComment
_TestBlock: TypeAlias = list[str] | list[_TopLevelEntity]
_PLUGIN = models.Plugin.from_value(name='test')
_INCLUDE = models.Include.from_value(filename='test')
_PUSHTAG = models.Pushtag.from_value(tag='test')


def build_dated_entry(entry: str) -> _TopLevelEntity:
    parts = entry.split(' ', maxsplit=1)
    date = datetime.datetime.strptime(parts[0], '%Y-%m-%d').date()
    meta: dict[str, str | decimal.Decimal]
    if len(parts) == 2:
        meta = dict(time=parts[1] if ':' in parts[1] else decimal.Decimal(parts[1]))
    else:
        meta = {}
    return models.Custom.from_value(date=date, type='test', values=(), meta=meta)


def unbuild_entity(entity: _TopLevelEntity) -> str | _TopLevelEntity:
    if not isinstance(entity, get_args(_Entry)):
        return entity
    entry: _Entry = cast(_Entry, entity)
    time = entry.meta.get('time')
    if time is None:
        return str(entry.date)
    return f'{entry.date} {time}'


def build_block(block: _TestBlock) -> list[_TopLevelEntity]:
    if not block:
        return []
    if not isinstance(block[0], str):
        return cast(list[_TopLevelEntity], block)
    return [build_dated_entry(entry) for entry in cast(list[str], block)]


def build_blocks(blocks: list[_TestBlock]) -> list[list[_TopLevelEntity]]:
    return [build_block(block) for block in blocks]


# For better test output
def unbuild_blocks(
        blocks: list[Sequence[models.Directive | models.BlockComment]]
) -> list[list[str | _TopLevelEntity]]:
    return [[unbuild_entity(entity) for entity in block] for block in blocks]


class TestSorting(base.BaseTest):

    @pytest.mark.parametrize('blocks,sorted_blocks', [
        pytest.param([], None, id='empty'),
        pytest.param([['2000-01-01']], None, id='single'),
        pytest.param([[_PLUGIN, _INCLUDE]], None, id='undated'),
        pytest.param([['2000-01-01', '2000-01-01', '2000-01-02', '2000-01-03']], None, id='sorted'),
        pytest.param(
            [['2000-01-01', '2000-01-02 01:00', '2000-01-02 02:00', '2000-01-02 03:00', '2000-01-03']],
            None,
            id='sorted with time'),
        pytest.param(
            [['2000-01-01', '2000-01-02 01:00', '2000-01-02', '2000-01-02 02:00', '2000-01-02',
              '2000-01-02 02:00', '2000-01-03']],
            None,
            id='sorted with optional time'),
        pytest.param(
            [['2000-01-01', '2000-01-02 01:00', '2000-01-02', '2000-01-02 02:00', '2000-01-02',
              '2000-01-02 01:01', '2000-01-03']],
            [['2000-01-01', '2000-01-02 01:00', '2000-01-02', '2000-01-02 01:01', '2000-01-02 02:00',
              '2000-01-02', '2000-01-03']],
            id='reorder one'),
        pytest.param(
            [['2000-01-05', '2000-01-04', '2000-01-03', '2000-01-02', '2000-01-01']],
            [['2000-01-01', '2000-01-02', '2000-01-03', '2000-01-04', '2000-01-05']],
            id='reversed',
        ),
        pytest.param(
            [['2000-01-02', '2000-01-03'], ['2000-01-01', '2000-01-02 01:00']],
            [['2000-01-01', '2000-01-02 01:00'], ['2000-01-02', '2000-01-03']],
            id='reorder whole block',
        ),
        pytest.param(
            [['2000-02-02', '2000-02-01'], [_PUSHTAG], ['2000-01-02', '2000-01-01']],
            [['2000-02-01', '2000-02-02'], [_PUSHTAG], ['2000-01-01', '2000-01-02']],
            id='no cross compartment',
        ),
        pytest.param(
            [['2000-01-04'], ['2000-01-02'], [_INCLUDE], ['2000-01-03'], ['2000-01-01']],
            [['2000-01-01'], ['2000-01-02'], [_INCLUDE], ['2000-01-03'], ['2000-01-04']],
            id='retain undated directives'
        ),
        pytest.param(
            [['2000-01-01', '2000-01-01', '2000-01-03', '2000-01-05'], ['2000-01-02', '2000-01-04', '2000-01-04', '2000-01-06', '2000-01-07']],
            [['2000-01-01', '2000-01-01'], ['2000-01-02'], ['2000-01-03'], ['2000-01-04', '2000-01-04'], ['2000-01-05'], ['2000-01-06', '2000-01-07']],
            id='split blocks',
        ),
        pytest.param(
            [['2000-01-02', '2000-01-01'], ['2000-01-03', '2000-01-02']],
            [['2000-01-01', '2000-01-02'], ['2000-01-02', '2000-01-03']],
            id='keep blocks',
        ),
        pytest.param(
            [['2000-01-01', '2000-01-01 02:00', '2000-01-01', '2000-01-01 08:00', '2000-01-01', '2000-01-01 04:00', '2000-01-01']],
            [['2000-01-01', '2000-01-01 02:00', '2000-01-01', '2000-01-01 04:00', '2000-01-01 08:00', '2000-01-01', '2000-01-01']],
            id='reorder with optional time',
        ),
        pytest.param(
            [['2000-01-01 08:00', '2000-01-01 07:00:00', '2000-01-01 946706400', '2000-01-01 946702800000', '2000-01-01 946699200000000']],
            [['2000-01-01 946699200000000', '2000-01-01 946702800000', '2000-01-01 946706400', '2000-01-01 07:00:00', '2000-01-01 08:00']],
            id='distinct time units',
        ),
        pytest.param(
            [['2000-01-02'], ['2000-01-02'], ['2000-01-01'], ['2000-01-01']],
            [['2000-01-01'], ['2000-01-01'], ['2000-01-02'], ['2000-01-02']],
            id='same sort key',
        ),
    ])
    def test_sort_blocks(self, blocks: list[_TestBlock], sorted_blocks: Optional[list[_TestBlock]]) -> None:
        if sorted_blocks is None:
            sorted_blocks = blocks
        assert unbuild_blocks(sorting.sort_blocks(build_blocks(blocks))) == sorted_blocks
