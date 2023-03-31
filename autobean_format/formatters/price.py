from typing import Iterator
from autobean_refactor import models
from ..internal import alignment, iterating
from . import base


@base.formatter(models.Price)
def format_price(open: models.Price, context: base.Context) -> Iterator[models.RawTokenModel]:

    children_it = iterating.BufferedIterator(open.iter_children_formatted())

    for child, indented in children_it.take_until(lambda x: isinstance(x[0], models.Date)):
        yield from base.format(child, context.with_indented(indented))

    line = base.collect(children_it.take_until_inclusive(lambda x: isinstance(x[0], models.Eol)), context)
    header = context.parser.parse(line, models.Price)
    if padding := alignment.get_padding_align_left(header.raw_amount.raw_currency, context.options.currency_column):
        header.raw_amount.spacing_before += padding
    yield from header.tokens

    for child, indented in children_it:
        yield from base.format(child, context.with_indented(indented))
