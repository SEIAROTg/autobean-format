import dataclasses
from typing import Any, Callable, Iterable, Optional, Type, TypeVar
from autobean_refactor import models
from .. import options_lib

_M = TypeVar('_M', bound=models.RawModel)


@dataclasses.dataclass(frozen=True)
class Context:
    options: options_lib.Options
    indent: int = 0

    def indented(self) -> 'Context':
        return dataclasses.replace(self, indent=self.indent + 1)

    def get_indent(self) -> str:
        return self.options.indent * self.indent


_Formatter = Callable[[_M, Context], _M]
_FORMATTERS = dict[Type[models.RawModel], _Formatter[Any]]()


def formatter(model_type: Type[_M]) -> Callable[[_Formatter[_M]], _Formatter[_M]]:
    def decorator(formatter: _Formatter[_M]) -> _Formatter[_M]:
        _FORMATTERS[model_type] = formatter
        return formatter
    return decorator


def format(model: _M, context: Context) -> _M:
    return _FORMATTERS[type(model)](model, context)


def format_optional(model: Optional[_M], context: Context) -> Optional[_M]:
    if model is None:
        return None
    return format(model, context)


def format_repeated(models: Iterable[_M], context: Context) -> Iterable[_M]:
    for model in models:
        yield format(model, context)
