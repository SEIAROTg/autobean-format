from typing import Iterator
from autobean_refactor import models
from ..internal import alignment, iterating
from . import base


@base.formatter(models.Posting)
def format_posting(posting: models.Posting, context: base.Context) -> Iterator[models.RawTokenModel]:

    children_it = iterating.BufferedIterator(posting.iter_children_formatted())

    for child, indented in children_it.take_until(lambda x: isinstance(x[0], models.Indent)):
        yield from base.format(child, context.with_indented(indented))

    line = base.collect(children_it.take_until_inclusive(lambda x: isinstance(x[0], models.Eol)), context)
    header = context.parser.parse(line, models.Posting)
    if header.raw_currency:
        if padding := alignment.get_padding_align_left(header.raw_currency, context.options.currency_column):
            header.raw_account.spacing_after += padding
    elif header.raw_number:
        if padding := alignment.get_padding_align_right(header.raw_number, context.options.currency_column - 1):
            header.raw_account.spacing_after += padding
    if header.raw_cost:
        if padding := alignment.get_padding_align_left(header.raw_cost, context.options.cost_column):
            header.raw_cost.spacing_before += padding
    elif header.raw_price:
        if padding := alignment.get_padding_align_left(header.raw_price, context.options.cost_column):
            header.raw_price.spacing_before += padding

    yield from header.tokens

    for child, indented in children_it:
        yield from base.format(child, context.with_indented(indented))
