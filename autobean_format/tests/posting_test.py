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
        pytest.param(
            '    Assets:Foo   1.00  GBP  @@  1.23  USD  ',
            '    Assets:Foo                                                             1.00 GBP  @@ 1.23 USD',
            id='price_explicit',
        ),
        pytest.param(
            '    Assets:Foo   1.00  GBP  @@  ',
            '    Assets:Foo                                                             1.00 GBP  @@',
            id='price_implicit',
        ),
        pytest.param(
            '    Assets:Foo   @@',
            '    Assets:Foo                                                                       @@',
            id='price_no_amount',
        ),
        pytest.param(
            '    Assets:Foo  1.00 GBP   {1.23 USD}   @ 1.23 USD  ',
            '    Assets:Foo                                                             1.00 GBP  {1.23 USD} @ 1.23 USD',
            id='cost_and_price',
        ),
        pytest.param(
            '    Assets:Foo  1.00 GBP   {}   ',
            '    Assets:Foo                                                             1.00 GBP  {}',
            id='cost_implicit',
        ),
        pytest.param(
            '    Assets:Foo  {}   ',
            '    Assets:Foo                                                                       {}',
            id='cost_no_amount',
        ),
    ])
    def test_posting(self, src: str, expected: str) -> None:
        assert self.format(src, models.Posting, indent=1) == expected
