from typing import Iterator
from autobean_refactor import models
from ..lib import alignment
from . import base


@base.formatter(models.Open)
def format_open(open: models.Open, context: base.Context) -> Iterator[models.RawTokenModel]:

    tracker = alignment.PositionTracker()
    children_it = alignment.BufferedIterator(open.iter_children_formatted())

    for child, indented in children_it.take_until(lambda x: isinstance(x[0], models.Currency)):
        for token in base.format(child, context.with_indented(indented)):
            tracker.append(token)
            yield token

    if not children_it.empty():
        yield from tracker.pad_to_column(context.options.currency_column)

    for child, indented in children_it:
        yield from base.format(child, context.with_indented(indented))
