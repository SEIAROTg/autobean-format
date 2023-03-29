import argparse
import dataclasses
import enum


class OutputMode(enum.Enum):
    STDOUT = 'stdout'
    DIFF = 'diff'
    INPLACE = 'inplace'

    def __str__(self) -> str:
        return self.value


class ThousandsSeparator(enum.Enum):
    ADD = 'add'
    REMOVE = 'remove'
    KEEP = 'keep'

    def __str__(self) -> str:
        return self.value


@dataclasses.dataclass(frozen=True)
class Options:
    indent: str
    currency_column: int
    cost_column: int
    output_mode: OutputMode
    thousands_separator: ThousandsSeparator
    recursive: bool


def parse_args() -> tuple[str, Options]:
    parser = argparse.ArgumentParser(
        prog='autobean-format',
        description='Formats beancount files',
    )
    parser.add_argument('filename')
    parser.add_argument('--indent', type=str, default='    ', help='Indentation string. (default: 4 spaces)')
    parser.add_argument('--currency-column', type=int, default=80, help='Column to align currencies to. (default: %(default)s)')
    parser.add_argument('--cost-column', type=int, default=85, help='Column to align cost and price to. (default: %(default)s)')
    parser.add_argument('--output-mode', choices=OutputMode, type=OutputMode, default=OutputMode.STDOUT, help='Output mode. Print to stdout, print a patch file, or update file in place. (default: %(default)s)')
    parser.add_argument('--thousands-separator', choices=ThousandsSeparator, type=ThousandsSeparator, default=ThousandsSeparator.KEEP, help='Add, remove, or keep thousand separators (default: %(default)s)')
    parser.add_argument('--recursive', action='store_true', help='Recursively format included files. (default: false)')

    args = parser.parse_args()
    return args.filename, Options(
        indent=args.indent,
        currency_column=args.currency_column,
        cost_column=args.cost_column,
        output_mode=args.output_mode,
        thousands_separator=args.thousands_separator,
        recursive=args.recursive,
    )
