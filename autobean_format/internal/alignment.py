from typing import Optional
from autobean_refactor import models


def get_padding_align_left(model: models.RawModel, column: int) -> Optional[str]:
    assert model.token_store
    length = column - model.token_store.get_position(model.first_token).column
    if length <= 0:
        return None
    return ' ' * length


def get_padding_align_right(model: models.RawModel, column: int) -> Optional[str]:
    assert model.token_store
    next_token = model.token_store.get_next(model.last_token)
    assert next_token
    length = column - model.token_store.get_position(next_token).column
    if length <= 0:
        return None
    return ' ' * length
