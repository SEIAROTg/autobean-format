from typing import Optional, cast
from autobean_refactor import models
from . import base


@base.formatter(models.Include)
def format_include(include: models.Include, context: base.Context) -> models.Include:
    return models.Include.from_children(
        leading_comment=base.format_optional(include.raw_leading_comment, context),
        filename=base.format(include.raw_filename, context),
        inline_comment=base.format_optional(include.raw_inline_comment, context),
        trailing_comment=base.format_optional(include.raw_trailing_comment, context),
    )


@base.formatter(models.Option)
def format_option(option: models.Option, context: base.Context) -> models.Option:
    return models.Option.from_children(
        leading_comment=base.format_optional(option.raw_leading_comment, context),
        key=base.format(option.raw_key, context),
        value=base.format(option.raw_value, context),
        inline_comment=base.format_optional(option.raw_inline_comment, context),
        trailing_comment=base.format_optional(option.raw_trailing_comment, context),
    )


@base.formatter(models.Plugin)
def format_plugin(plugin: models.Plugin, context: base.Context) -> models.Plugin:
    return models.Plugin.from_children(
        leading_comment=base.format_optional(plugin.raw_leading_comment, context),
        name=base.format(plugin.raw_name, context),
        config=base.format_optional(plugin.raw_config, context),
        inline_comment=base.format_optional(plugin.raw_inline_comment, context),
        trailing_comment=base.format_optional(plugin.raw_trailing_comment, context),
    )


@base.formatter(models.Pushmeta)
def format_pushmeta(pushmeta: models.Pushmeta, context: base.Context) -> models.Pushmeta:
    return models.Pushmeta.from_children(
        leading_comment=base.format_optional(pushmeta.raw_leading_comment, context),
        key=base.format(pushmeta.raw_key, context),
        value=cast(Optional[models.MetaRawValue], base.format_optional(pushmeta.raw_value, context)),
        inline_comment=base.format_optional(pushmeta.raw_inline_comment, context),
        trailing_comment=base.format_optional(pushmeta.raw_trailing_comment, context),
    )


@base.formatter(models.Popmeta)
def format_popmeta(popmeta: models.Popmeta, context: base.Context) -> models.Popmeta:
    return models.Popmeta.from_children(
        leading_comment=base.format_optional(popmeta.raw_leading_comment, context),
        key=base.format(popmeta.raw_key, context),
        inline_comment=base.format_optional(popmeta.raw_inline_comment, context),
        trailing_comment=base.format_optional(popmeta.raw_trailing_comment, context),
    )


@base.formatter(models.Pushtag)
def format_pushtag(pushtag: models.Pushtag, context: base.Context) -> models.Pushtag:
    return models.Pushtag.from_children(
        leading_comment=base.format_optional(pushtag.raw_leading_comment, context),
        tag=base.format(pushtag.raw_tag, context),
        inline_comment=base.format_optional(pushtag.raw_inline_comment, context),
        trailing_comment=base.format_optional(pushtag.raw_trailing_comment, context),
    )


@base.formatter(models.Poptag)
def format_poptag(poptag: models.Poptag, context: base.Context) -> models.Poptag:
    return models.Poptag.from_children(
        leading_comment=base.format_optional(poptag.raw_leading_comment, context),
        tag=base.format(poptag.raw_tag, context),
        inline_comment=base.format_optional(poptag.raw_inline_comment, context),
        trailing_comment=base.format_optional(poptag.raw_trailing_comment, context),
    )
