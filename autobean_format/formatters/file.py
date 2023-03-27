from typing import Iterator, Optional, TypeAlias, TypeGuard, get_args
from autobean_refactor import models
from . import base

_DirectiveOrComment: TypeAlias = models.Directive | models.BlockComment
_BLANK_LINE_SURROUNDED = {
    models.BlockComment,
    models.IgnoredLine,
    models.Transaction,
}


def _get_category(model: _DirectiveOrComment) -> str:
    if isinstance(model, models.Pushtag | models.Poptag | models.Pushmeta | models.Popmeta):
        return 'push_pop'
    if isinstance(model, models.Open | models.Close | models.Commodity):
        return 'open_close'
    if isinstance(model, models.Plugin | models.Include | models.Option):
        return 'directive'
    if isinstance(model, models.Pad | models.Balance):
        return 'balance'
    return 'other'


def _get_spacing(prev: Optional[_DirectiveOrComment], next: _DirectiveOrComment) -> str:
    if prev is None:
        return ''
    
    current_spacing = prev.spacing_after.count('\n')
    if current_spacing >= 2:
        # If multiple blank lines are needed, maybe there should be a block comment.
        return '\n\n'
    if type(prev) in _BLANK_LINE_SURROUNDED or type(next) in _BLANK_LINE_SURROUNDED:
        return '\n\n'
    if _get_category(prev) != _get_category(next):
        return '\n\n'
    return '\n'    


def _is_directive_or_comment(model: models.RawModel) -> TypeGuard[_DirectiveOrComment]:
    return isinstance(model, get_args(_DirectiveOrComment))


@base.formatter(models.File)
def format_file(file: models.File, context: base.Context) -> Iterator[models.RawTokenModel]:
    prev = None    
    for child, indented in file.iter_children_formatted():
        if isinstance(child, models.Whitespace | models.Newline):
            continue
        assert _is_directive_or_comment(child)
        yield models.Whitespace.from_raw_text(_get_spacing(prev, child))
        yield from base.format(child, context.with_indented(indented))
        prev = child
    if prev is not None:
        yield models.Newline.from_default()
