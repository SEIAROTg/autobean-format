from autobean_refactor import parser as parser_lib
import pytest


@pytest.fixture(scope='package')
def parser() -> parser_lib.Parser:
    return parser_lib.Parser()
