import dataclasses
from autobean_refactor import models
import pytest
from . import base


class TestInlineComment(base.BaseTest):

    @pytest.mark.parametrize('src,expected,column', [
        pytest.param(
            '2000-10-01      custom\t   "foo"   1.23   USD  "bar";xxx',
            '2000-10-01 custom "foo" 1.23 USD "bar" ; xxx\n',
            0,
            id='default',
        ),
        pytest.param(
            '2000-10-01      custom\t   "foo"   1.23   USD  "bar";xxx',
            '2000-10-01 custom "foo" 1.23 USD "bar"                      ; xxx\n',
            60,
            id='aligned',
        ),
        pytest.param(
            '2000-10-01 balance Assets:Foo 1.00 USD    ;yyy',
            '2000-10-01 balance Assets:Foo                          1.00 USD                 ; yyy\n',
            80,
            id='aligned balance',
        ),
        pytest.param(
            '2000-10-01 *    ;foo\n    Assets:Foo 1.00 USD   ;bar',
            (
                '2000-10-01 *                                                                    ; foo\n' +
                '    Assets:Foo                                         1.00 USD                 ; bar\n'
            ),
            80,
            id='aligned txn',
        ),
        pytest.param(
            '2000-10-01 *    ;foo\n    Assets:Foo 1.00 USD   ;bar',
            (
                '2000-10-01 *                                                ; foo\n' +
                '    Assets:Foo                                         1.00 USD ; bar\n'
            ),
            60,
            id='aligned txn unsatisified',
        ),
    ])
    def test_inline_comment(self, src: str, expected: str, column: int) -> None:
        options = dataclasses.replace(
            base.DEFAULT_OPTIONS,
            currency_column=60,
            inline_comment_column=column)
        assert self.format(src, models.File, options) == expected
