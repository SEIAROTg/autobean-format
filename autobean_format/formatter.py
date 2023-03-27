import io
from autobean_refactor import models
from . import options_lib
from . import formatters


def format(model: models.RawModel, options: options_lib.Options, stream: io.StringIO) -> None:
    context = formatters.Context(options=options, indent=0)
    for token in formatters.format(model, context):
        stream.write(token.raw_text)
