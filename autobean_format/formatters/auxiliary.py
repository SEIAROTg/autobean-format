from typing import Optional, cast
from autobean_refactor import models
from . import base


@base.formatter(models.MetaItem)
def format_meta_item(meta_item: models.MetaItem, context: base.Context) -> models.MetaItem:
    return models.MetaItem.from_children(
        leading_comment=base.format_optional(meta_item.raw_leading_comment, context),
        indent=models.Indent.from_value(context.get_indent()),
        key=base.format(meta_item.raw_key, context),
        value=cast(Optional[models.MetaRawValue], base.format_optional(meta_item.raw_value, context)),
        inline_comment=base.format_optional(meta_item.raw_inline_comment, context),
        trailing_comment=base.format_optional(meta_item.raw_trailing_comment, context),
    )
