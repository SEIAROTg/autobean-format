import re
from typing import Iterator
from autobean_refactor import models
from . import base

_NARRATION_RE = re.compile(r';;(.*?)(?:;(.*))?')


@base.formatter(models.Indent)
def format_indent(indent: models.Indent, context: base.Context) -> Iterator[models.RawTokenModel]:
    yield models.Indent.from_value(context.get_indent())


@base.formatter(models.BlockComment)
def format_block_comment(comment: models.BlockComment, context: base.Context) -> Iterator[models.RawTokenModel]:
    yield models.BlockComment.from_value(
        value=comment.value,
        indent=context.get_indent())


@base.formatter(models.InlineComment)
def format_inline_comment(comment: models.InlineComment, context: base.Context) -> Iterator[models.RawTokenModel]:
    match = re.fullmatch(_NARRATION_RE, comment.raw_text)
    if not match:
        yield models.InlineComment.from_value(comment.value)
        return

    # autobean.narration
    raw_text = ';;'
    narration = match.group(1).strip()
    if narration:
        raw_text += ' ' + narration
    comment_part = match.group(2)
    if comment_part is not None:
        raw_text += ' ;'
        comment_value = comment_part.strip()
        if comment_value:
            raw_text += ' ' + comment_value
    yield models.InlineComment.from_raw_text(raw_text)
