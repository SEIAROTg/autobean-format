import argparse
import dataclasses
import enum


class OutputMode(enum.Enum):
    STDOUT = 'stdout'
    DIFF = 'diff'
    INPLACE = 'inplace'

    def __str__(self) -> str:
        return self.value


@dataclasses.dataclass(frozen=True)
class Options:
    indent: str
    currency_column: int
    output_mode: OutputMode
    recursive: bool


def parse_args() -> tuple[str, Options]:
    parser = argparse.ArgumentParser(
        prog='autobean-format',
        description='Formats beancount files',
    )
    parser.add_argument('filename')
    parser.add_argument('--indent', type=str, default='    ', help='Indentation string. (default: 4 spaces)')
    parser.add_argument('--currency-column', type=int, default=80, help='Column to align currencies to. (default: %(default)s)')
    parser.add_argument('--output-mode', choices=OutputMode, type=OutputMode, default=OutputMode.STDOUT, help='Output mode. Print to stdout, print a patch file, or update file in place. (default: %(default)s)')
    parser.add_argument('--recursive', action='store_true', help='Recursively format included files. (default: false)')

    args = parser.parse_args()
    return args.filename, Options(
        indent=args.indent,
        currency_column=args.currency_column,
        output_mode=args.output_mode,
        recursive=args.recursive,
    )
