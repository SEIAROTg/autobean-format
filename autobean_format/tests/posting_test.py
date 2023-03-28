from autobean_refactor import models
import pytest
from . import base


class TestPosting(base.BaseTest):

    @pytest.mark.parametrize('src,expected', [
        pytest.param(
            '    Assets:Foo   1.23  USD  ',
            '    Assets:Foo                                                             1.23 USD',
            id='simple',
        ),
        pytest.param(
            '    Assets:Foo   1.23  USD  @@  ',
            '    Assets:Foo                                                             1.23 USD @@',
            id='price',
        ),
        pytest.param(
            '    Assets:Foo       ',
            '    Assets:Foo',
            id='no_amount',
        ),
        pytest.param(
            '    Assets:Foo   USD     ',
            '    Assets:Foo                                                                  USD',
            id='currency_only',
        ),
        pytest.param(
            '    Assets:Foo   1.23     ',
            '    Assets:Foo                                                             1.23',
            id='number_only',
        ),
    ])
    def test_posting(self, src: str, expected: str) -> None:
        assert self.format(src, models.Posting, indent=1) == expected
