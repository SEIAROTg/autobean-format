import re
from autobean_refactor import models
from . import base

_NARRATION_RE = re.compile(r';;(.*?)(?:;(.*))?')


@base.formatter(models.Indent)
def format_indent(indent: models.Indent, context: base.Context) -> None:
    indent = models.Indent.from_value(context.get_indent())
    base.print_token(indent, context)


@base.formatter(models.BlockComment)
def format_block_comment(comment: models.BlockComment, context: base.Context) -> None:
    comment = models.BlockComment.from_value(
        value=comment.value,
        indent=context.get_indent())
    base.print_token(comment, context)


@base.formatter(models.InlineComment)
def format_inline_comment(comment: models.InlineComment, context: base.Context) -> None:
    match = re.fullmatch(_NARRATION_RE, comment.raw_text)
    if not match:
        base.print_token(models.InlineComment.from_value(comment.value), context)
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
    context.stream.write(raw_text)
