import difflib
import io
import sys
from . import formatter, options_lib
from autobean_refactor import models, parser as parser_lib


def main() -> None:
    filename, options = options_lib.parse_args()
    parser = parser_lib.Parser()
    with open(filename) as f:
        text = f.read()
    file = parser.parse(text, models.File)
    file.auto_claim_comments()
    
    stream = io.StringIO()
    formatter.format(file, options, stream)

    match options.output_mode:
        case options_lib.OutputMode.STDOUT:
            sys.stdout.write(stream.getvalue())
            sys.stdout.flush()
        case options_lib.OutputMode.DIFF:
            diff = difflib.unified_diff(
                text.splitlines(keepends=True),
                stream.getvalue().splitlines(keepends=True),
                fromfile=filename,
                tofile=filename + ' (formatted)')
            sys.stdout.writelines(diff)
            sys.stdout.flush()
        case options_lib.OutputMode.INPLACE:
            with open(filename, 'w') as f:
                f.write(stream.getvalue())
