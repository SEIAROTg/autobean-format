import copy
from autobean_refactor import models
from . import base


@base.formatter(models.Close)
def format_close(close: models.Close, context: base.Context) -> models.Close:
    return models.Close.from_children(
        leading_comment=base.format_optional(close.raw_leading_comment, context),
        date=base.format(close.raw_date, context),
        account=base.format(close.raw_account, context),
        inline_comment=base.format_optional(close.raw_inline_comment, context),
        meta=base.format_repeated(close.raw_meta_with_comments, context.indented()),
        trailing_comment=base.format_optional(close.raw_trailing_comment, context),
    )
