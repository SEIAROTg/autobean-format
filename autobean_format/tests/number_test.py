import dataclasses
from autobean_refactor import models
import pytest
from .. import options_lib
from . import base


class TestNumber(base.BaseTest):

    @pytest.mark.parametrize('src,expected,mode', [
        ('1234567890.0987654321', '1234567890.0987654321', 'keep'),
        ('1,234,567,890.0987654321', '1,234,567,890.0987654321', 'keep'),
        ('1234567890.0987654321', '1,234,567,890.0987654321', 'add'),
        ('1234567890.0987654321', '1234567890.0987654321', 'remove'),
        ('1,234,567,890.0987654321', '1234567890.0987654321', 'remove'),
    ])
    def test_thousands_separator(self, src: str, expected: str, mode: str) -> None:
        options = dataclasses.replace(
            base.DEFAULT_OPTIONS,
            thousands_separator=options_lib.ThousandsSeparator(mode))
        assert self.format_token(src, models.Number, options) == expected
