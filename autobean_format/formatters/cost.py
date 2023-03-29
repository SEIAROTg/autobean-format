from typing import Iterator
from autobean_refactor import models
from . import base


def format_cost(cost: models.UnitCost | models.TotalCost, context: base.Context) -> Iterator[models.RawTokenModel]:
    spaces_in_braces = context.options.spaces_in_braces and next(iter(cost.raw_components), None) is not None

    for child, indented in cost.iter_children_formatted():
        if spaces_in_braces and isinstance(child, models.RightBrace | models.DblRightBrace):
            yield models.Whitespace.from_default()
        yield from base.format(child, context.with_indented(indented))
        if spaces_in_braces and isinstance(child, models.LeftBrace | models.DblLeftBrace):
            yield models.Whitespace.from_default()


base.formatter(models.UnitCost)(format_cost)
base.formatter(models.TotalCost)(format_cost)
