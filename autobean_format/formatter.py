import io
from autobean_refactor import models, parser as parser_lib
from . import options_lib
from . import formatters


def format(
    model: models.RawModel,
    parser: parser_lib.Parser,
    options: options_lib.Options,
    stream: io.StringIO,
) -> None:
    context = formatters.Context(parser=parser, options=options, indent=0)
    for token in formatters.format(model, context):
        stream.write(token.raw_text)
