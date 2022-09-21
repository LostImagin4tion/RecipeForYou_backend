from typing import Union
from uuid import UUID

from pydantic import BaseModel


class IngredientSchema(BaseModel):
    uid: Union[UUID, str, None]
    name: str
    images_name: Union[str, None]
    categories: Union[str, None]
