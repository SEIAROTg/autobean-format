from typing import Iterator
from autobean_refactor import models
from ..internal import alignment, iterating
from . import base


@base.formatter(models.Balance)
def format_balance(open: models.Balance, context: base.Context) -> Iterator[models.RawTokenModel]:

    children_it = iterating.BufferedIterator(open.iter_children_formatted())

    for child, indented in children_it.take_until(lambda x: isinstance(x[0], models.Date)):
        yield from base.format(child, context.with_indented(indented))

    line = base.collect(children_it.take_until_inclusive(lambda x: isinstance(x[0], models.Eol)), context)
    header = context.parser.parse(line, models.Balance)
    if padding := alignment.get_padding_align_left(header.raw_currency, context.options.currency_column):
        header.raw_account.spacing_after += padding
    if (raw_inline_comment := header.raw_inline_comment) is not None:
        if padding := alignment.get_padding_align_left(raw_inline_comment, context.options.inline_comment_column):
            raw_inline_comment.spacing_before += padding
    yield from header.tokens

    for child, indented in children_it:
        yield from base.format(child, context.with_indented(indented))
