from typing import Iterator
from autobean_refactor import models
from ..lib import alignment
from . import base


@base.formatter(models.Open)
def format_open(open: models.Open, context: base.Context) -> Iterator[models.RawTokenModel]:

    children_it = alignment.BufferedIterator(open.iter_children_formatted())

    for child, indented in children_it.take_until(lambda x: isinstance(x[0], models.Date)):
        yield from base.format(child, context.with_indented(indented))
    
    line = base.collect(children_it.take_until_inclusive(lambda x: isinstance(x[0], models.Eol)), context)
    header = context.parser.parse(line, models.Open)
    if header.raw_currencies:
        if padding := alignment.get_padding_align_left(header.raw_currencies[0], context.options.currency_column):
            header.raw_currencies[0].spacing_before += padding
    yield from header.tokens

    for child, indented in children_it:
        yield from base.format(child, context.with_indented(indented))
