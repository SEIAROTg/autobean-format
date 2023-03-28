from typing import Iterator
from autobean_refactor import models
from .. import options_lib
from . import base


@base.formatter(models.Number)
def format_number(number: models.Number, context: base.Context) -> Iterator[models.RawTokenModel]:
    match context.options.thousands_separator:
        case options_lib.ThousandsSeparator.ADD:
            yield models.Number.from_raw_text(f'{number.value:,f}')
        case options_lib.ThousandsSeparator.REMOVE:
            yield models.Number.from_raw_text(f'{number.value:f}')
        case _:
            yield number
