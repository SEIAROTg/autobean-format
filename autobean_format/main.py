import io
import sys
from . import formatter, options_lib
from autobean_refactor import models, parser as parser_lib


def main() -> None:
    filename, options = options_lib.parse_args()
    parser = parser_lib.Parser()
    with open(filename) as f:
        file = parser.parse(f.read(), models.File)
    file.auto_claim_comments()
    
    stream = io.StringIO()
    formatter.format(file, options, stream)
    sys.stdout.write(stream.getvalue())
    sys.stdout.flush()
