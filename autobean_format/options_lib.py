import argparse
import dataclasses
import enum
import re

_INDENT_REGEX = re.compile('[ \t]+')


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
    inline_comment_column: int
    output_mode: OutputMode
    thousands_separator: ThousandsSeparator
    spaces_in_braces: bool
    sort: bool
    recursive: bool


def _indent_type(value: str) -> str:
    if not _INDENT_REGEX.fullmatch(value):
        raise argparse.ArgumentTypeError(
            f'Expected a string of spaces or tabs (not number). Got {value!r}.')
    return value


def parse_args() -> tuple[str, Options]:
    parser = argparse.ArgumentParser(
        prog='autobean-format',
        description='Formats beancount files',
    )
    parser.add_argument('filename', help="When filename is -, read standard input and disallow --recursive")
    parser.add_argument('--indent', type=_indent_type, default='    ', help='Indentation string. (default: 4 spaces)')
    parser.add_argument('--currency-column', type=int, default=80, help='Column to align currencies to. (default: %(default)s)')
    parser.add_argument('--cost-column', type=int, default=85, help='Column to align cost and price to. (default: %(default)s)')
    parser.add_argument('--inline-comment-column', type=int, default=0, help='Column to align cost and price to. (default: %(default)s)')
    output_mode = parser.add_argument('--output-mode', choices=OutputMode, type=OutputMode, default=OutputMode.STDOUT, help='Output mode. Print to stdout, print a patch file, or update file in place. (default: %(default)s)')
    parser.add_argument('--thousands-separator', choices=ThousandsSeparator, type=ThousandsSeparator, default=ThousandsSeparator.KEEP, help='Add, remove, or keep thousand separators (default: %(default)s)')
    parser.add_argument('--spaces-in-braces', action='store_true', help='Add spaces around content of braces if not empty. (default: false)')
    parser.add_argument('--sort', action='store_true', help='Sort entries by date and time. (default: false)')
    recursive = parser.add_argument('--recursive', action='store_true', help='Recursively format included files. (default: false)')

    args = parser.parse_args()
    if args.filename == '-':
        if args.recursive:
            raise argparse.ArgumentError(
                recursive, 'not supported when reading from stin')
        if args.output_mode == OutputMode.INPLACE:
            raise argparse.ArgumentError(
                output_mode, 'inplace not supported when reading from stin')

    return args.filename, Options(
        indent=args.indent,
        currency_column=args.currency_column,
        cost_column=args.cost_column,
        inline_comment_column=args.inline_comment_column,
        output_mode=args.output_mode,
        thousands_separator=args.thousands_separator,
        spaces_in_braces=args.spaces_in_braces,
        sort=args.sort,
        recursive=args.recursive,
    )
