import io
from autobean_refactor import models, printer
from . import options_lib
from . import formatters


def format(model: models.RawModel, options: options_lib.Options, stream: io.StringIO) -> None:
    context = formatters.Context(options)
    formatted = formatters.format(model, context)
    printer.print_model(formatted, stream)
