import dataclasses
import io
from typing import Any, Callable, Iterable, Iterator, Type, TypeVar
from autobean_refactor import models, parser as parser_lib
from .. import options_lib

_M = TypeVar('_M', bound=models.RawModel)


@dataclasses.dataclass(frozen=True)
class Context:
    parser: parser_lib.Parser
    options: options_lib.Options
    indent: int

    def with_indented(self, indented: bool) -> 'Context':
        if not indented:
            return self
        return dataclasses.replace(self, indent=self.indent + 1)

    def get_indent(self) -> str:
        return self.options.indent * self.indent


_Formatter = Callable[[_M, Context], Iterator[models.RawTokenModel]]
_FORMATTERS = dict[Type[models.RawModel], _Formatter[Any]]()


def formatter(model_type: Type[_M]) -> Callable[[_Formatter[_M]], _Formatter[_M]]:
    def decorator(formatter: _Formatter[_M]) -> _Formatter[_M]:
        _FORMATTERS[model_type] = formatter
        return formatter
    return decorator


def format(model: models.RawModel, context: Context) -> Iterator[models.RawTokenModel]:
    for cls in type(model).__mro__:
        fn = _FORMATTERS.get(cls)
        if fn is not None:
            break
    else:
        assert False
    yield from fn(model, context)


def collect(children: Iterable[tuple[models.RawModel, bool]], context: Context) -> str:
    stream = io.StringIO()
    for child, indented in children:
        for token in format(child, context.with_indented(indented)):
            stream.write(token.raw_text)
    return stream.getvalue()
