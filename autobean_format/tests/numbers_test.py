from autobean_refactor import models
import pytest
from . import base


class TestNumbers(base.BaseTest):

    @pytest.mark.parametrize('src,expected', [
        ('1-2+3', '1 - 2 + 3'),
        ('1+2*3', '1 + 2 * 3'),
        ('1     +  2  /  5', '1 + 2 / 5'),
        ('--+-+2', '--+-+2'),
        ('-(2)*-3 +- 5', '-(2) * -3 + -5'),
        ('(1+2)*3', '(1 + 2) * 3'),
    ])
    def test_expr(self, src: str, expected: str) -> None:
        assert self.format_inline(src, models.NumberExpr) == expected
