from typing import Iterator
from autobean_refactor import models
from ..internal import alignment, iterating
from . import base


@base.formatter(models.RawTokenModel)  # type: ignore[type-abstract]
def format_token(model: models.RawTokenModel, context: base.Context) -> Iterator[models.RawTokenModel]:
    yield model


@base.formatter(models.RawTreeModel)  # type: ignore[type-abstract]
def format_tree(model: models.RawTreeModel, context: base.Context) -> Iterator[models.RawTokenModel]:
    children_it = iterating.BufferedIterator(model.iter_children_formatted())

    if (getattr(model, 'raw_inline_comment', None)) is not None:
        line = base.collect(children_it.take_until_inclusive(lambda x: isinstance(x[0], models.Eol)), context)
        header = context.parser.parse(line, type(model))
        raw_inline_comment: models.InlineComment = getattr(header, 'raw_inline_comment')
        if padding := alignment.get_padding_align_left(raw_inline_comment, context.options.inline_comment_column):
            raw_inline_comment.spacing_before += padding
        yield from header.tokens

    for child, indented in children_it:
        yield from base.format(child, context.with_indented(indented))
