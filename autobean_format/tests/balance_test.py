from autobean_refactor import models
import pytest
from . import base


class TestBalance(base.BaseTest):

    @pytest.mark.parametrize('src,expected', [
        pytest.param(
            '2000-01-01      balance\tAssets:Foo  1.23   USD',
            '2000-01-01 balance Assets:Foo                                              1.23 USD',
            id='simple',
        ),
        pytest.param(
            '2000-01-01      balance\tAssets:Foo  1.23  ~   0.00   USD',
            '2000-01-01 balance Assets:Foo                                       1.23 ~ 0.00 USD',
            id='tolerance',
        ),
        pytest.param(
            '2000-01-01      balance\tAssets:Foo  (1.23  *   0.00)   USD',
            '2000-01-01 balance Assets:Foo                                     (1.23 * 0.00) USD',
            id='expr',
        ),
        pytest.param(
            '; aaa\n2000-01-01      balance\tAssets:Foo  1.23   USD  ; xxx\n; bbb',
            '; aaa\n2000-01-01 balance Assets:Foo                                              1.23 USD ; xxx\n; bbb',
            id='comment',
        ),
        pytest.param(
            '2000-01-01 balance Assets:Foooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo   1.23   USD',
            '2000-01-01 balance Assets:Foooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo 1.23 USD',
            id='no_align_currency_long_account',
        ),
    ])
    def test_balance(self, src: str, expected: str) -> None:
        assert self.format(src, models.Balance) == expected  
