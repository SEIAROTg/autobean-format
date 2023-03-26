import argparse
import dataclasses


@dataclasses.dataclass(frozen=True)
class Options:
    indent: str
    currency_column: int


def parse_args() -> tuple[str, Options]:
    parser = argparse.ArgumentParser(
        prog='autobean-format',
        description='Formats beancount files',
    )
    parser.add_argument('filename')
    parser.add_argument('--indent', type=str, default='    ')
    parser.add_argument('--currency-column', type=int, default=80)

    args = parser.parse_args()
    return args.filename, Options(
        indent=args.indent,
        currency_column=args.currency_column,
    )
