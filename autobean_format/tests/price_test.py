from autobean_refactor import models
import pytest
from . import base


class TestPrice(base.BaseTest):

    @pytest.mark.parametrize('src,expected', [
        pytest.param(
            '2000-01-01      price\tGBP  1.23   USD',
            '2000-01-01 price GBP                                                       1.23 USD',
            id='simple',
        ),
        pytest.param(
            '; aaa\n2000-01-01      price\tGBP  1.23   USD  ; xxx\n; bbb',
            '; aaa\n2000-01-01 price GBP                                                       1.23 USD ; xxx\n; bbb',
            id='comment',
        ),
        pytest.param(
            '2000-01-01 price GBPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP   1.23   USD',
            '2000-01-01 price GBPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP 1.23 USD',
            id='no_align_currency_long_currency',
        ),
    ])
    def test_price(self, src: str, expected: str) -> None:
        assert self.format(src, models.Price) == expected  
