import copy
import re
from autobean_refactor import models
from . import base

_NARRATION_RE = re.compile(r';;(.*?)(?:;(.*))?')


@base.formatter(models.BlockComment)
def format_block_comment(comment: models.BlockComment, context: base.Context) -> models.BlockComment:
    return models.BlockComment.from_value(
        value=comment.value,
        indent=context.get_indent())


@base.formatter(models.InlineComment)
def format_inline_comment(comment: models.InlineComment, context: base.Context) -> models.InlineComment:
    match = re.fullmatch(_NARRATION_RE, comment.raw_text)
    if match:  # autobean.narration
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
        return models.InlineComment.from_raw_text(raw_text)
    return models.InlineComment.from_value(comment.value)


@base.formatter(models.IgnoredLine)
def format_ignored_line(line: models.IgnoredLine, context: base.Context) -> models.IgnoredLine:
    return copy.deepcopy(line)


@base.formatter(models.Tag)
def format_tag(tag: models.Tag, context: base.Context) -> models.Tag:
    return models.Tag.from_value(tag.value)


@base.formatter(models.Date)
def format_date(date: models.Date, context: base.Context) -> models.Date:
    return models.Date.from_value(date.value)


@base.formatter(models.Account)
def format_account(account: models.Account, context: base.Context) -> models.Account:
    return models.Account.from_value(account.value)


@base.formatter(models.Currency)
def format_currency(currency: models.Currency, context: base.Context) -> models.Currency:
    return models.Currency.from_value(currency.value)


@base.formatter(models.EscapedString)
def format_escaped_string(string: models.EscapedString, context: base.Context) -> models.EscapedString:
    return models.EscapedString.from_value(string.value)


@base.formatter(models.MetaKey)
def format_meta_key(key: models.MetaKey, context: base.Context) -> models.MetaKey:
    return models.MetaKey.from_value(key.value)
