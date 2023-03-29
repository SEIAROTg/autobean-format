import dataclasses
from typing import Type
from autobean_refactor import models
import pytest
from . import base


class TestCost(base.BaseTest):

    @pytest.mark.parametrize('src,expected,model_type', [
        ('  {  }  ', '{}', models.UnitCost),
        ('  {1.00USD   }  ', '{1.00 USD}', models.UnitCost),
        ('  {{1.00      USD}}  ', '{{1.00 USD}}', models.TotalCost),
        ('  {{1.00      USD  ,   2000-01-01}}  ', '{{1.00 USD, 2000-01-01}}', models.TotalCost),
    ])
    def test_cost(self, src: str, expected: str, model_type: Type[models.UnitCost | models.TotalCost]) -> None:
        assert self.format(src, model_type) == expected

    @pytest.mark.parametrize('src,expected,model_type', [
        ('  {  }  ', '{}', models.UnitCost),
        ('  {1.00USD}  ', '{ 1.00 USD }', models.UnitCost),
        ('  {{1.00      USD}}  ', '{{ 1.00 USD }}', models.TotalCost),
        ('  {{1.00      USD  ,   2000-01-01}}  ', '{{ 1.00 USD, 2000-01-01 }}', models.TotalCost),
    ])
    def test_spaces_in_braces(self, src: str, expected: str, model_type: Type[models.UnitCost | models.TotalCost]) -> None:
        options = dataclasses.replace(base.DEFAULT_OPTIONS, spaces_in_braces=True)
        assert self.format(src, model_type, options) == expected
