import dataclasses
import io
from typing import Any, Callable, Type, TypeVar
from autobean_refactor import models
from .. import options_lib

_M = TypeVar('_M', bound=models.RawModel)


@dataclasses.dataclass(frozen=True)
class Context:
    options: options_lib.Options
    stream: io.TextIOBase
    indent: int

    def with_indented(self, indented: bool) -> 'Context':
        if not indented:
            return self
        return dataclasses.replace(self, indent=self.indent + 1)

    def get_indent(self) -> str:
        return self.options.indent * self.indent


_Formatter = Callable[[_M, Context], None]
_FORMATTERS = dict[Type[models.RawModel], _Formatter[Any]]()


def formatter(model_type: Type[_M]) -> Callable[[_Formatter[_M]], _Formatter[_M]]:
    def decorator(formatter: _Formatter[_M]) -> _Formatter[_M]:
        _FORMATTERS[model_type] = formatter
        return formatter
    return decorator


def format(model: _M, context: Context) -> None:
    formatter = _FORMATTERS.get(type(model))
    if formatter:
        formatter(model, context)
    elif isinstance(model, models.RawTokenModel):
        context.stream.write(model.raw_text)
    else:
        for child, indented in model.iter_children_formatted():
            format(child, context.with_indented(indented))


def print_token(token: models.RawTokenModel, context: Context) -> None:
    context.stream.write(token.raw_text)
