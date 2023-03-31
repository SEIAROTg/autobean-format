from typing import Iterable, Iterator, Optional, Sequence, TypeAlias, TypeGuard, get_args
from autobean_refactor import models
from ..internal import sorting
from . import base

_TopLevelEntity: TypeAlias = models.Directive | models.BlockComment
_Block: TypeAlias = Sequence[_TopLevelEntity]
_BLANK_LINE_SURROUNDED = {
    models.BlockComment,
    models.IgnoredLine,
    models.Transaction,
}


def _get_category(model: _TopLevelEntity) -> str:
    if isinstance(model, models.Pushtag | models.Poptag | models.Pushmeta | models.Popmeta):
        return 'push_pop'
    if isinstance(model, models.Open | models.Close | models.Commodity | models.Pad | models.Balance):
        return 'declaration'
    if isinstance(model, models.Plugin | models.Include | models.Option):
        return 'directive'
    return 'other'


def _should_split(prev: Optional[_TopLevelEntity], current: _TopLevelEntity) -> bool:
    if prev is None:
        return False
    current_spacing = prev.spacing_after.count('\n')
    if current_spacing >= 2:
        return True
    if type(prev) in _BLANK_LINE_SURROUNDED or type(current) in _BLANK_LINE_SURROUNDED:
        return True
    if _get_category(prev) != _get_category(current):
        return True
    return False


def _is_directive_or_comment(model: models.RawModel) -> TypeGuard[_TopLevelEntity]:
    return isinstance(model, get_args(_TopLevelEntity))


def _partition(file: models.File, context: base.Context) -> list[_Block]:
    prev = None
    last_block = None
    blocks: list[_Block] = []
    for child, indented in file.iter_children_formatted():
        if isinstance(child, models.Whitespace | models.Newline):
            continue
        assert _is_directive_or_comment(child)
        assert not indented
        if last_block is None or _should_split(prev, child):
            last_block = [child]
            blocks.append(last_block)
        else:
            last_block.append(child)
        prev = child
    return blocks


def _render(blocks: Iterable[_Block], context: base.Context) -> Iterator[models.RawTokenModel]:
    prev = None
    for block in blocks:
        if prev:
            yield models.Newline.from_default()
        for child in block:
            yield from base.format(child, context)
            yield models.Newline.from_default()
        prev = block


@base.formatter(models.File)
def format_file(file: models.File, context: base.Context) -> Iterator[models.RawTokenModel]:
    blocks: list[_Block] = _partition(file, context)
    if context.options.sort:
        blocks = sorting.sort_blocks(blocks)
    yield from _render(blocks, context)
