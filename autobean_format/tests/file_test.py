from autobean_refactor import models
import pytest
from . import base


class TestFile(base.BaseTest):

    @pytest.mark.parametrize('src,expected', [
        pytest.param(
            '', '',
            id='empty',
        ),
        pytest.param(
            'include "foo.bean"',
            'include "foo.bean"\n',
            id='trailing_newline_add',
        ),
        pytest.param(
            'include "foo.bean"\n',
            'include "foo.bean"\n',
            id='trailing_newline_existing',
        ),
        pytest.param(
            'include "foo.bean"\n\n\n\n\n\ninclude "bar.bean"\n\n\n\n\n',
            'include "foo.bean"\n\ninclude "bar.bean"\n',
            id='remove_blank_lines',
        ),
        pytest.param(
            'include "foo.bean"\n\n; xxx\n\ninclude "bar.bean"\n',
            'include "foo.bean"\n\n; xxx\n\ninclude "bar.bean"\n',
            id='block_comment',
        ),
        pytest.param(
            'include "foo.bean"\n\n    ; xxx\n  ; yy\n\ninclude "bar.bean"\n',
            'include "foo.bean"\n\n; xxx\n; yy\n\ninclude "bar.bean"\n',
            id='block_comment_dedent',
        ),
        pytest.param(
            'include "foo.bean"\n; xxx\ninclude "bar.bean"\n; yyy\n',
            'include "foo.bean"\n; xxx\ninclude "bar.bean"\n; yyy\n',
            id='surrounding_comment',
        ),
        pytest.param(
            'include "foo.bean"\n*xxx\ninclude "bar.bean"\n',
            'include "foo.bean"\n\n*xxx\n\ninclude "bar.bean"\n',
            id='add_blank_lines',
        ),
        pytest.param(
            'include "foo.bean"\n*xxx\n',
            'include "foo.bean"\n\n*xxx\n',
            id='add_blank_lines_last',
        ),
        pytest.param(
            'include "foo.bean"\nplugin "foo"\n',
            'include "foo.bean"\nplugin "foo"\n',
            id='no_blank_lines_same_category',
        ),
        pytest.param(
            'include "foo.bean"\npushtag #foo\n',
            'include "foo.bean"\n\npushtag #foo\n',
            id='add_blank_lines_different_category',
        ),
    ])
    def test_file(self, src: str, expected: str) -> None:
        assert self.format(src, models.File) == expected  
