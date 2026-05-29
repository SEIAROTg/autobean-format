from typing import Type
from autobean_refactor import models
import pytest
from . import base


class TestToken(base.BaseTest):

    @pytest.mark.parametrize('model_type,src,expected', [
        pytest.param(
            models.InlineComment, ';!foo', '; !foo',
            id='inline_comment',
        ),
        pytest.param(
            models.InlineComment, ';!foo;bar', '; !foo;bar',
            id='inline_comment and semicolon',
        ),
        pytest.param(
            models.InlineComment, ';', ';',
            id='inline_comment_empty',
        ),
        pytest.param(
            models.InlineComment, ';;foo', ';; foo',
            id='autobean.narration',
        ),
        pytest.param(
            models.InlineComment, ';;', ';;',
            id='empty autobean.narration',
        ),
        pytest.param(
            models.InlineComment, ';;;', ';; ;',
            id='empty autobean.narration and empty comment',
        ),
        pytest.param(
            models.InlineComment, ';;;;;', ';; ; ;;',
            id='empty autobean.narration and semicolons',
        ),
        pytest.param(
            models.InlineComment, ';;foo;bar;baz', ';; foo ; bar;baz',
            id='autobean.narration and comment',
        ),
        # https://github.com/SEIAROTg/autobean-format/issues/15
        pytest.param(
            models.BlockComment,
            ';; A\n;;; B\n; C\n;;hello\n;four',
            ';;  A\n;;; B\n;   C\n;;  hello\n;   four',
            id='block_comment_semi_alignment',
        ),
    ])
    def test_token(self, model_type: Type[models.RawTokenModel], src: str, expected: str) -> None:
        assert self.format_token(src, model_type) == expected
