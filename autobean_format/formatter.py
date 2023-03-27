import io
from autobean_refactor import models
from . import options_lib
from . import formatters


def format(model: models.RawModel, options: options_lib.Options, stream: io.StringIO) -> None:
    context = formatters.Context(options=options, stream=stream, indent=0)
    formatters.format(model, context)
